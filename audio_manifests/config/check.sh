#!/usr/bin/env sh
# audio-rt-ground -- one command, three places: editor, pre-commit hook, CI all run THIS.
#
# Local/CI parity contract (reference/quality_gates_ci_manifest.md section G2): a gate that
# only runs in CI teaches people to push and wait, and a gate that only runs locally does
# not exist. If you add a check to CI, add it HERE and let CI call this script.
# Leg awareness: this script runs the CURRENT-OS leg; CI runs both legs by running this
# same script once per leg job (config/ci-github.yml).
#
# Usage:
#   ./check.sh                 run the default blocking gates, stop at the first failure
#   ./check.sh --all           run every default gate, report all failures, exit non-zero
#   ./check.sh --fix           apply clang-format in place, then run the gates (LOCAL ONLY)
#   ./check.sh tidy audits     run only the named gates
#   ./check.sh san             named-only lanes: san (ASan+UBSan), tsan (Linux), bench
#
# Default gates:    format tidy build unit audits remark schema
# Named-only lanes: san tsan bench   (config/ci-github.yml wires them; testing T8, G4)
# Exit codes: 0 all pass; 1 at least one gate failed; 2 usage or wrong environment.
# Every gate failure also prints one machine-readable line (the traceability doctrine --
# the artifact tells the agent WHAT failed and WHERE to read next):
#   GATE-FAIL gate=<name> route=<file/section to read before patching>
# Placeholder gates print GATE-NOT-WIRED and pass until their DECIDE is made; the ratchet
# (quality_gates_ci section G8) obliges you to flip each one blocking during bring-up.
#
# NEVER pass --fix in CI. CI reports; humans and hooks fix.
# NEVER green a gate by loosening a config in the same change that trips it -- a loosening
# is its own reviewed commit with a ledger row (quality_gates_ci section G8).

set -eu

# ---- leg detection ---------------------------------------------------------------------
# MEASURED 2026-08-12: in the MSYS2 CLANG64 shell `uname -s` prints MINGW64_NT-10.0-26200,
# so the *_NT* suffix is the Windows discriminator and MSYSTEM tells the flavors apart.
case "$(uname -s)" in
  Linux*) LEG=linux; PRESET_LEG=linux ;;
  *_NT*)  LEG=windows; PRESET_LEG=win ;;
  *) echo "check.sh: unsupported leg '$(uname -s)' -- hub H2 pins the two legs" >&2; exit 2 ;;
esac

if [ "$LEG" = windows ] && [ "${MSYSTEM:-}" != "CLANG64" ]; then
  echo "check.sh: MSYSTEM='${MSYSTEM:-unset}' -- the Windows leg builds only in the MSYS2" >&2
  echo "CLANG64 environment (hub H3). Open a CLANG64 shell, not MSYS/MINGW64/UCRT64." >&2
  exit 2
fi

# ---- project pins (DECIDE rows) --------------------------------------------------------
# DECIDE: preset names must match config/CMakePresets.json (toolchain_build section B5).
PRESET="${CHECK_PRESET:-$PRESET_LEG-test}"           # configure/build/ctest preset for the gates
PERF_PRESET="${CHECK_PERF_PRESET:-$PRESET_LEG-perf}" # remark + bench lanes build this preset
SAN_PRESET="${CHECK_SAN_PRESET:-$PRESET_LEG-test}"   # ASan+UBSan already ride cfg-test (testing T8)
TSAN_PRESET="${CHECK_TSAN_PRESET:-linux-tsan}"       # TSan: Linux leg only, own preset (hub H5)
# DECIDE: must match the presets' binaryDir layout.
BUILD_DIR="${CHECK_BUILD_DIR:-build/$PRESET}"
# DECIDE: path of the linked core static library -- the symbol audit's target (invariant 8).
CORE_LIB="${CHECK_CORE_LIB:-build/$PRESET/core/libaudio_core.a}"
ALLOWLIST="${CHECK_SYMBOL_ALLOWLIST:-config/core_symbol_allowlist.txt}"  # bootstrap: G9
KERNEL_MANIFEST="${CHECK_KERNEL_MANIFEST:-tools/kernel_manifest.txt}"    # remark rows: G4
SCHEMA_SAMPLES="${CHECK_SCHEMA_SAMPLES:-test/data/session_reports}"      # samples: E8
if [ "$LEG" = windows ]; then PY="${PYTHON:-python}"; else PY="${PYTHON:-python3}"; fi

