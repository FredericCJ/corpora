# Card: add or split a module, package it, change a public name

**Load when:** creating a module, moving code between modules, adding a dependency, publishing, or
changing/removing anything public.
**Depth:** `reference/python_module_boundaries_manifest.md`. Scaffolding a new project is
`cards/start-project.md`; CI wiring is `cards/gates-and-ci.md`.

## The organising claim

**A boundary that is not machine-checked is a preference, and preferences decay.** `__all__`, docstrings
and directory names document intent; a contract file that fails a build enforces it. Everything below
turns "keep it modular" into something a machine can reject.

## Do

1. **One package, one public surface.** The public API is what `__init__` re-exports and `__all__` names;
   everything else is underscore-private and callers have no claim on it.
2. **Dependencies point toward the more fundamental.** `domain` depends on nothing of yours; `services`
   depend on `ports`; `adapters` implement `ports`; only the composition root knows concrete adapters.
   Write the direction down, then enforce it (step 3).
3. **Express the direction as a contract, not a convention.** `import-linter` contract types:
   - `layers` — an ordered stack; higher may import lower, never the reverse
   - `forbidden` — named modules may not import named targets (including external packages)
   - `independence` — named siblings may not import each other
   - `protected` — only an allow-list may import the target. **Direct imports only** — unlike the other
     three it does **not** follow chains, so `a → b → protected` passes. Know this before relying on it.
   `lint-imports` in CI; `deptry .` for declared-vs-actual dependency drift.
4. **Absolute imports.** Relative imports make a module's position load-bearing, which is exactly what you
   are trying to keep changeable.
5. **No import-time side effects.** Import defines; it does not act. This is what makes a module safe to
   import from a test, a script, or a different application.
6. **Break cycles by extracting the shared abstraction**, not by moving the import inside a function.
   A deferred import hides the cycle from the reader and from most tools while keeping the coupling.
   (Understand the mechanics: a partially-initialised module is registered in `sys.modules` *before* its
   body finishes, which is why a cycle fails with a confusing `AttributeError` rather than a clean error.)
7. **Plugin seams via entry points** (`importlib.metadata`), with dependency injection at a **single**
   composition root. Service Locator is the named alternative you are choosing against — say so if you
   pick it.
8. **Declare dependencies in the right bucket.** Runtime → `dependencies`. Development tooling →
   `[dependency-groups]`. Consumer-facing optional features → `optional-dependencies`. Applications lock
   (`pylock.toml`); libraries pin nothing and constrain narrowly.

## Changing a public name — the four-part visibility contract

**All four parts, or the deprecation window is fiction:**

| # | who / when | mechanism |
|---|---|---|
| 1 | producer, runtime | `@warnings.deprecated` (PEP 702) on the member |
| 2 | producer, test | `-W error::DeprecationWarning` in your own suite, so you see your own deprecations |
| 3 | consumer, static | the type checker reports use of a deprecated member (mypy `deprecated`) |
| 4 | consumer, test | pytest `filterwarnings` promoting `DeprecationWarning` to error downstream |

Then the shape of the change is **expand → migrate → contract**: add the new form, move callers, remove
the old form in a later release — never expand-and-contract in one release, which is a breaking change
wearing a deprecation's clothes. `DeprecationWarning` is invisible by default outside `__main__`, which
is precisely why parts 2 and 4 exist.

## Splitting a module without breaking importers

Move the code, then **re-export from the old location** for one deprecation window, with
`@warnings.deprecated` on the old name. Update the contract file in the same change — a split that
silently satisfies the old contract has not been checked.

## Never

- **Treat `__all__` as enforcement.**
- **Import a sibling's internals** because it is one line shorter than the abstraction.
- **Add a dependency without recording why**, or leave one used-but-undeclared (`deptry` catches the
  second; only review catches the first).
- **Monkey-patch a third-party library** to fit your interface. Adapt at your own seam instead.
- **Publish without `py.typed`** if you ship annotations — consumers get nothing from them otherwise.
- **A `requires-python` ceiling.** A floor only.
- **Remove or rename a public name in the same release you deprecate it.**
- **Flat layout** for anything installable. → `cards/start-project.md` step 2

## When this is over-engineering

For a **single-package project with one public surface**, most of the contract machinery does not pay.
The minimum viable boundary is still worth having: `src/` layout, absolute imports, `__all__` on the
package, no import-time side effects, and one `forbidden` contract keeping I/O out of your pure core.
Add layers when there are layers. → boundaries §12

## Decisions you must not invent

The layer names and direction · which contract types express them · the `requires-python` floor (hub
§3e; default `>=3.13`) · the deprecation window length · versioning scheme and what counts as breaking ·
build backend · whether the repo is a workspace of several packages.

## Go deeper

| question | where |
|---|---|
| the build-system contract, PEP 517/518/621 and the pyproject spine | boundaries §2 |
| src vs flat, and exactly which bugs src prevents | boundaries §3 |
| dependency declaration: deps / groups / extras / lock | boundaries §4 |
| import mechanics as architecture: cycles, side effects, lazy imports | boundaries §6 |
| contract types, what each cannot see, and CI wiring | boundaries §7 |
| plugin seams and the composition root | boundaries §8 |
| PEP 440 versions and visible deprecation | boundaries §9 |
| workspaces and editable installs for incremental build | boundaries §10 |
| documenting a boundary — module view, ADR | boundaries §11 |
