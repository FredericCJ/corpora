#!/usr/bin/env sh
# One command, three places: editor, pre-commit hook, CI all run THIS.
#
# This file is the local/CI parity contract from reference/python_quality_gates_manifest.md §3.
# The rule it exists to enforce: a gate that only runs in CI teaches people to push and wait, and a
# gate that only runs locally does not exist. If you add a check to CI, add it here instead.
#
# Usage:
#   ./check.sh              run every blocking gate, stop at the first failure
#   ./check.sh --all        run every gate, report all failures, then exit non-zero
#   ./check.sh --fix        apply formatter + safe lint fixes, then run the gates  (LOCAL ONLY)
#   ./check.sh lint types   run only the named gates
#
# NEVER pass --fix in CI. CI reports; humans and hooks fix. (quality_gates anti-patterns)

set -eu

RUN="${RUNNER:-uv run}"   # DECIDE: `uv run`, `poetry run`, `nox -s`, or empty for a bare venv.
                          # Whatever you choose, CI must use the SAME value.

FAILED=""
KEEP_GOING=0
FIX=0
GATES=""

for arg in "$@"; do
  case "$arg" in
    --all) KEEP_GOING=1 ;;
    --fix) FIX=1 ;;
    -*)    echo "unknown flag: $arg" >&2; exit 2 ;;
    *)     GATES="$GATES $arg" ;;
  esac
done
[ -n "$GATES" ] || GATES="format lint types tests boundaries deps"

want() { case " $GATES " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

run() {
  name="$1"; shift
  printf '\n=== %s ===\n' "$name"
  if "$@"; then
    printf '--- %s: ok\n' "$name"
  else
    printf '!!! %s: FAILED\n' "$name"
    FAILED="$FAILED $name"
    [ "$KEEP_GOING" -eq 1 ] || { printf '\nFAILED:%s\n' "$FAILED"; exit 1; }
  fi
}

if [ "$FIX" -eq 1 ]; then
  printf '=== applying fixes (local only) ===\n'
  $RUN ruff format
  # Safe fixes only. NEVER add --unsafe-fixes here: some fixes are marked unsafe by ruff itself and
  # change runtime behaviour where dunder methods are overridden. Apply those one at a time, reviewed.
  $RUN ruff check --fix
fi

# 1. Formatting is not a code-review topic. It either matches or it does not.
want format     && run "format"     sh -c "$RUN ruff format --check ."

# 2. Lint. The rule set is an explicit, committed artefact - see config/pyproject.toml [tool.ruff].
want lint       && run "lint"       sh -c "$RUN ruff check ."

# 3. Types. DECIDE which checker is authoritative and pin it; substitute it here.
want types      && run "types"      sh -c "$RUN mypy src"

# 4. Tests. `-X dev` is NOT optional: with filterwarnings=error alone, ResourceWarning stays filtered
#    and unclosed-resource bugs never surface. Both are required together.
want tests      && run "tests"      sh -c "$RUN python -X dev -m pytest"

# 5. Module boundaries. The contract file, not a convention. config/importlinter.toml
want boundaries && run "boundaries" sh -c "$RUN lint-imports"

# 6. Declared-vs-actual dependencies. Catches the undeclared-import break no internal contract sees.
want deps       && run "deps"       sh -c "$RUN deptry ."

# --- ADVISORY / DIAGNOSTIC, deliberately not part of the default gate set -----------------------
# Coverage is a DIAGNOSTIC, not a target. Report it, read the MISSING lines, do not gate on a number:
#   $RUN python -X dev -m pytest --cov=src --cov-report=term-missing
# Same for mutation score, complexity and docstring coverage - diagnostics only, never blocking.
# See quality_gates §9-§10 for which numbers are defensible as gates and which invite gaming.

if [ -n "$FAILED" ]; then
  printf '\nFAILED:%s\n' "$FAILED"
  exit 1
fi
printf '\nall gates passed\n'