# ---- argument parsing ------------------------------------------------------------------
FAILED=""
KEEP_GOING=0
FIX=0
GATES=""
DEFAULT_GATES="format tidy build unit audits remark schema"
KNOWN_GATES="$DEFAULT_GATES san tsan bench"

for arg in "$@"; do
  case "$arg" in
    --all) KEEP_GOING=1 ;;
    --fix) FIX=1 ;;
    -*)    echo "check.sh: unknown flag: $arg" >&2; exit 2 ;;
    *)     GATES="$GATES $arg" ;;
  esac
done
[ -n "$GATES" ] || GATES="$DEFAULT_GATES"
for g in $GATES; do
  case " $KNOWN_GATES " in
    *" $g "*) ;;
    *) echo "check.sh: unknown gate '$g' (known: $KNOWN_GATES)" >&2; exit 2 ;;
  esac
done

want() { case " $GATES " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# Fix-routing pointers, printed on failure (gate ledger: quality_gates_ci section G1).
route_for() {
  case "$1" in
    format) echo "config/.clang-format + ./check.sh --fix" ;;
    tidy)   echo "reference/toolchain_build_manifest.md section B3 (deviations need a record)" ;;
    build)  echo "reference/toolchain_build_manifest.md section B11" ;;
    unit)   echo "reference/testing_verification_manifest.md section T13" ;;
    audits) echo "reference/quality_gates_ci_manifest.md section G9" ;;
    remark) echo "reference/dsp_kernel_patterns_manifest.md section K5 + optimization P3" ;;
    schema) echo "reference/error_tracing_contract_manifest.md section E8" ;;
    san|tsan) echo "reference/testing_verification_manifest.md section T8" ;;
    bench)  echo "reference/optimization_microarch_manifest.md section P2" ;;
    *)      echo "reference/quality_gates_ci_manifest.md section G1" ;;
  esac
}

run() {
  name="$1"; shift
  printf '\n=== %s ===\n' "$name"
  if "$@"; then
    printf -- '--- %s: ok\n' "$name"
  else
    printf '!!! %s: FAILED\n' "$name"
    printf 'GATE-FAIL gate=%s route=%s\n' "$name" "$(route_for "$name")"
    FAILED="$FAILED $name"
    [ "$KEEP_GOING" -eq 1 ] || { printf '\nFAILED:%s\n' "$FAILED"; exit 1; }
  fi
}

# ---- gate bodies -----------------------------------------------------------------------

format_gate() {
  git ls-files '*.c' '*.h' | xargs -r clang-format --dry-run -Werror
}

tidy_gate() {
  # clang-tidy reads flags from the compile database the configure step exports
  # (CMAKE_EXPORT_COMPILE_COMMANDS; toolchain_build section B5). -p names its directory
  # [CC-FACT]. Headers are covered via HeaderFilterRegex in config/.clang-tidy.
  [ -f "$BUILD_DIR/compile_commands.json" ] || cmake --preset "$PRESET" >/dev/null || return 1
  git ls-files '*.c' | grep -E '^(core|ports|adapters|shell)/' \
    | xargs -r clang-tidy --quiet -p "$BUILD_DIR"
}

build_gate() {
  cmake --preset "$PRESET" && cmake --build --preset "$PRESET"
}

unit_gate() {
  # Unit + property + table + tolerance-golden suites all run as ctest tests (testing T1).
  ctest --preset "$PRESET" --output-on-failure
}

audits_gate() {
  rc=0
  "$PY" config/audit_includes.py . || rc=1
  if [ -f "$CORE_LIB" ] && [ -f "$ALLOWLIST" ]; then
    "$PY" config/audit_symbols.py "$CORE_LIB" "$ALLOWLIST" || rc=1
  else
    echo "GATE-NOT-WIRED gate=symbol-audit missing=$CORE_LIB or $ALLOWLIST route=quality_gates_ci G9 (bootstrap ritual)"
  fi
  return $rc
}

