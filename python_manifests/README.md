# python-agent-ground

A redistributable grounding package for building **Python that is testable, diagnosable, maintainable,
modular, and safe to extend incrementally** — shaped so an agent can actually use it.

Drop it into any repo or agent workflow. No runtime, no build, no dependencies: plain Markdown, one JSON
index, and a handful of copy-in config files.

**Agents: start at [`AGENTS.md`](AGENTS.md), not here.**

---

## The problem this shape solves

The underlying reference is ~425k tokens of version-anchored, source-cited ground truth. That is the
right size for a *reference* and an impossible size for *context*. Handing an agent the whole thing
fails; handing it nothing means it invents rule codes.

So the package is layered, and an agent loads only two files to be fully operational:

| layer | file(s) | tokens | loaded |
|---|---|---|---|
| **entry** | `AGENTS.md` | ~2.8k | always |
| **task card** | one of `cards/*.md` | ~2–4k | one per task |
| **reference** | `reference/*.md` | ~425k total | only the *section* a card names |
| **config** | `config/*` | — | copied, not read |
| **index** | `INDEX.json` | 96 KB | `jq`/`grep` only, never read |

**≈4.7k tokens to operate at full competence — 1.1% of the corpus.** Depth stays one hop away and
fully cited, instead of being summarised into something unverifiable.

## Layout

```
AGENTS.md            entry point: 20 non-negotiables, tag protocol, task router
INDEX.json           647 reference sections, machine-queryable
cards/               11 task cards — the layer agents actually read
config/              copy-in artefacts (pyproject, import contracts, check.sh, hooks, CI)
reference/           16 ground-truth manifests — the evidence, with citations and tags
adapters/            wiring for Claude Code, Cursor, Copilot, custom loops
_work/               provenance: research packs, audit record, house rules
```

## Install

Vendor it anywhere (copy, submodule, or package):

```
your-repo/.agent/python-ground/
```

Then add a pointer to whatever your harness always loads — `CLAUDE.md`, `.cursor/rules/`,
`.github/copilot-instructions.md`, or your system prompt:

```markdown
Before writing or reviewing Python, read `.agent/python-ground/AGENTS.md`, then the single card in
`.agent/python-ground/cards/` matching the task. Open only the `reference/` sections a card names.
Copy `config/` artefacts verbatim rather than deriving them.
```

For Claude Code, prefer the skill in `adapters/claude-code/` — it loads on demand instead of occupying
context on every turn. Full per-harness instructions: [`adapters/README.md`](adapters/README.md).

## What is in `cards/`

`write-code` · `review-code` · `start-project` · `module-boundaries` · `write-tests` · `handle-errors` ·
`observability` · `diagnose-runtime` · `concurrency` · `gates-and-ci` · `write-spec`

Each card is: what to do, what to never do, **the decisions you must not invent**, and a table of
pointers into `reference/` for depth. Every rule names what mechanically enforces it — or admits that
nothing does.

## The idea the package is organised around

> Static typing is a good start. A pedantic linter is very nice. A set of coding practices is also nice.
> **A way of enforcing all of it is the point** — advice that isn't mechanically enforced decays to zero.

So every hazard and practice carries an **enforcement route**: `type-catchable` · `lint-catchable` ·
`feature-eliminated` · `test-catchable` · `fitness-function` · `runtime-catchable` · **`contract-only`**.

That last one is load-bearing. Roughly a third of what matters has no mechanical enforcer, and the
package says so rather than implying coverage it does not have.

## Epistemic discipline

Every factual claim in `reference/` is tagged — **ESTABLISHED**, **VERSION-DEPENDENT**, **MEASURED**,
**OPEN**, **FLAGGED-SECONDARY**, **UNVERIFIED**, **CC-FACT** — so a reader knows what weight it bears.
An untagged factual claim is a defect. `OPEN` appears ~490 times, deliberately: those are decisions your
project owns, surfaced rather than guessed.

**Nothing is fabricated.** Where a fact could not be confirmed, the package says so and says what could
not be confirmed. An honest `OPEN` outranks a plausible sentence, because a plausible sentence about a
rule code gets pasted into a config and silently disables a check.

## Verification status

Facts verified **2026-08-08** against primary sources: 2,294 tagged claims, 644 unique source URLs.

An adversarial audit then checked **946 claims** and found **66 defects** — including a **rule code that
does not exist** (`D216`, makes ruff refuse to start) and a rule wrongly listed as enabled-by-default
(`LOG004`). All 66 were dispositioned; **103 claims were verified by running the tool**, and 24 audit
prescriptions were themselves refuted with primary sources. Record: [`_work/AUDIT.md`](_work/AUDIT.md).

That audit produced the package's most portable lesson, now house rule 12: **where a claim is about what
a tool *does*, run the tool** — both config-breaking defects were doc-derived rather than measured.

## Limits, stated plainly

- **Facts expire.** `reference/python_platform_baseline_manifest.md` §8 lists its own re-verification
  triggers, several falling within weeks of the verification date. Re-check the hub before trusting a
  version claim; the rest of the set degrades gracefully behind it.
- **Print sources were not checked against the books.** Pattern attributions trace to a research
  corpus's records, not to the physical volumes — so a systematic error inside that corpus would pass
  invisibly. Treat them as corpus-accurate, not book-verified.
- **The default target is small-to-mid single-process Python.** Where a mechanism's home is distributed
  systems, the manifests say plainly that adopting it at this scale is over-engineering. That restraint
  is content, not a gap.
- **Two `reference/` files are language-agnostic on purpose** (`architecture_manifest_default.md`,
  `software_spec_discipline_manifest.md`): no versions, no tags, no sources. They answer *how to think
  about it*, and retro-fitting the ground-truth template onto them would break them.

## Provenance

`_work/` carries the full trail: `PLAN.md` (scope boundaries and 12 house rules), `RESUME_STATE.md`,
`AUDIT.md` (findings, disposition and errata), `facts/` (1.28 MB of source-anchored research packs),
`seed/` (design-vocabulary mining), and `fixes/` (per-file findings and the cross-file decisions).

Version `2026.08.08`. See `INDEX.json` for the machine-readable manifest of the package.
