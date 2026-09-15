# audio-rt-ground

A layered knowledge and reference database for **coding agents** implementing real-time audio
processing in C17 on **Linux and Windows NT (one codebase)** with the **clang/LLVM** toolchain —
**MSYS2 CLANG64** on Windows. Sibling of the house `python-agent-ground` package and built to the
same operating model: a ~3k-token entry point, one task card at a time, reference sections loaded
only as named, config artifacts copied rather than re-derived.

**The organizing doctrine is testability + traceability as the agent's feedback loop.** Error
traces, logs, and test reports are designed to tell a coding agent exactly *what* failed, *where*,
and *how* — stable test/contract ids, a frozen machine-parseable check-failure line, a
schema-versioned session report, xrun autopsies, registry-controlled error codes and event ids —
so the failure→patch loop closes from artifacts alone.

## Layout

| path | contents |
|---|---|
| `AGENTS.md` | entry point: twenty non-negotiables, tag protocol, routes, task router |
| `cards/` | 13 task cards (~2k tokens each) — load exactly one |
| `reference/` | 13 manifests — the hub (versions), build, RT rules, channels, adapters, testing, error tracing, observability, memory, kernels, optimization, gates, booklet map |
| `config/` | copy-verbatim artifacts: CMake toolchains + presets, check.sh, CI example, clang-format/tidy, RT poison header, session-report JSON schema, audit scripts |
| `adapters/claude-code/` | SKILL.md for the Claude Code harness |
| `INDEX.json` | machine-greppable section index — query it, never load it |
| `_work/` | build plan, audit gate, resume state |

## Provenance

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root),
itself a specialization of the house embedded-C parent booklet. This package operationalizes the
booklet and pins the version-dependent facts the booklet refuses to carry — it **is** the
`audio_manifests/` version-hub family the booklet's §16.3 declares. Facts verified 2026-08-12 on
the reference machine (i9-12900K hybrid, Windows 11, MSYS2 CLANG64 clang 22.1.8); the hub's §H9
lists re-check triggers. Machine-checked by `_work/audit.py` (section ids, cross-references,
required files, tag presence, schema validity, booklet references).
