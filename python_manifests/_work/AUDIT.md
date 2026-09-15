# Adversarial audit of the Python manifest set — 2026-08-08

Six independent auditors, read-only, each given a distinct area and instructed that a clean result was
valid and that manufacturing findings to look thorough was a failure. **946 claims checked. 66 defects
found: 7 CRITICAL, 28 MAJOR, 31 MINOR.** Per-file work orders are in `fixes/*.findings.md`; the
cross-file calls are in `fixes/DECISIONS.md`.

The audit was worth running. It found a **fabricated rule code** that would hard-break a reader's
config, a rule wrongly listed as enabled-by-default in a section headed "do not lose", and three
mutually contradictory answers to the single most consequential line in a new `pyproject.toml`.

## Coverage by area

| auditor | claims checked | findings |
|---|---|---|
| rule codes and tool flags | 255 | the two config-breaking CRITICALs, plus the measurement-based refutations |
| versions, PEP status, APIs | 183 | pulled `peps.python.org/api/peps.json` for ~90 PEP statuses in one pass, the python.org release API, and PyPI JSON for 40+ packages |
| cross-file contradictions and ownership | 57 | the floor contradiction, 6 ownership violations, broken section references |
| citations, URLs, SWE vocabulary | 178 | 2 misattributed quotations, 1 element misattribution, 1 tag-mistaken-for-an-id |
| register and structure | 242 | missing template sections, undeclared tag markers, routing-table gaps |
| consumer usability | 31 | the cold-start path could not produce a lint config at all |

## The seven CRITICAL findings

1. **`D216` does not exist.** Asserted in two files as a rule the `numpy` docstring convention disables.
   All three convention disable-lists were also wrong, and the claim that `google` and `pep257` are
   identical is false (they differ in 8 codes). A reader pasting `D216` gets
   `Cause: Unknown rule selector 'D216'` and ruff refuses to start.
2. **`LOG004` listed as default-on** in a table headed *"Already on by default — do not re-add, do not
   lose"*. It was **stabilised** in ruff 0.16.0, which is a different fact from being **added to the
   default set**. A reader trusting the row omits it from `select` and loses the only check for
   `.exception()` called outside an except handler.
3. Same pydocstyle defect repeated in the file that **owns** the rule set, attached directly to the
   copy-paste config block.
4. **Three answers to the minimum Python floor** — testing said 3.11, error-tracing said 3.13+/prefer
   3.14, and the hub declared it OPEN while module-boundaries deferred to the hub, which deferred back.
5. **`target-version = "py314"`** hard-coded with no instruction tying it to the `requires-python`
   floor. Ruff treats it as the *minimum*, so `UP` autofixes emit syntax that is a `SyntaxError` on the
   floor the project publishes.
6. The recommended config **enables `TC001`–`TC003` in exactly the state its own comment forbids** —
   both `runtime-evaluated-*` exemption lists left empty two lines below.
7. The README cold-start reading order **omitted the only file containing a `[tool.ruff]` block**, so an
   agent following it could not produce a lint configuration.

## Independently re-confirmed by me, not just reported

Both measurable CRITICALs, checked directly with `uvx ruff@0.16.2` in this environment:

- `uvx ruff@0.16.2 rule D216` → `error: invalid value 'D216' for '[RULE]'`; control `D215` resolves to
  `overindented-section-underline`. **The fabrication is real.**
- The default resolved rule set contains exactly `LOG001 LOG002 LOG009 LOG014 LOG015`. **No `LOG004`.**

## The most instructive class of defect

Three claims had been asserted **confidently, and tagged `ESTABLISHED` or `MEASURED`, while being
false** — the worst possible combination in a grounding document, because the tag is what tells a reader
how much weight to put on the sentence:

- "A removed rule code in `select` is silently inert." Wrong: redirects **warn and enable the successor
  rule**; fully-removed codes make ruff **refuse to run**. Removed codes are loud.
- "Selecting a preview rule is silently ineffective." Half wrong: selection by **exact code warns**;
  only selection by **prefix** is silent.
- "The formatter-conflict guard rail does not exist." Wrong: it exists, but only in the `ruff format`
  subcommand and only for 2 of 14 documented conflicts — which is a sharper and more useful fact than
  either the original claim or its blanket refutation.

In one of these, an author had explicitly overridden a fact pack that had the documentation right, on
the grounds that "the measurement wins" — but the measurement had been run against the wrong
subcommand. The lesson is not that measurement is unreliable; it is that a measurement must be reported
with what was measured, which is why fixes are now required to name the tool version and the command.

## Two misattributed quotations — the credibility defect

