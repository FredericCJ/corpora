# Audit findings for `python_language_hazards_manifest.md`

7 findings: MAJOR 4, MINOR 3

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MAJOR] around line 862

**Quoted text being challenged:**

> | A removed rule code (`TRY200`, `PGH001`, `PGH002`, `PT004`) in `select` | an enforced rule | inert configuration | nothing flags a dead code in a config file.

**What is actually true:**

The 'silently ineffective' table row is false for every code it names. Ruff does flag a dead code in a config file. Same claim also asserted at line 245 ("listing a removed code in `select` is silently inert — nothing flags a dead code") and line 1045 ("a removed or preview-gated code in `select` — silently inert").

**Source the auditor checked:**

Live measurement, ruff 0.16.2 — TRY200/PGH001/PGH002 each emit `warning: `X` has been remapped to `Y`` and enable Y; PT004 aborts with `Rule `PT004` was removed and cannot be selected`.

**Prescribed fix:**

Replace the row's outcome/note with: "a *redirect* (`TRY200`→`B904`, `PGH001`→`S307`, `PGH002`→`G010`): ruff warns and enables the successor rule; a *fully removed* code (`PT004`) makes ruff exit with a configuration error. MEASURED (0.16.2)." Correct lines 245 and 1045 to match.

---

## 2. [MAJOR] around line 442

**Quoted text being challenged:**

> pylint **W4701**/**W4702**/**W4703** `modified-iterating-list`/`-dict`/`-set` `[?]`

**What is actually true:**

The dict and set variants are ERROR-category messages E4702 and E4703, not W4702/W4703. W4702 and W4703 do not exist in pylint 4.0.6 — putting them in `enable=`/`disable=` yields a bad-option-value and the check is not configured as intended. The file's own Sources block (lines 1282-1283) claims these symbolic names were "confirmed" on that page, so the false code is laundered as verified; the underlying pack `_work/facts/r11_language_hazards.md:152`,`:458`,`:933` carries the same error.

**Source the auditor checked:**

pylint 4.0.6 message index — https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html : `modified-iterating-list / W4701`, `modified-iterating-dict / E4702`, `modified-iterating-set / E4703`.

**Prescribed fix:**

Change to `pylint **W4701**/**E4702**/**E4703** `modified-iterating-list`/`-dict`/`-set``, and correct the code list at lines 1282-1283 (W4701, E4702, E4703). Note in passing that the dict/set variants are `E`, i.e. pylint treats them as errors, not warnings.

---

## 3. [MAJOR] around line 150

**Quoted text being challenged:**

> Eighteen codes were simultaneously *removed* from the default set:

```
E401  E402  E701  E702  E703  E711  E712  E713  E714  E721  E731  E741  E742  E743
F403  F405  F406  F722
```

**What is actually true:**

This is a full parallel treatment of content this same file's deferral block cedes: line 30-31 says "**Rule-family config, suppression hygiene, idiom catalogue → `python_linting_practices_manifest.md`**", and PLAN.md says hazards "does **not** enumerate lint config (that is the linting manifest) — it cites the rule code and moves on." python_linting_practices_manifest.md already owns every piece §1.1 reproduces: the identical 18-code list (§2.2, lines 131-139), select-replaces/extend-select-adds (§2.3, lines 141-149), the 413-rule prefix distribution verbatim (§2.3, lines 152-158), and the preview-cannot-be-selected trap (§2.5, lines 178-190). Two ruff bumps from now these enumerations will disagree and nothing marks which is stale.

**Source the auditor checked:**

python_linting_practices_manifest.md:106-201 (§2.1–§2.5); python_language_hazards_manifest.md:30-31 (its own deferral block); _work/PLAN.md scope-boundaries section

**Prescribed fix:**

