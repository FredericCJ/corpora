# `config/` — copy these, do not re-derive them

Ready-made artefacts for the baseline the manifests argue for. **Copy them in and edit the marked
decisions.** Deriving a lint config from prose is how a fabricated rule code ends up in a real project.

| file | what it is | provenance |
|---|---|---|
| `pyproject.toml` | project metadata, ruff, checker, pytest, coverage | `[tool.ruff]` is **verbatim and MEASURED**; the rest is a starting point |
| `importlinter.toml` | dependency-direction contracts (+ a `tach` alternative) | **verbatim** from `python_module_boundaries_manifest.md` §7 |
| `check.sh` | the one command the editor, the hook and CI all run | the local/CI parity contract, `python_quality_gates_manifest.md` §3 |
| `pre-commit-config.yaml` | the hook layer | assembled from `quality_gates` §2–§3 |
| `ci-github.yml` | example CI wiring on one platform | illustrative; `check.sh` is the portable artefact |

## What is measured and what is not

**`[tool.ruff]` in `pyproject.toml` is the only block here that was verified by execution.** It was
extracted and run as a real `pyproject.toml` against **ruff 0.16.2**: it loads clean, resolves to **708
enabled rules**, and the set difference *(413 default-on rules) − (708 recommended)* is **empty** — so no
rule that ruff enables by default is silently switched off by the `select` list. That last property is
the one people get wrong, because **`select` replaces the default set rather than adding to it.**

Everything else is a defensible starting point assembled from the manifests. Treat the two differently:
the ruff block should not be "tidied" without re-measuring; the rest is yours to shape.

## Decide these before shipping

Every `DECIDE:` comment marks something the manifests tag `OPEN` — a real choice with consequences, not
a blank to fill. The ones that bite hardest:

1. **The `requires-python` floor.** Default `>=3.13`. It must equal ruff's `target-version`: ruff treats
   that as a **minimum**, so setting it above your floor makes `UP` autofixes emit syntax that is a
   `SyntaxError` on the interpreter you publish for.
2. **Exact tool pins.** `ruff 0.16.0` moved its default rule set from 59 rules to 413 *and dropped 18* —
   including `E711` (`== None`) and `E712` (`== True`) — without recording it as a breaking change.
   Teams that had not pinned found out from a red build. Pin, and upgrade deliberately.
3. **Which checker is authoritative.** One, pinned. A second is advisory at most; cross-checker agreement
   is not an adoptable goal.
4. **The `RUNNER` in `check.sh`.** Whatever you pick, CI must use the same value or parity is a fiction.
5. **The CI interpreter matrix**, which is *not* the same list as `requires-python`.

## Two things deliberately absent

- **No coverage threshold.** Coverage is a diagnostic. Gate on the absence of assertion-free tests and on
  error paths having tests; read the *missing* lines. A percentage is gameable by construction.
- **No `--unsafe-fixes` anywhere.** Some ruff fixes are marked unsafe by ruff itself and can change
  runtime behaviour where dunder methods are overridden. Apply those individually, reviewed — never in
  bulk and never in CI.

## Verify before you trust

These files were assembled 2026-08-08 and tool behaviour drifts. Where a claim here is about what a tool
*does*, re-measure it rather than re-reading the docs — that is house rule 12, and it exists because both
config-breaking defects found in this package's own audit were doc-derived rather than measured:

```sh
ruff --version
ruff check --isolated --show-settings <any.py> | grep -c '^ *- '   # the resolved default set
ruff rule <CODE>                                                  # does this code even exist?
```

The last one is not paranoia. An earlier draft of these manifests asserted a rule code (`D216`) that does
not exist; ruff aborts with `Unknown rule selector` and refuses to start, so a project that pasted it had
no linting at all until someone read the error.
