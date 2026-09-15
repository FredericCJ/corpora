"""Mechanical audit gate for audio-rt-ground. Run before any commit; CLEAN required.

Checks: required files; dictated section skeletons; every section pointer resolves; tag
presence in reference files; JSON configs parse; booklet references resolve against the
booklet; card required blocks; INDEX.json freshness; no TODO markers.

Usage: python _work/audit.py    Exit 0 = CLEAN (warnings allowed), 1 = findings.
"""
import json
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
ROOT = PKG.parent
BOOKLET = ROOT / "realtime-audio-pc-architecture-and-design-r1.md"

sys.path.insert(0, str(PKG / "_work"))
import build_index  # noqa: E402

findings = []
warnings = []

# ------------------------------------------------------------ expected files
REFERENCE = {
    "audio_platform_baseline_manifest.md": ("H", 9),
    "toolchain_build_manifest.md": ("B", 11),
    "rt_plane_rules_manifest.md": ("R", 8),
    "concurrency_channels_manifest.md": ("C", 9),
    "device_adapter_manifest.md": ("D", 9),
    "testing_verification_manifest.md": ("T", 13),
    "error_tracing_contract_manifest.md": ("E", 10),
    "observability_flightring_manifest.md": ("O", 9),
    "memory_residency_manifest.md": ("M", 8),
    "dsp_kernel_patterns_manifest.md": ("K", 8),
    "optimization_microarch_manifest.md": ("P", 10),
    "quality_gates_ci_manifest.md": ("G", 9),
}
CARDS = [
    "start-project.md", "build-and-flags.md", "write-dsp-kernel.md", "write-rt-code.md",
    "concurrency-channels.md", "device-adapters.md", "write-tests.md", "diagnose-failure.md",
    "handle-errors.md", "observability.md", "optimize-performance.md", "gates-and-ci.md",
    "review-code.md",
]
CONFIG = [
    "toolchain-clang64-windows.cmake", "toolchain-linux-clang.cmake", "CMakePresets.json",
    ".clang-format", ".clang-tidy", "rt_prelude_poison.h", "check.sh", "ci-github.yml",
    "session_report.schema.json", "audit_includes.py", "audit_symbols.py",
]
TOP = ["AGENTS.md", "README.md", "reference/booklet_map.md", "adapters/claude-code/SKILL.md"]

for rel in TOP:
    if not (PKG / rel).exists():
        findings.append(f"FILE missing: {rel}")
for name in REFERENCE:
    if not (PKG / "reference" / name).exists():
        findings.append(f"FILE missing: reference/{name}")
for name in CARDS:
    if not (PKG / "cards" / name).exists():
        findings.append(f"FILE missing: cards/{name}")
for name in CONFIG:
    if not (PKG / "config" / name).exists():
        findings.append(f"FILE missing: config/{name}")

# --------------------------------------------------- section skeletons exact
LETTER_TO_FILE = {}
sections_by_file = {}
for name, (letter, count) in REFERENCE.items():
    p = PKG / "reference" / name
    LETTER_TO_FILE[letter] = name
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    ids = re.findall(r"^## ([A-Z]\d+)\. ", text, re.M)
    sections_by_file[name] = set(ids)
    expected = [f"{letter}{i}" for i in range(1, count + 1)]
    for sid in expected:
        if sid not in ids:
            findings.append(f"SECTION missing: reference/{name} lacks '## {sid}.'")
    for sid in ids:
        if sid not in expected:
            findings.append(f"SECTION unexpected: reference/{name} has '## {sid}.' beyond the dictated map")
    dupes = {s for s in ids if ids.count(s) > 1}
    for d in dupes:
        findings.append(f"SECTION duplicated: reference/{name} '## {d}.'")

# ------------------------------------------------------- pointer resolution
scan_files = []
for rel in TOP:
    if (PKG / rel).exists():
        scan_files.append(PKG / rel)
scan_files += sorted((PKG / "cards").glob("*.md"))
scan_files += [PKG / "reference" / n for n in REFERENCE if (PKG / "reference" / n).exists()]

