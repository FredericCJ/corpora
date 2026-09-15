---
name: python-ground
description: Grounding for writing, reviewing, testing, diagnosing and shipping Python that must be testable, diagnosable, maintainable and modular. Use when writing or changing Python code, reviewing a Python diff, scaffolding a Python project or pyproject.toml, choosing tool or lint configuration, designing error handling or validation, adding logging or telemetry, writing tests, debugging a hung/crashed/leaking/slow process, adding concurrency (asyncio, threads, processes), enforcing module boundaries, setting up CI or quality gates, or writing a design spec. Also use when asked what Python version to target or which type checker to pin.
---

# Python Ground

Layered grounding for Python engineering. **Load progressively — never the whole package** (it is
~430k tokens; you need about 6k).

Set `$PKG` to wherever the package is vendored — typically `.agent/python-ground/`. If you cannot find
it, look for a directory containing `AGENTS.md` alongside `cards/` and `reference/`.

## Step 1 — always

Read **`$PKG/AGENTS.md`** (~3k tokens). It carries the twenty non-negotiables, the epistemic tag
protocol, the enforcement-route vocabulary and the task router.

## Step 2 — load exactly one card

From `$PKG/cards/`, matched to the task:

| task | card |
|---|---|
| writing or changing Python | `write-code.md` |
| reviewing a diff, or final-checking your own work | `review-code.md` |
| new project, `pyproject.toml`, version/tool choices | `start-project.md` |
| adding/splitting a module, packaging, deprecating a public name | `module-boundaries.md` |
| tests | `write-tests.md` |
| error handling, exceptions, validation | `handle-errors.md` |
| logging, metrics, traces | `observability.md` |
| a hung, crashed, leaking or slow **running** process | `diagnose-runtime.md` |
| `asyncio`, threads, processes, subinterpreters | `concurrency.md` |
| CI, lint, type-check, coverage gates | `gates-and-ci.md` |
| writing a spec before implementing | `write-spec.md` |

If two apply, load the one matching what you are about to *do*, not what the code is *about*. Finishing
a code change always ends with `review-code.md`.

## Step 3 — reference sections, only as named

Cards name sections (`hazards §16.1`, `gates §4`). Open **that section**, not the file:

```sh
grep -n '^## \|^### ' $PKG/reference/python_language_hazards_manifest.md   # find the line
sed -n '868,918p'      $PKG/reference/python_language_hazards_manifest.md   # read the slice
```

`$PKG/INDEX.json` maps all 647 sections (`jq`/`grep` it; do not read it).

## Step 4 — config, copied not derived

For any configuration artefact, **copy from `$PKG/config/`**:
`pyproject.toml` (its `[tool.ruff]` block is measured-verified against ruff 0.16.2) ·
`importlinter.toml` · `check.sh` · `pre-commit-config.yaml` · `ci-github.yml`.

Composing a lint config from prose is how a rule code that does not exist ends up in a real project.

## Non-negotiable conduct

- **Never invent an identifier.** A fabricated rule code, flag, version or API name gets pasted into a
  config and silently disables a check. If you cannot verify it, leave it out and say so.
- **Where a claim is about what a tool *does*, run the tool** — `ruff rule <CODE>`,
  `ruff check --isolated --show-settings`. Record the version and the command. Documentation states
  intent; resolved settings are the fact.
- **`OPEN` means decide and say so**, split as **ASSUMED** (you took a stated default) or
  **NEEDS-INPUT** (you need the owner). Never resolve one silently.
- **Version facts route to the hub** (`reference/python_platform_baseline_manifest.md`). If any file
  disagrees with the hub about a version, the hub wins and that file is stale.
- These are **grounding, not rules**. Cite one when it shapes a decision; reason past it when the
  situation genuinely differs — and say which you did.

## Facts expire

Verified **2026-08-08**. The hub's §8 lists its own re-verification triggers, several of which fall
within weeks of that date. If today is materially later, say so before presenting a version fact as
current.