Cut hazards §1.1 to the routing fact only: "ruff 0.16.0 replaced a 59-rule implicit default with a 413-rule one and dropped 18 codes, two of which (`E711`, `E712`) are the enforcement route for the identity hazard in §4. `lint.select` replaces the default set. The list, the prefix distribution and the preview-selection trap are owned by `python_linting_practices_manifest.md` §2.1–§2.5." Delete the 18-code block, the prefix distribution, and the "rules an agent will assume are on" list from hazards.

---

## 4. [MAJOR] around line 50

**Quoted text being challenged:**

> | Import Linter | **2.3** | only the `/en/v2.3/` docs URL resolves; `latest` and `stable` returned HTTP 404 | VERSION-DEPENDENT (2.3) |

**What is actually true:**

import-linter's latest release is 2.13 (2026-07-03), with 2.12, 2.11, 2.10, 2.9 and 2.8 preceding it — the file's pin is ten releases stale, and both sibling files agree on 2.13 (python_module_boundaries_manifest.md line 673, python_quality_gates_manifest.md ledger row 12 and tool table). The 404 on `latest`/`stable` was read as evidence for 2.3 rather than as a docs-hosting artefact. The consumer damage is concrete: hazards repeats the 2.3 pin at line 580 ("Import Linter **2.3** contracts `type = layers` ...") and cites `https://import-linter.readthedocs.io/en/v2.3/contract_types.html` at line 1301, while module_boundaries §7.3 documents surface that post-dates it — the `import-linter lint` group-command alias is stated there as "added in 2.10", and `exclude_type_checking_imports` / `--cache-dir` are described for 2.13. An agent that pins `import-linter==2.3` from the hazards table gets a tool whose documented CLI in the owning file does not exist.

**Source the auditor checked:**

https://pypi.org/pypi/import-linter/json — latest 2.13, released 3 July 2026; releases 2.8-2.13 all post-date 2.3. Fetched 8 Aug 2026. Cross-read against python_module_boundaries_manifest.md:673, 700-706 and python_quality_gates_manifest.md ledger row 12

**Prescribed fix:**

Change line 50 to `| Import Linter | **2.13** (2026-07-03) | version from PyPI; `latest`/`stable` docs URLs 404, so cite the versioned path `/en/v2.13/` | VERSION-DEPENDENT (2.13) |`, and update lines 580 and 1300-1301 to 2.13 with the `/en/v2.13/contract_types.html` URL.

---

## 5. [MINOR] around line 248

**Quoted text being challenged:**

> Of the `RUF` family only `RUF006`, `RUF008`, `RUF009`, `RUF012`, `RUF018`, `RUF028`, `RUF100`, `RUF101`, `RUF102`, `RUF103`, `RUF104` appear below, each verified on its own page or by measurement.

**What is actually true:**

RUF015 also appears in the file (line 930, the unsafe-fix demonstration, and line 1311 in Measurements), so the enumeration is incomplete — as is the matching Open Question 11 at lines 1123-1124 ("the verified eleven"). The code itself is genuine and the §16.2 use is MEASURED, so this is a bookkeeping slip rather than a laundered code — but the enumeration is precisely the mechanism the file offers as its quarantine guarantee, so it should be exact. (The actually-quarantined name `mutable-frozen-dataclass` is correctly absent from all 13 files — confirmed.)

**Source the auditor checked:**