ptr_pat = re.compile(r"(?:§|\bsection )([A-Z]\d+)\b")
n_ptrs = 0
for f in scan_files:
    text = f.read_text(encoding="utf-8")
    for sid in ptr_pat.findall(text):
        letter = sid[0]
        target = LETTER_TO_FILE.get(letter)
        if target is None:
            continue  # not a package section letter
        n_ptrs += 1
        if target in sections_by_file and sid not in sections_by_file[target]:
            findings.append(
                f"XREF dangling: {f.relative_to(PKG).as_posix()} points at §{sid} "
                f"but reference/{target} has no such section"
            )

# ---------------------------------------------------------------- tag audit
TAGS = ["MEASURED", "CC-FACT", "ESTABLISHED", "VERSION-DEPENDENT", "OPEN",
        "FLAGGED-SECONDARY", "UNVERIFIED"]
for name in REFERENCE:
    p = PKG / "reference" / name
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    n_tags = sum(len(re.findall(r"\[" + t, text)) for t in TAGS)
    if n_tags < 5:
        findings.append(f"TAGS sparse: reference/{name} carries only {n_tags} epistemic tags")

# ------------------------------------------------------------- config parse
for jname in ["CMakePresets.json", "session_report.schema.json"]:
    p = PKG / "config" / jname
    if p.exists():
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            findings.append(f"CONFIG invalid JSON: config/{jname}: {e}")
p = PKG / "config" / "check.sh"
if p.exists() and not p.read_text(encoding="utf-8").startswith("#!"):
    findings.append("CONFIG check.sh lacks a shebang")
p = PKG / "config" / "rt_prelude_poison.h"
if p.exists() and "poison" not in p.read_text(encoding="utf-8"):
    findings.append("CONFIG rt_prelude_poison.h contains no poison pragma")

# -------------------------------------------------------- booklet references
if BOOKLET.exists():
    btext = BOOKLET.read_text(encoding="utf-8")
    b_subsecs = set(re.findall(r"^### (\d+\.\d+)", btext, re.M))
    b_chaps = set(int(m) for m in re.findall(r"^## (\d+)\.", btext, re.M))
    for f in scan_files:
        text = f.read_text(encoding="utf-8")
        for ref in re.findall(r"booklet (?:§|section )(\d+\.\d+)", text):
            if ref not in b_subsecs:
                findings.append(
                    f"BOOKLET dangling: {f.relative_to(PKG).as_posix()} cites booklet §{ref}"
                )
        for ref in re.findall(r"booklet ch(?:apter)?\.? (\d+)", text):
            if int(ref) not in b_chaps:
                findings.append(
                    f"BOOKLET dangling: {f.relative_to(PKG).as_posix()} cites booklet ch. {ref}"
                )
else:
    warnings.append("booklet file not found; booklet references unchecked")

# ------------------------------------------------------------- card blocks
for name in CARDS:
    p = PKG / "cards" / name
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    if "Load when" not in text:
        findings.append(f"CARD missing 'Load when' block: cards/{name}")
    if "Go deeper" not in text:
        findings.append(f"CARD missing 'Go deeper' table: cards/{name}")
    if "Never" not in text:
        warnings.append(f"CARD has no 'Never' list: cards/{name}")

# ----------------------------------------------------------------- markers
for f in scan_files:
    text = f.read_text(encoding="utf-8")
    for marker in ["TODO", "TBD", "FIXME", "XXX"]:
        if re.search(r"\b" + marker + r"\b", text):
            findings.append(f"MARKER {marker} present in {f.relative_to(PKG).as_posix()}")

# ------------------------------------------------------------ INDEX freshness
idx_path = PKG / "INDEX.json"
if idx_path.exists():
    try:
        current = json.loads(idx_path.read_text(encoding="utf-8"))
        fresh = build_index.build(PKG)
        if current.get("sections") != fresh.get("sections"):
            findings.append("INDEX stale: rerun python _work/build_index.py")
    except Exception as e:  # noqa: BLE001
        findings.append(f"INDEX unreadable: {e}")
else:
    findings.append("INDEX.json missing: run python _work/build_index.py")

# ------------------------------------------------------------------- report
print(f"files checked: {len(scan_files)}  section pointers resolved: {n_ptrs}")
for w in warnings:
    print("WARN ", w)
if findings:
    print(f"\n{len(findings)} FINDINGS:")
    for x in findings:
        print("  -", x)
    sys.exit(1)
print("\nCLEAN")
