# Card: write or change application code

**Load when:** you are writing new Python, or editing existing Python, in a project that ships.
**Depth:** `reference/python_language_hazards_manifest.md` (hazards, §2–§14) and
`reference/python_linting_practices_manifest.md` (practices, §9–§15). Read only the section named.

## The short version

- Prefer the construct that **eliminates** a hazard class over the discipline that avoids it. A
  `with` block, a frozen dataclass and an `Enum` remove whole categories of bug that no amount of care
  removes reliably.
- Every rule below carries its **enforcement route**. Where the route is `contract-only`, nothing will
  catch you — those are the ones to slow down on.
- **Check the `[on]`/`[off]` marker before trusting a rule code to be active.** Most of the rules you
  would assume are on are off by default. `reference/python_language_hazards_manifest.md` §0.2.

## Write it this way

**Data shape**
1. **Frozen dataclass for a record; `Enum`/`StrEnum` for a closed set; `NewType` for an identifier.**
   A `dict` passed between functions is an untyped contract. `str` for an id is primitive obsession.
2. **`frozen=True` is shallow.** A frozen dataclass wrapping a `list` is mutable — freeze the field type
   too (`tuple`, `frozenset`, or a read-only view). Route: `contract-only`.
3. **Never a mutable default.** Use `field(default_factory=...)`. Route: `lint-catchable` `B006`,
   `RUF012` for mutable class attributes. **The dataclass runtime guard is a *hashability* test, not a
   mutability test** — a custom mutable class that defines `__hash__` sails through and is then shared
   by every instance.
4. **`eq=False` silently gives you identity hashing**, so value-equal objects stop colliding in a
   `dict`/`set` with no diagnostic. Decide `eq`/`frozen`/`order` deliberately.

**Functions**
5. **Guard clauses and early return.** Keep the happy path at one indent level.
6. **Keyword-only parameters for anything a caller could transpose**, positional-only where the name is
   an implementation detail. Route: `contract-only` (but `PLR0913` bounds the count).
7. **No boolean flag parameters** — they encode two functions in one signature. Route: `lint-catchable`
   `FBT001`/`FBT002`.
8. **Pure core, effectful shell.** Keep I/O, the clock, randomness and the network at the edge; the core
   takes values and returns values. This single choice is what makes the rest of the package's testing
   and diagnosis advice affordable.

**Resources and lifetime**
9. **Every resource acquisition is a `with`.** `contextlib.ExitStack` for a dynamic set. Never rely on
   `__del__` or on reference counting — finalisation timing is not a contract.
10. **`pathlib` over `os.path`** for new code. Route: `lint-catchable` `PTH`.

**Correctness traps that read as fine**
11. **`is` compares identity, not value.** Small-int and string interning is an implementation detail;
    `x is 256` is a bug that passes tests. Use `==`, and `is` only for `None`, `True`, `False` and
    sentinels. Note: the checks for `== None` / `== True` are `E711`/`E712`, both **dropped from ruff's
    default set in 0.16.0** — you must select them explicitly.
12. **`zip()` truncates silently.** Always `zip(a, b, strict=True)` unless truncation is the intent.
    Route: `lint-catchable` `B905`, **off by default**.
13. **`dict` preserves insertion order (a language guarantee); `set` does not.** Relying on set order
    passes CI for months, then fails when `PYTHONHASHSEED` changes.
14. **A generator is consumed once.** Iterating twice yields nothing the second time, silently.
15. **Timezone-aware datetimes only.** `datetime.now(tz=UTC)`, never `utcnow()`. Route:
    `lint-catchable` `DTZ`; also banned by name in `config/pyproject.toml`.
16. **Pick the numeric domain deliberately** — `float` for measurement, `Decimal` for money, `Fraction`
    for exact ratios, `int` for counts. Compare floats with `math.isclose`, never `==` and never a bare
    absolute tolerance.
17. **`match` on a bare name is a *capture pattern*, not a constant comparison.** `case SOME_CONSTANT:`
    always matches and binds. Use `case Cls.MEMBER:` or a dotted/literal pattern, and close every
    `match` over a union with `case _: assert_never(x)`.

**Modules**
18. **No import-time work** beyond definitions — no I/O, no network, no config reads, no logging setup.
19. **No module-level mutable state.** If something must be shared, own it explicitly and pass it.
    Route: `contract-only` — say it in review, because no tool will.
20. **Absolute imports; `__init__.py` re-exports deliberately with `__all__`.** Underscore prefix is
    Python's only visibility mechanism — use it and honour it.

## Never

- **`assert` for anything that must hold in production** — stripped under `-O`. Validate and `raise`.
- **A bare `except:` or `except BaseException:`**, or a caught exception that is silently dropped.
- **`except Exception` around `await`** where cancellation must propagate — `CancelledError` is a
  `BaseException` and must not be swallowed.
- **`eval`/`exec` on anything derived from input**; `pickle` on untrusted bytes; `subprocess` with
  `shell=True`; `yaml.load` without `SafeLoader` (note `S506` fires on `yaml.load` regardless of loader,
  so silencing it with `FullLoader` satisfies the linter and not the threat model).
- **`from None`** unless you can say why deleting the cause from the traceback helps the reader.
- **`# noqa` or `# type: ignore` without a code and a reason.** Route: `lint-catchable` `PGH003`/`PGH004`,
  and `RUF100` for suppressions that no longer suppress anything.
- **Mutating a container while iterating it.** Route: `lint-catchable` ruff `B909`, pylint `W4701`
  (list), `E4702` (dict), `E4703` (set) — note the dict and set variants are `E`, not `W`; `W4702`/
  `W4703` do not exist and naming them yields `bad-option-value`.
- **Silently ineffective constructs**: `assert (cond, "msg")` (always true — it is a tuple), a missing
  `@enum.unique`, `Final`/`Protocol` expected to do something at runtime, audit hooks mistaken for a
  sandbox. Full list: hazards §15.

## Decisions you must not invent

- **The `requires-python` floor.** Default `>=3.13` (hub §3e). It determines which constructs below are
  even available, and it must equal `target-version`.
- **Whether the project ships `assert` statements at all**, and whether it refuses to start under `-O`.
- **Numeric domain per quantity**, and whether `decimal` traps `FloatOperation` at process start.
- **Whether `__getattr__`-style dynamic access is permitted.** It is unverifiable by construction —
  a design prohibition backed by no diagnostic.

## Go deeper

| question | where |
|---|---|
| the mechanism behind a hazard, and why competent people still write it | hazards §2–§14 |
| the full routing table: hazard → rule code → residual risk | hazards §0–§19 |
| constructs that look like enforcement and are not | hazards §15 |
| `B023` vs `B006` — the fix for one is what the other forbids | hazards §16.1 |
| the safe modern subset for a new project, as prohibitions plus replacements | hazards §18 |
| which lint families to enable, and which fight the type checker | linting §3.2 |
| idioms and named anti-patterns at function/module/expression altitude | linting §9–§15 |
| what the type system cannot express, so it must become a runtime contract | `reference/python_typing_contract_manifest.md` §4 |
| checking your work before you finish | `cards/review-code.md` |