Internal: `grep -n 'RUF015' python_language_hazards_manifest.md` → lines 930 and 1311. RUF015 = unnecessary-iterable-allocation-for-first-element, stable since v0.0.278, default-on (verified on https://docs.astral.sh/ruff/rules/ and in the 413-code default set).

**Prescribed fix:**

Add `RUF015` to both lists: line 248-249 → "...`RUF012`, `RUF015`, `RUF018`, `RUF028`, `RUF100`–`RUF104`..."; line 1123-1124 → "beyond the verified twelve" with RUF015 included.

---

## 6. [MINOR] around line 128

**Quoted text being challenged:**

> Read a hazard class here, take its codes, and the `select` list writes itself with a traceable reason per entry. Reviewing a lint config then reduces to two questions: **does every enabled rule trace to a hazard row?** and **does every hazard row trace to a rule, a construct, a test, or an explicit `contract-only`?**

**What is actually true:**

The second question holds — all 103 hazard rows in §2–§14 carry a populated route column. The first does not hold against the collection's own recommended config. python_linting_practices_manifest.md §4.3 (L349–L356) recommends 34 `select` entries; ten of them have no code named anywhere in the hazards file: `UP`, `C4`, `LOG`, `FLY`, `ICN`, `INP`, `PIE`, `RSE`, `SLF`, `PYI` (verified by `grep -oE '\b(UP|C4|LOG|FLY|ICN|INP|PIE|RSE|SLF|PYI)[0-9]+\b'` → 0 hits each). For five of those the linting file's own §3.2 verdict reason is not a hazard at all but a noise judgement — L257: `| \`ICN\`,\`INP\`,\`PIE\`,\`RSE\`,\`SLF\`,\`TID\` | **enable** | small and low-noise` — and `FLY`'s reason concedes 'The individual codes were not verified this session'. `LOG` does trace, but to logging_observability_manifest.md §12a (11 LOG codes), not to a hazard row, which §0.3's test as written does not allow for. So an agent applying §0.3's stated review rule to the collection's own recommended select list would flag a third of it, or strip those families.

**Source the auditor checked:**

E:/dev/corpora/manifests/python_linting_practices_manifest.md L349-356 (the recommended select list) and L257 (§3.2 verdict row); E:/dev/corpora/manifests/python_language_hazards_manifest.md L124-131 (§0.3); per-family code grep across all 11 ground-truth files

**Prescribed fix:**

Weaken §0.3's first question to admit the two legitimate escapes, e.g. replace 'does every enabled rule trace to a hazard row?' with 'does every enabled rule trace to a hazard row here, to a hazard row in the sibling that owns the topic (`LOG` → `logging_observability_manifest.md` §12a, `PT` → `python_testing_tooling_manifest.md`, `D` → §15 of the linting file), or to an explicitly-recorded noise/consistency judgement in `python_linting_practices_manifest.md` §3.2?' — and add one clarifying sentence: 'Ten of the 34 families in that file's recommended `select` (UP, C4, LOG, FLY, ICN, INP, PIE, RSE, SLF, PYI) are enabled on consistency or low-noise grounds rather than against a hazard row here; that is a recorded judgement, not a derivation.'

---

## 7. [MINOR] around line 1001

**Quoted text being challenged:**

> The hazard tables in §2–§14 carry **103 routed hazard rows**.

**What is actually true:**

There are exactly 103 rows in the five-column hazard tables of §2–§14, and the by-route tallies that follow are exactly right — I recounted them mechanically and got lint-catchable 43, contract-only 29, type-catchable 13, feature-eliminated 9, test-catchable 8, runtime-catchable 3, fitness-function 2, summing to 107, matching the file's stated 'a row naming a primary route and a backstop counts in both, so these sum to 107' verbatim. (§15's '14 silently-ineffective constructs' and §18's '27 prohibition/replacement pairs' also verify exactly.) But one of the 103 is not routed: the last row of §7.2 at L509, 'Integer floor-division semantics for negative operands', carries `**OPEN — not verified**` in the route column, with 'the numeric-operations table in `library/stdtypes.html` was not loaded this session'. So 102 rows are routed and one is honestly unrouted — which is why the seven route counts sum over only 102 rows, not 103. The file itself sets this standard at L96: 'An unrouted hazard is a defect in this file.'

**Source the auditor checked:**

E:/dev/corpora/manifests/python_language_hazards_manifest.md L999-1006 (§19 tallies) vs L509 (the OPEN row); mechanical recount of all rows in §2–§14

**Prescribed fix:**

Change to: 'The hazard tables in §2–§14 carry **103 hazard rows, 102 of them routed** (the exception is the floor-division row in §7.2, held OPEN pending a primary page — §ac open questions).'

---