In two places the SWE corpus's own **editorial `what` field** was placed inside quotation marks and
attributed to a named external source: once to **ISO 26262:2018** (the `safe-state` element) and once to
**Kuhn, Hanafee & Allen, *Reactive Design Patterns*** (the `error-kernel` element). Nothing was
invented — the words are the corpus's real text — but quoting a compiler's summary as a standards body's
definition is exactly the failure that would destroy the collection's credibility with a reader who
checks. Fixed by dropping the quotation marks and attributing the gloss to the corpus.

## What the auditors could NOT check — carried forward honestly

- **Print sources.** BCK *SAIP* 4th ed., Meszaros, POSA 2 and 4, Feathers, *Java Concurrency in
  Practice*, Douglass, Evans, Bloch, Kerrisk and Kuhn et al. are not online. Every element attribution
  was verified against the corpus's own `named_in`/`works` records, **not against the books**. A
  systematic error inside the corpus would pass this check invisibly — which is precisely the class the
  `feature-toggle`/`feature-flag` misattribution belongs to, so treat corpus attributions as
  corpus-accurate rather than book-verified.
- **Register auditing did no page loads** by design; factual accuracy in that area rests on the other
  auditors.
- **The usability auditor had no ruff/mypy/pytest on PATH**, so every `MEASURED` claim it encountered
  was checked against docs only. The rule-codes auditor did have `uvx` and did measure.
- A handful of CLI-shaped claims (how ruff's CLI classifies removed rules; one complexity-traversal
  semantic) could not be settled and remain flagged in the files.

## Disposition — the fix round (2026-08-08)

Nine fixers, each owning distinct files, all bound to `fixes/DECISIONS.md`. **All 66 findings
dispositioned. 103 claims verified by running the tool.** Fixers were explicitly instructed that a
well-evidenced refusal beat a compliant error, and they used it **24 times** — refuting or qualifying a
prescription with a primary source rather than applying it. A selection, because these are the round's
most valuable outputs:

- **A fixer corrected this file's own decisions.** `DECISIONS.md` D1 listed group-aware
  `contextlib.suppress` among the constructs 3.13 makes native; it is **3.12**. The erratum is recorded
  in D1 rather than silently patched.
- **The auditor's prescribed replacement URL 404s.** import-linter's 2.13 docs moved to mkdocs-material
  directory URLs, so `/en/v2.13/contract_types.html` does not resolve; the fixer curl-tested it and
  used the path that does.
- **"Fourteen documented formatter conflicts" is fifteen**, and the guard rail also warns on two
  *settings*, not only rules — so the corrected text neither over-claims (as the original did) nor
  under-claims (as the prescription would have).
- **`D420` is a preview rule**, so it is only in the `pep257` disable set under `lint.preview = true` —
  a qualification neither the audit nor the docs-derived list carried.
- **One finding was refuted outright.** The claim that "seam" is undefined in
  `architecture_manifest_default.md` §1 was wrong: it is at line 24 of the Vocabulary section. No edit
  made.
- **PEP 661 really does write `sentinel(name, /, repr=None)`** without the `*`, so the Sources entry
  attributing that signature to the PEP must *not* be "corrected" to match the 3.15 builtins reference.
  Two sources, two spellings, both quoted accurately.
- A fixer found **a defect the audit missed**: the recommended `select` had also dropped the `T10`
  (flake8-debugger) family — a ninth default-on family, not eight.

The corrected `[tool.ruff]` block was then extracted and **run as a real `pyproject.toml`**: it loads
clean, resolves to 708 enabled rules, and the set difference *(413 defaults) − (708 recommended)* is
empty — every default-on code is either selected or in `ignore` with a stated reason. That is the
strongest form of verification available for this kind of artefact, and it is now the standard the
config block is held to.

## Errata in the evidence base — not fixed, deliberately

Two errors were traced back into `facts/r01_platform_baseline.md`, which is a **dated evidence
snapshot**; fixers were correctly forbidden from editing it, so the errors remain there and are
recorded here instead:

- `r01:91` mis-files `os.path.realpath(strict=os.path.ALLOW_MISSING)` under 3.15. It landed in
  **3.13.4** and is documented "Changed in version 3.14". Corrected in the hub.
- `r01:237` carries an unsourced "roughly 1,400 bugfixes" figure for 3.14.0→3.14.7. The ten-month
  interval is right; the count is not supported by the release pages. Corrected in the hub.

The pattern is worth naming: both errors survived research *and* authoring, and were caught only by an
adversarial reader. Fact packs are evidence, not scripture.

## Standing lesson for the next pass

The two config-breaking CRITICALs were both **tool-behaviour claims taken from documentation prose
rather than from the tool**. Where a claim is about what a tool does, and the tool can be run, run it —
and record the version and the command alongside the result. That is now house rule material, not just
this pass's advice.
