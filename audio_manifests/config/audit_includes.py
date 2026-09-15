#!/usr/bin/env python3
"""audio-rt-ground include audit -- the build-catchable half of invariant 8.

Enforces the include arrows of the booklet (realtime-audio-pc-architecture-and-design-r1.md
section 15.3): core sees core+ports only; adapters see ports plus their own subtree; nothing
includes an adapter except the composition root (shell). Also polices OS-header freedom of
core/ports and OS-conditional confinement (booklet section 5.5) so the two structural-audit
rows of reference/quality_gates_ci_manifest.md section G3 ride in one script.

Stdlib-only. Textual audit: it reads `#include` and `#if*` lines, it does not preprocess.
A construct hidden behind an exotic macro escapes it -- that residue is registered
contract-only in reference/rt_plane_rules_manifest.md section R8.

Usage:
    python audit_includes.py <repo-root>
    python audit_includes.py <repo-root> --list-rules

Exit codes:
    0  clean
    1  at least one VIOLATION
    2  usage or configuration error (bad root, no known zone directory found)

Output grammar (machine-parseable; one line per finding; paths repo-relative, POSIX slashes;
documented with examples in reference/quality_gates_ci_manifest.md section G9):
    <path>:<line>: VIOLATION [INC-0x] <detail>
    include-audit: files=<n> violations=<m>
Grammar regex:
    ^(?P<file>[^:]+):(?P<line>[0-9]+): VIOLATION \\[(?P<rule>INC-[0-9]{2})\\] (?P<detail>.*)$

Rules:
    INC-01  quoted include crosses a zone boundary the ALLOW table forbids
            (includes parent-relative `..` includes, which defeat the audit)
    INC-02  OS header included from an OS-free zone (core, ports)
    INC-03  adapter includes a sibling adapter subtree (legs never cross)
    INC-04  banned C-runtime facility header in core/ports (stdio/locale/threads --
            reference/rt_plane_rules_manifest.md section R2; config/rt_prelude_poison.h)
    INC-05  OS/compiler conditional-compilation token in core/ports
            (confinement per booklet section 5.5; only the compiler port is exempt)

The tables below are DATA -- edit them when the project tree differs, and record every edit
per reference/quality_gates_ci_manifest.md section G8 (the ratchet: never silently loosen).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---- project pins (DECIDE rows; keep in sync with quality_gates_ci G3/G9) ------------------

# Top-level zone directories walked and policed. DECIDE: match your tree.
ZONES = ("core", "ports", "adapters", "shell", "tools", "test")

# Quoted-include permission table: includer zone -> target zones it may name.
ALLOW = {
    "core": {"core", "ports"},
    "ports": {"ports"},
    "adapters": {"adapters", "ports"},  # own subtree only -- INC-03 refines
    "shell": {"shell", "core", "ports", "adapters"},  # the composition root wires everything
    "tools": {"tools", "core", "ports", "shell"},
    # DECIDE: test sees adapters so the port-contract suites
    # (reference/testing_verification_manifest.md section T6) can instantiate the real
    # adapter under test. Drop "adapters" here if your suites go through shell factories.
    "test": {"test", "core", "ports", "adapters", "shell"},
}

# The compiler port may hold compiler conditionals (booklet section 5.6). DECIDE: its path.
COMPILER_PORT_EXEMPT = {"ports/compiler_port.h"}

SOURCE_SUFFIXES = {".c", ".h"}

# OS headers that must never appear in core/ports (INC-02): exact names, then prefixes.
# Extend freely -- additions only tighten (G8).
OS_HEADERS = {
    "windows.h", "winbase.h", "synchapi.h", "processthreadsapi.h", "memoryapi.h",
    "mmdeviceapi.h", "audioclient.h", "avrt.h", "mmsystem.h", "winsock2.h", "objbase.h",
    "unistd.h", "fcntl.h", "sched.h", "pthread.h", "semaphore.h", "poll.h", "dlfcn.h",
}
OS_HEADER_PREFIXES = ("sys/", "linux/", "asm/", "alsa/", "netinet/", "arpa/")

# C-runtime facility headers banned in core/ports (INC-04): the poison-prelude families
# (allocation/stdio/locale/formatting, booklet section 15.2) at include granularity.
# malloc/free ride in <stdlib.h>, which core legitimately needs for other symbols; the
# poison prelude (config/rt_prelude_poison.h) owns symbol-level bans there.
BANNED_FACILITY_HEADERS = {"stdio.h", "locale.h", "threads.h"}

INCLUDE_RE = re.compile(r'^\s*#\s*include\s*([<"])\s*([^">]+?)\s*[">]')
COND_RE = re.compile(r"^\s*#\s*(?:if|ifdef|ifndef|elif)\b")
OS_TOKEN_RE = re.compile(
    r"\b(_WIN32|_WIN64|__linux__|__gnu_linux__|__unix__|__unix|__CYGWIN__"
    r"|__MINGW32__|__MINGW64__|__APPLE__|_MSC_VER)\b"
)

RULES_TEXT = __doc__.split("Rules:", 1)[1].split("The tables below", 1)[0]


def zone_of_include(inc: str) -> str | None:
    """First path segment of a quoted include if it names a known zone, else None."""
    first = inc.split("/", 1)[0]
    return first if first in ZONES else None


def adapter_sub(path_parts: tuple[str, ...] | list[str]) -> str | None:
    """adapters/<sub>/... -> <sub>; None when there is no subtree segment."""
    return path_parts[1] if len(path_parts) > 1 else None


def audit_file(root: Path, rel: Path, violations: list[str]) -> None:
    zone = rel.parts[0]
    rel_posix = rel.as_posix()
    exempt_cond = rel_posix in COMPILER_PORT_EXEMPT
    text = (root / rel).read_text(encoding="utf-8", errors="replace")

    for lineno, line in enumerate(text.splitlines(), start=1):

        def emit(rule: str, detail: str) -> None:
            violations.append(f"{rel_posix}:{lineno}: VIOLATION [{rule}] {detail}")

        m = INCLUDE_RE.match(line)
        if m:
            quote, inc = m.group(1), m.group(2)
            # INC-02 / INC-04: OS-free and facility-free zones, either quote style.
            if zone in ("core", "ports"):
                if inc in OS_HEADERS or inc.startswith(OS_HEADER_PREFIXES):
                    emit("INC-02", f"OS header {quote}{inc}> in OS-free zone '{zone}' "
                                   f"(invariant 8; symbol audit is the link-time twin)")
                elif inc in BANNED_FACILITY_HEADERS:
                    emit("INC-04", f"banned facility header {quote}{inc}> in zone '{zone}' "
                                   f"(rt_plane_rules R2; config/rt_prelude_poison.h)")
            if quote == '"':
                if ".." in inc.split("/"):
                    emit("INC-01", f'parent-relative include "{inc}" defeats the audit -- '
                                   f"include repo-root-relative or same-dir only")
                else:
                    target = zone_of_include(inc)
                    if target is not None:
                        allowed = ALLOW[zone]
                        if target not in allowed:
                            emit("INC-01", f'include "{inc}" -> zone \'{target}\' not allowed '
                                           f"from zone '{zone}' (allowed: "
                                           f"{', '.join(sorted(allowed))})")
                        elif zone == "adapters" and target == "adapters":
                            mine = adapter_sub(rel.parts)
                            theirs = adapter_sub(inc.split("/"))
                            if mine != theirs:
                                emit("INC-03", f"adapter '{mine}' includes sibling adapter "
                                               f"'{theirs}' -- adapter subtrees never cross")

        if (zone in ("core", "ports")) and not exempt_cond and COND_RE.match(line):
            tok = OS_TOKEN_RE.search(line)
            if tok:
                emit("INC-05", f"OS/compiler conditional token '{tok.group(1)}' in zone "
                               f"'{zone}' (confinement: adapters/shell only; "
                               f"compiler port exempt)")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="audio-rt-ground include audit (invariant 8)")
    ap.add_argument("root", help="repository root (the directory holding the zone dirs)")
    ap.add_argument("--list-rules", action="store_true", help="print the rule table and exit")
    args = ap.parse_args(argv)

    if args.list_rules:
        print("include-audit rules:" + RULES_TEXT.rstrip())
        return 0

    root = Path(args.root)
    if not root.is_dir():
        print(f"include-audit: ERROR root '{args.root}' is not a directory", file=sys.stderr)
        return 2

    zone_dirs = [z for z in ZONES if (root / z).is_dir()]
    if not zone_dirs:
        print(f"include-audit: ERROR no known zone directory under '{args.root}' "
              f"(expected any of: {', '.join(ZONES)}) -- edit ZONES in this script",
              file=sys.stderr)
        return 2

    violations: list[str] = []
    files = 0
    for zone in zone_dirs:
        for path in sorted((root / zone).rglob("*")):
            if path.suffix in SOURCE_SUFFIXES and path.is_file():
                files += 1
                audit_file(root, path.relative_to(root), violations)

    for v in violations:
        print(v)
    print(f"include-audit: files={files} violations={len(violations)}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
