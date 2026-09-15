# Card: scaffold a new project

**Load when:** creating a new Python project or package, or bringing an existing one up to this
package's baseline.
**Depth:** `reference/python_platform_baseline_manifest.md` (versions), `..._module_boundaries_...`
(layout and packaging), `..._quality_gates_...` (the gate set).

## Do these in order

### 1. Pick the floor, and pick it once

**Default: `requires-python = ">=3.13"`.** Not the newest release — a floor. The reasoning is calendar
and behaviour, not fashion: on 2026-08-08 only 3.13 and 3.14 are in the bugfix phase, and 3.13 makes
native every construct this package's own rules depend on (`@warnings.deprecated`, callable
`split`/`subgroup` on `ExceptionGroup`, `exc_type_str`).

- **`">=3.12"`** is the defensible alternative if you are in the scientific ecosystem (SPEC 0's window).
  It forfeits the three constructs above and needs `typing_extensions` for `@deprecated`.
- **Prefer `">=3.14"`** where nothing forces wider compatibility — it adds the PEP 765 `SyntaxWarning`
  that turns "no `return` in `finally`" from a review item into a compiler-enforced one.
- The floor is tagged **OPEN as a policy**: record which policy produced it, in an ADR. → hub §3d–§3e

**Then: `target-version` in ruff must equal this floor.** It is a minimum, not a target.

### 2. Layout — `src/`, always

```
myapp/
├── pyproject.toml
├── src/myapp/__init__.py        # re-exports, with __all__
│   ├── domain/                  # pure: no I/O, no framework imports
│   ├── ports/                   # Protocols the domain needs
│   ├── services/                # orchestration over ports
│   ├── adapters/                # concrete I/O: db, http, filesystem
│   └── composition.py           # the ONE place adapters are wired to ports
└── tests/                       # no __init__.py; --import-mode=importlib
```

`src/` is not taste. It prevents the class of bug where tests import the working copy instead of the
installed package, so "works locally, fails installed" cannot happen. → boundaries §3

The `domain → ports ← services → adapters` direction is the thing you will enforce mechanically in
step 5. Pick your own names, but pick the direction and write it down.

### 3. `pyproject.toml`

Start from `config/pyproject.toml` in this package. It carries the ruff block **verbatim from the
linting manifest** — that block was run as a real `pyproject.toml` and verified to load clean, resolve
to 708 rules, and leave no default-on rule silently switched off.

Non-obvious fields that change behaviour:
- `requires-python` — step 1. Never a ceiling, only a floor.
- `dependencies` — runtime only. Development tools go in `[dependency-groups]` (PEP 735), **not** in
  optional-dependencies; extras are a consumer-facing feature, not a dev bucket.
- `py.typed` marker in the package if you ship types (PEP 561), or consumers get nothing.
- Lock file is `pylock.toml` (PEP 751) for applications. A library pins nothing.

### 4. The checker

Pick **one** authoritative checker and pin it; a second is advisory at most. Agreement between checkers
is not an adoptable goal — they use different inference and disagree by design.

- Enable `strict`, then add the opt-in error codes that catch real hazards and are **not** in `--strict`:
  `truthy-bool`, `truthy-iterable`, `possibly-undefined`, `exhaustive-match`, `mutable-override`,
  `explicit-override`, `redundant-expr`, `ignore-without-code`, `unused-awaitable`, `deprecated`.
- Know the gaps you are accepting: pyright leaves `reportUninitializedInstanceVariable`,
  `reportImplicitOverride` and `reportUnnecessaryTypeIgnoreComment` at `"none"` in **all four** modes,
  strict included. → typing §1

### 5. Make the boundary real

`__all__` is documentation. The contract is a file a CI job checks. Start from
`config/importlinter.toml`; `lint-imports` fails the build on a violation.

Know the one trap: the `protected` contract type checks **direct** imports only — unlike `layers`,
`forbidden` and `independence`, it does not follow chains, so `a → b → protected` passes.
→ boundaries §7

### 6. The gate set — smallest set that actually holds

Wire these on day one, all runnable locally with one command:

| gate | command |
|---|---|
| format | `ruff format --check` |
| lint | `ruff check` |
| types | your pinned checker, `strict` |
| tests | `pytest` with `filterwarnings = ["error::DeprecationWarning"]` and `-X dev` |
| boundaries | `lint-imports` |
| dependencies | `deptry .` |

`config/pre-commit-config.yaml` and `config/ci-github.yml` are the wiring. The rule that matters
more than the list: **the same command must run in the editor, in the hook and in CI.** A gate that only
exists in CI teaches people to push and wait. → gates §3

### 7. Record the decisions

An ADR for: the floor and the policy behind it, the layer direction, the checker choice and what its
gaps are, and any rule family you deliberately disabled. Everything this package tags `OPEN` is a
decision someone will otherwise re-litigate every month.

## Never

- **Rely on a tool's default rule set.** ruff 0.16.0 moved its default from 59 rules to 413 and dropped
  18 — including the `== None` and `== True` checks. Unpinned tools rewrite your standard for you.
- **Set `target-version` to the newest release.** See step 1.
- **Put dev tools in `optional-dependencies`.**
- **Add a gate as "advisory for now"** with no date and no owner. It will be advisory forever.
- **Start with a flat layout** because it is one directory fewer.

## Decisions you must not invent

The floor and its policy · the layer names and direction · which checker is authoritative · whether
free-threading is a supported configuration, an experiment, or out of scope · whether `assert` ships ·
the CI interpreter matrix (which is **not** the same list as `requires-python`).

## Go deeper

| question | where |
|---|---|
| the support matrix, and which dates are estimates | hub §1 |
| the floor decision, its alternative, and what each forfeits | hub §3d–§3e |
| feature availability at a given floor | hub §4a |
| src vs flat, and the exact failure modes src prevents | boundaries §3 |
| dependency declaration: deps vs groups vs extras vs lock | boundaries §4 |
| the full gate ledger with exit-code contracts | gates §2 |
| adopting gates on an existing codebase without a rewrite | gates §4, and `cards/gates-and-ci.md` |
