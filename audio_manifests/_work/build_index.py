"""Build INDEX.json for audio-rt-ground: every section of every .md, greppable, never loaded whole.

Usage: python _work/build_index.py   (from the package root or repo root)
"""
import json
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


def build(pkg: Path) -> dict:
    sections = []
    files = [pkg / "AGENTS.md", pkg / "README.md"]
    files += sorted((pkg / "cards").glob("*.md"))
    files += sorted((pkg / "reference").glob("*.md"))
    files += sorted((pkg / "adapters").rglob("*.md"))
    for f in files:
        rel = f.relative_to(pkg).as_posix()
        text = f.read_text(encoding="utf-8")
        lines = text.split("\n")
        heads = [
            (i + 1, m.group(1), m.group(2).strip())
            for i, ln in enumerate(lines)
            if (m := re.match(r"^(#{1,3}) (.+)$", ln))
        ]
        for idx, (lineno, hashes, title) in enumerate(heads):
            end = heads[idx + 1][0] - 1 if idx + 1 < len(heads) else len(lines)
            body = "\n".join(lines[lineno - 1 : end])
            sid = None
            m = re.match(r"^([A-Z]\d+)\. ", title)
            if m:
                sid = m.group(1)
            sections.append(
                {
                    "file": rel,
                    "id": sid,
                    "level": len(hashes),
                    "title": title,
                    "line": lineno,
                    "approx_tokens": max(1, len(body) // 4),
                }
            )
    return {
        "package": "audio-rt-ground",
        "description": (
            "Knowledge database for coding agents implementing real-time audio in C17 on "
            "Linux/Windows NT, clang/LLVM + MSYS2 CLANG64. Testability and traceability as the "
            "agent feedback loop."
        ),
        "version": "2026.08.12",
        "facts_verified": "2026-08-12",
        "entry_point": "AGENTS.md",
        "how_to_use": [
            "1. Always load AGENTS.md (~3k tokens): non-negotiables, tag protocol, task router.",
            "2. Load the ONE card in cards/ matching the task (~2k tokens).",
            "3. Read a reference/ section only when a card names it. Never a whole file.",
            "4. Copy config/ artifacts verbatim rather than deriving them.",
            "5. Any red artifact: cards/diagnose-failure.md is the dispatch table.",
        ],
        "section_count": len(sections),
        "sections": sections,
    }


def main() -> int:
    index = build(PKG)
    out = PKG / "INDEX.json"
    out.write_text(json.dumps(index, indent=1), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes); sections: {index['section_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
