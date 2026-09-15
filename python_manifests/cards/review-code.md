# Card: review a diff (or check your own work before finishing)

**Load when:** reviewing a change, or doing the final pass over your own edit before you report done.
**Depth:** every `reference/` file carries an `## Anti-patterns checklist`; this card is the union,
ordered by how often the defect ships. Read the owning section when you need the argument.

## How to use this

Work top to bottom. Each item is **reject on sight** — not a discussion prompt. Where an item names a
rule code, the reviewer's job is to check whether that code is *actually enabled* in this repo, because
most are off by default; a rule nobody runs is not a control.

State findings as: **what is wrong → what it breaks → the fix.** A finding without a failure mode is a
preference.

## Correctness

- [ ] **`assert` doing real work** — validating input, enforcing an invariant, checking a security
      property. Stripped under `-O`. → validate and `raise`. `S101`
- [ ] **`assert (cond, "message")`** — a non-empty tuple, always true. Silently no test at all.
- [ ] **Mutable default argument**, or a mutable class attribute shared across instances. `B006`, `RUF012`
- [ ] **Closure capturing a loop variable** and used later — all copies see the last value. `B023`
- [ ] **`zip()` without `strict=`** where lengths should match. Silent truncation. `B905` *(off by default)*
- [ ] **`is` against a literal or a computed value**; `== None` / `== True`. `E711`/`E712`
      *(both dropped from ruff's defaults in 0.16.0 — check they are selected)*
- [ ] **Naive `datetime`**, or `utcnow()`. `DTZ`
- [ ] **Float compared with `==`**, or with a bare absolute tolerance. → `math.isclose`
- [ ] **Reliance on `set` iteration order**, or on `dict` order where the code did not create it.
- [ ] **A generator iterated twice**, or consumed before the length check.
- [ ] **`case NAME:` in a `match`** — a capture pattern that always matches. → dotted or literal pattern.
- [ ] **A `match` over a union with no `case _: assert_never(x)`** — adding a variant will not break the
      build, which is the whole point of the union.
- [ ] **Container mutated while iterated.** `B909`, pylint `W4701`/`E4702`/`E4703`

## Errors

- [ ] **Bare `except:` / `except BaseException:`** — swallows `KeyboardInterrupt`, `SystemExit`. `BLE`
- [ ] **Catch-and-ignore**, `except: pass`, `except: continue`. `S110`, `S112`
- [ ] **`except Exception` around an `await`** where cancellation must propagate — `CancelledError` is a
      `BaseException` and swallowing it breaks shutdown.
- [ ] **A library exception crossing your own API boundary** unwrapped. → `raise Domain(...) from low`
- [ ] **Lost cause** — `raise Domain(...)` inside an `except` with no `from`. `B904` *(off by default)*
- [ ] **`from None`** with no stated reason. It deletes the real source from the traceback.
- [ ] **An exception used for a routine, expected outcome** that the caller must always handle. → typed
      in-band result the checker forces them to handle.
- [ ] **`return`/`break`/`continue` inside `finally`** — discards an in-flight exception. `B012`
- [ ] **String-only errors** with no structured attributes — not machine-consumable, not greppable.
- [ ] **Catch-log-rethrow at every level.** Log once, at the handling boundary.

## Observability

- [ ] **A library configuring handlers, `basicConfig`, or a level.** Libraries emit; applications route.
- [ ] **Missing `NullHandler`** on a library's top-level logger.
- [ ] **f-string or `.format()` inside a logging call** — formats even when the level is disabled, and
      defeats structured aggregation. `G001`–`G004` *(off by default)*
- [ ] **`logger.error()` where the exception is being handled** — use `logger.exception()` so the
      traceback survives. `TRY400`
- [ ] **`.exception()` outside an `except` block** — attaches `None` as the exception. `LOG004`
      *(stabilised in ruff 0.16.0 but **not** default-enabled)*
- [ ] **A secret, token, password or PII in a log line, an exception message, or a `repr`.**
- [ ] **`print()` in library or application code.** `T201`

## Concurrency

- [ ] **`create_task` with no reference held** — the task can be garbage-collected mid-flight. `RUF006`
- [ ] **A queue with no `maxsize`**, or with no stated policy for what happens when it fills.
- [ ] **`sleep` used to synchronise.** → an event, a condition, or a deterministic clock.
- [ ] **A blocking call inside a coroutine.** `ASYNC`
- [ ] **Shared mutable state across threads with no lock and no ownership rule** — and no, the GIL never
      guaranteed what people think it did.

## Structure

- [ ] **Import-time side effects** — I/O, network, config reads, logging setup at module scope.
- [ ] **Module-level mutable state** used as a singleton.
- [ ] **A new cross-layer import** that the dependency contract does not permit. → `lint-imports`
- [ ] **A public name changed or removed with no deprecation window.** All four parts of the visibility
      contract, or the window is fiction (`python_module_boundaries_manifest.md` §9.3).
- [ ] **A new dependency added to `pyproject.toml` with no reason recorded**, or used-but-undeclared.
      `deptry`
- [ ] **`__all__` treated as enforcement.** It is documentation.

## Tests

- [ ] **A test with no assertion.**
- [ ] **A mock where a fake implementing the real contract would do** — mocks couple tests to
      implementation and survive refactors that break behaviour.
- [ ] **A test that depends on wall-clock time, real randomness, network, or execution order.**
- [ ] **A new error path with no test**, and a new `raise` with no test that it is reachable.
- [ ] **A coverage number quoted as the goal.** It is a diagnostic.

## Suppressions and config

- [ ] **`# noqa` or `# type: ignore` with no code and no reason.** `PGH003`, `PGH004`
- [ ] **A suppression that no longer suppresses anything.** `RUF100`
- [ ] **A suppression count that went up** without a stated reason. The ratchet only works one way.
- [ ] **An unpinned tool version**, or a `select` list that relies on the tool's defaults.
- [ ] **`target-version` above the `requires-python` floor** — `UP` fixes will emit syntax that is a
      `SyntaxError` on the interpreter you publish for.

## Before you say "done"

- [ ] Every `OPEN` you hit is written down as **ASSUMED** (with the default you took) or
      **NEEDS-INPUT** (with the question) — never silently resolved.
- [ ] Every claim you made about tool behaviour was **measured**, or is flagged as unverified.
- [ ] You did not invent a rule code, flag, version or API name anywhere.

## Go deeper

| question | where |
|---|---|
| the argument behind any item above | that manifest's `## Anti-patterns checklist` |
| whether a named rule is on by default in this repo | linting §4.1/§4.2, and measure it |
| the failure mode behind a hazard | hazards §2–§14 |
| what belongs in a gate versus a review | `reference/python_quality_gates_manifest.md` §2 |
