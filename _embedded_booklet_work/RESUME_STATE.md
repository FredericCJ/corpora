# Embedded C parent booklet — endeavour state

**Status: SEALED r1.5, 2026-08-12.** Written 2026-08-11 (r1.0), then hardened through a
five-iteration convergence program, one commit per revision (`94b20fe` r1.0 → `72a844d` r1.1 →
`71e6c81` r1.2 → `534419e` r1.3 → `dba2629` r1.4 → `ecff19b` r1.5).

## Deliverables

- `E:\dev\corpora\embedded-c-architecture-and-design-r1.md` — the booklet (~150 KB, 16 chapters,
  25 invariants, 63 subsections). Revision history inside §16.4.
- `embedded-c-architecture-and-design-r1.html` — house-styled rendering; regenerate with
  `python _embedded_booklet_work/build_html.py` after any .md edit.
- `_embedded_booklet_work/audit.py` — **the seal gate**. Verifies every backticked element id
  against `SWE/explorer/data/elements.json`, all 80 lineage work ids + verification stances
  against `corpus.json`, every §/chapter/invariant cross-reference, and the structural counts.
  Run before any future commit of the booklet; CLEAN required.
- `_embedded_booklet_work/reviews/r1.2_adjudication.md` — full adjudication record: 33 findings
  (3 critical) from three scoped adversarial reviewers, + 12 findings from the r1.5 cold read.
  All 45 accepted, none rejected; dissent/survivals recorded.

## The five iterations (what each lens was)

1. **r1.1 ground truth, mechanized** — built audit.py; fixed a truncated element id, a wrong
   POSA3 verification stance, the backtick overclaim.
2. **r1.2 adversarial technical** — 3 scoped refutation reviewers; criticals: SPSC
   visibility/publication-ordering, volatile/barrier completion partition, opaque-storage
   effective-type UB (now carries its discharges).
3. **r1.3 coverage** — §3.8 documentation views, §4.6 composition root, §6.4 idle architecture,
   §7.4 second master, §11.5 security posture; invariant 25.
4. **r1.4 coherence** — terminology (activity vs task), §3.2 priced list, dense passages split.
5. **r1.5 cold read** — fresh-eyes architect, 12 findings: integer-determinism condition,
   bring-up order rewrite (watchdog-first, march-before-RAM-lives, harvest-first), register
   reconciliation, firmware identity, §10.7 arithmetic contract, bootloader recursion.
   Verdict pre-fix: "would adopt; would not seal as-is", 8/10.

## Re-verification queue (flagged UNVERIFIED in §16.2, per corpus records)

`hanmer` · `nygard` · `posa2` · `posa3` · `dsimonprimer` · `pont` · `labrosse` · `freertosbook`
· `memfaultea` · `sakscolumns` · `eideregehr` · `preschernplop` · `lakoslsc` · `dreppermem`.

## If resuming / extending

Next moves: (a) spawn `embedded_manifests/` children per ch. 15's pin table (platform version
hub first); (b) re-verify the UNVERIFIED queue → r1.6 or r2; (c) explorer view indexing the
booklet's element usage. Edit the .md → run audit.py → run build_html.py → commit.
