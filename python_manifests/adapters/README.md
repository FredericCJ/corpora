# `adapters/` — wiring this package into a harness

The package is harness-neutral: `AGENTS.md` + `cards/` + `reference/` are plain Markdown and work
anywhere. These adapters just make the right layer load at the right time so an agent does not have to
be told twice.

**The one thing every wiring must get right:** load `AGENTS.md` always, load **one** card per task, and
never load a whole `reference/` file. That is the difference between ~6k tokens and ~430k.

## Install

Vendor the directory into the target repo (a copy, a submodule, or a package dependency — the package
has no runtime and no build):

```
your-repo/
├── .agent/python-ground/       ←  this package, wherever you like
│   ├── AGENTS.md
│   ├── cards/
│   ├── config/
│   ├── reference/
│   └── INDEX.json
└── ...
```

Then wire it per harness below. **Pin the version you vendored** (`INDEX.json` → `version`) and re-check
`reference/python_platform_baseline_manifest.md` §8 when you bump it — the version facts expire on a
schedule, and the hub lists its own re-verification triggers.

## Claude Code

Two options; the skill is better because it loads on demand rather than occupying context always.

**As a skill (recommended).** Copy `adapters/claude-code/` to `.claude/skills/python-ground/` and point
its paths at wherever you vendored the package. The skill's description triggers it on Python work; its
body then routes to the one card that fits.

**As always-on context.** Add to your root `CLAUDE.md`:

```markdown
## Python work

Before writing or reviewing Python, read `.agent/python-ground/AGENTS.md` and then the single card in
`.agent/python-ground/cards/` that matches the task. Do not read `reference/` files whole — open only
the section a card names. Copy `config/` artefacts verbatim rather than deriving them.
```

Keep the pointer short. Pasting `AGENTS.md` itself into `CLAUDE.md` costs ~3k tokens on every turn
including ones with no Python in them.

## Cursor / Windsurf

Add a rule file (`.cursor/rules/python-ground.mdc` or the editor's equivalent) with a glob so it only
attaches to Python files:

```markdown
---
description: Python architecture, design and quality grounding
globs: ["**/*.py", "pyproject.toml"]
alwaysApply: false
---
Read `.agent/python-ground/AGENTS.md` first, then the one card in `.agent/python-ground/cards/` matching
the task. Open only the `reference/` sections a card names.
```

## GitHub Copilot

Put the same pointer in `.github/copilot-instructions.md`. Copilot's instruction file is always-on, so
keep it to the pointer and the handful of non-negotiables you most want present — not the whole file.

## Any agent loop / SDK / custom harness

Two integration shapes, depending on whether you have retrieval:

**Without retrieval** — inject `AGENTS.md` into the system prompt, and select a card from the task
router by matching the user's intent. That is a dictionary lookup, not a model call.

**With retrieval** — index `reference/` at **section** granularity. `INDEX.json` already carries all 647
sections with their file, heading and line number:

```sh
# every section title in one file, with line numbers
jq -r '.reference[] | select(.file|test("hazards")) | .sections[] | "\(.line)\t\(.title)"' INDEX.json

# which file owns a pillar
jq -r '.reference[] | select(.pillar=="diagnosable") | .file' INDEX.json

# find the section that mentions a topic, then read just that slice
grep -n 'ExceptionGroup' reference/error_tracing_contract_manifest.md | head
sed -n '380,430p'  reference/error_tracing_contract_manifest.md
```

`INDEX.json` is ~96 KB — a `jq`/`grep` target, never something to read into context.

## Verifying the wiring works

Three checks, in order of what they catch:

1. Ask the agent a question whose answer is in a card and **not** in `AGENTS.md` — e.g. *"what does a
   frozen dataclass wrapping a list actually guarantee?"* If it answers well, card loading works.
2. Ask for a `pyproject.toml`. It should **copy `config/pyproject.toml`**, not compose one from memory.
   Composing from memory is how invented rule codes get in.
3. Ask something the package tags `OPEN` — e.g. *"what should `requires-python` be?"* A correctly wired
   agent gives the default (`>=3.13`), names it as a decision, and says what the alternative forfeits.
   An agent that answers with false confidence has not read the epistemic protocol.

## What not to do

- **Do not concatenate the package into one file.** The layering *is* the feature.
- **Do not summarise `reference/` into the cards.** The cards are pointers plus rules; the references
  hold the evidence, the citations and the tags. Collapsing them loses the provenance that makes any of
  it trustworthy.
- **Do not strip the epistemic tags** when quoting a manifest into another document. An `OPEN` that
  arrives untagged reads as settled, which is precisely the failure the tags exist to prevent.
