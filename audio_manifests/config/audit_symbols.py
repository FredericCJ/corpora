#!/usr/bin/env python3
"""audio-rt-ground symbol audit -- the link-time half of invariant 8.

Runs llvm-nm over the linked core static library and asserts its undefined-symbol set is
inside a reviewed allowlist: C-runtime math/memory primitives, compiler-runtime helpers,
and the port symbols -- no OS import passes (booklet
realtime-audio-pc-architecture-and-design-r1.md section 15.3). llvm-nm presence and object
listing: MEASURED 2026-08-12 (llvm 22.1.8, CLANG64). Stdlib-only apart from llvm-nm itself.

Usage:
    python audit_symbols.py <static-lib> <allowlist> [--nm PATH]
    python audit_symbols.py <static-lib> --print-undefined     # bootstrap: dump the raw set
Environment: LLVM_NM overrides the nm binary (default "llvm-nm" on PATH); --nm wins over both.

Allowlist grammar (one entry per line):
    memcpy          exact undefined-symbol name
    art_port_*      trailing-star prefix glob -- the ONLY glob form supported
    # comment       full-line comments; text after ' #' on an entry line is stripped
    Blank lines ignored. Entries match raw nm names: x86_64 ELF and x86_64 COFF both carry
    undecorated C names, so one allowlist serves both legs [CC-FACT -- if your first
    Windows run shows decorated names, the audit output itself is the correction].

Only type 'U' (undefined) symbols are audited. Weak-undefined ('w'/'v') symbols bind to
null when absent and are ignored here; if one appears, review it by hand.

Bootstrap ritual (reference/quality_gates_ci_manifest.md section G9): build the core lib,
run --print-undefined, review EVERY symbol against rt_plane_rules section R7 and
invariant 8, commit the reviewed allowlist. Never seed the allowlist from output unread.

Exit codes:
    0  clean (or --print-undefined dump completed)
    1  at least one VIOLATION
    2  usage/environment error (lib/allowlist missing or malformed, llvm-nm not found/failed)

Output grammar (machine-parseable; documented in quality_gates_ci section G9):
    VIOLATION [SYM-01] undefined symbol '<name>' not in allowlist (member: <obj>[ +N more])
    symbol-audit: lib=<lib> undefined=<n> allowlisted=<k> violations=<m>
Grammar regex:
    ^VIOLATION \\[SYM-01\\] undefined symbol '(?P<sym>[^']+)' not in allowlist \\(member: (?P<member>[^)]+)\\)$
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def load_allowlist(path: Path) -> tuple[set[str], list[str]]:
    """Return (exact names, prefix globs). Exit-worthy errors raise SystemExit(2)."""
    exact: set[str] = set()
    prefixes: list[str] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        entry = raw.split("#", 1)[0].strip()
        if not entry:
            continue
        if "*" in entry:
            if not entry.endswith("*") or "*" in entry[:-1]:
                print(f"symbol-audit: ERROR {path.as_posix()}:{lineno}: bad glob '{entry}' "
                      f"(only a single trailing '*' is supported)", file=sys.stderr)
                raise SystemExit(2)
            prefixes.append(entry[:-1])
        else:
            exact.add(entry)
    return exact, prefixes


def run_nm(nm: str, lib: Path) -> str:
    if shutil.which(nm) is None:
        print(f"symbol-audit: ERROR nm binary '{nm}' not found on PATH "
              f"(set --nm or LLVM_NM; hub H3 lists the CLANG64 package set)", file=sys.stderr)
        raise SystemExit(2)
    proc = subprocess.run(
        [nm, "--undefined-only", "--format=posix", str(lib)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        print(f"symbol-audit: ERROR nm-failed rc={proc.returncode} lib={lib.as_posix()}",
              file=sys.stderr)
        raise SystemExit(2)
    return proc.stdout


def collect_undefined(nm_output: str) -> dict[str, list[str]]:
    """Map undefined symbol -> archive members referencing it, in first-seen order."""
    undefined: dict[str, list[str]] = {}
    member = "(unknown)"
    for raw in nm_output.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.endswith(":"):  # archive-member header, e.g. "libcore.a[biquad.o]:"
            member = line[:-1]
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "U":
            undefined.setdefault(parts[0], [])
            if member not in undefined[parts[0]]:
                undefined[parts[0]].append(member)
    return undefined


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="audio-rt-ground symbol audit (invariant 8)")
    ap.add_argument("lib", help="static library to audit (the linked core lib)")
    ap.add_argument("allowlist", nargs="?", help="allowlist file (grammar: module docstring)")
    ap.add_argument("--nm", default=os.environ.get("LLVM_NM", "llvm-nm"),
                    help="nm binary (default: $LLVM_NM or 'llvm-nm')")
    ap.add_argument("--print-undefined", action="store_true",
                    help="dump the undefined set and exit 0 (allowlist bootstrap, G9)")
    args = ap.parse_args(argv)

    lib = Path(args.lib)
    if not lib.is_file():
        print(f"symbol-audit: ERROR lib '{args.lib}' not found "
              f"(build the core lib first: ./check.sh build)", file=sys.stderr)
        return 2

    undefined = collect_undefined(run_nm(args.nm, lib))

    if args.print_undefined:
        for sym in sorted(undefined):
            print(f"UNDEF {sym} members={','.join(undefined[sym])}")
        print(f"symbol-audit: lib={lib.as_posix()} undefined={len(undefined)} (dump mode)")
        return 0

    if args.allowlist is None:
        print("symbol-audit: ERROR allowlist argument required unless --print-undefined",
              file=sys.stderr)
        return 2
    allowlist_path = Path(args.allowlist)
    if not allowlist_path.is_file():
        print(f"symbol-audit: ERROR allowlist '{args.allowlist}' not found "
              f"(bootstrap ritual: quality_gates_ci section G9)", file=sys.stderr)
        return 2
    exact, prefixes = load_allowlist(allowlist_path)

    violations = 0
    allowlisted = 0
    for sym in sorted(undefined):
        if sym in exact or any(sym.startswith(p) for p in prefixes):
            allowlisted += 1
            continue
        violations += 1
        members = undefined[sym]
        suffix = f" +{len(members) - 1} more" if len(members) > 1 else ""
        print(f"VIOLATION [SYM-01] undefined symbol '{sym}' not in allowlist "
              f"(member: {members[0]}{suffix})")

    print(f"symbol-audit: lib={lib.as_posix()} undefined={len(undefined)} "
          f"allowlisted={allowlisted} violations={violations}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