remark_gate() {
  # Invariant 15: a hot kernel that silently de-vectorizes fails the build.
  # Wiring spec: quality_gates_ci section G4. Manifest rows: "path/to/kernel.c[:function]".
  if [ ! -f "$KERNEL_MANIFEST" ]; then
    echo "GATE-NOT-WIRED gate=remark missing=$KERNEL_MANIFEST route=quality_gates_ci G4 (list the hot TUs; G8 flips this blocking)"
    return 0
  fi
  cmake --preset "$PERF_PRESET" >/dev/null || return 1
  log="build/$PERF_PRESET/remarks.log"
  # Touch every listed TU so an incremental build re-emits its remarks.
  while IFS= read -r row; do
    case "$row" in ''|'#'*) continue ;; esac
    tu="${row%%:*}"
    [ -f "$tu" ] && touch "$tu"
  done < "$KERNEL_MANIFEST"
  # Kernel TUs build with -Rpass=loop-vectorize in the perf preset (flag canon B2/B8);
  # remarks arrive on stderr. MEASURED 2026-08-12 (clang 22.1.8) remark shape:
  #   <tu>:<line>:<col>: remark: vectorized loop (vectorization width: 8, interleaved count: 4)
  if ! cmake --build --preset "$PERF_PRESET" >"$log" 2>&1; then
    cat "$log" >&2
    return 1
  fi
  rc=0
  while IFS= read -r row; do
    case "$row" in ''|'#'*) continue ;; esac
    tu="${row%%:*}"
    if ! grep -Eq "$tu:[0-9]+:[0-9]+: (remark: )?vectorized loop" "$log"; then
      echo "GATE-FAIL gate=remark tu=$tu reason=no-vectorized-loop-remark route=dsp_kernel_patterns K5 + optimization P3"
      rc=1
    fi
  done < "$KERNEL_MANIFEST"
  return $rc
}

schema_gate() {
  # Session reports are the agent's patch input; a writer that drifts from the schema
  # breaks the feedback loop silently (error_tracing E8, observability O7).
  if [ ! -d "$SCHEMA_SAMPLES" ]; then
    echo "GATE-NOT-WIRED gate=schema missing=$SCHEMA_SAMPLES route=error_tracing E8 (commit sample reports; G8 flips this blocking)"
    return 0
  fi
  # DECIDE: pin one validator and delete the fallback. Placeholder spelling: the Python
  # package `check-jsonschema` ships a CLI of that name [CC-FACT -- verify on install].
  if command -v check-jsonschema >/dev/null 2>&1; then
    check-jsonschema --schemafile config/session_report.schema.json "$SCHEMA_SAMPLES"/*.json
  else
    echo "GATE-NOT-WIRED gate=schema reason=validator-not-installed route=quality_gates_ci G1 (ledger row: schema)"
    return 0
  fi
}

san_gate() {
  # ASan+UBSan on the host suite, per commit, both legs (booklet 10.8; hub H5).
  cmake --preset "$SAN_PRESET" && cmake --build --preset "$SAN_PRESET" \
    && ctest --preset "$SAN_PRESET" --output-on-failure
}

tsan_gate() {
  if [ "$LEG" != linux ]; then
    echo "SKIP gate=tsan reason=TSan-absent-on-CLANG64 (hub H5) -- the Linux lane owns the race suites (testing T8)"
    return 0
  fi
  cmake --preset "$TSAN_PRESET" && cmake --build --preset "$TSAN_PRESET" \
    && ctest --preset "$TSAN_PRESET" --output-on-failure
}

bench_gate() {
  # Advisory locally, blocking on merge WHERE A SAME-MACHINE BASELINE EXISTS -- bench JSON
  # never gates across machines (optimization P2; quality_gates_ci G4). The reference
  # runner sets CHECK_BENCH_BLOCKING=1.
  echo "GATE-NOT-WIRED gate=bench route=quality_gates_ci G4 + optimization P2 (wire the JSON baseline compare)"
  if [ "${CHECK_BENCH_BLOCKING:-0}" = "1" ]; then return 1; else return 0; fi
}

# ---- fixes (LOCAL ONLY), then the gates ------------------------------------------------

if [ "$FIX" -eq 1 ]; then
  printf '=== applying fixes (local only) ===\n'
  git ls-files '*.c' '*.h' | xargs -r clang-format -i
  # No wholesale `clang-tidy --fix` here: fix-its can change semantics near volatile,
  # atomics, and macro-heavy DSP code. Apply tidy fixes one check at a time, reviewed.
fi

want format && run "format" format_gate
want tidy   && run "tidy"   tidy_gate
want build  && run "build"  build_gate
want unit   && run "unit"   unit_gate
want audits && run "audits" audits_gate
want remark && run "remark" remark_gate
want schema && run "schema" schema_gate
want san    && run "san"    san_gate
want tsan   && run "tsan"   tsan_gate
want bench  && run "bench"  bench_gate

if [ -n "$FAILED" ]; then
  printf '\nFAILED:%s\n' "$FAILED"
  exit 1
fi
printf '\nall gates passed (leg=%s preset=%s)\n' "$LEG" "$PRESET"
