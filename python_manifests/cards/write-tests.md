# Card: write or fix tests

**Load when:** adding tests, fixing a flaky test, or deciding what a change owes in verification.
**Depth:** `reference/python_testing_tooling_manifest.md`. Concurrency determinism is in
`cards/concurrency.md`; what to assert about errors is in `cards/handle-errors.md`.

## The short version

- **Specify the obligation, then write the test.** Name the seam, the observable contract, the input
  partitions (equivalence classes + boundary values), and the error paths. A test that asserts nothing
  a contract promised is decoration.
- **Design for testability instead of mocking around its absence.** A pure core needs no doubles; most
  mocking is a symptom of I/O in the wrong place.
- **Coverage is a flashlight, not a target.** Use it to find untested branches — especially error paths.

## Do

1. **Four phases, visibly: arrange, act, assert, teardown** — and teardown belongs to the fixture, not
   the test body.
2. **Prefer a fake that implements the real contract over a mock.** Then run **one contract test suite
   against both the fake and the real implementation** — that is what keeps the fake honest. When you do
   mock, use `autospec=True`/`spec_set=True` so the double cannot drift from the signature.
3. **Build test data with a builder** (named defaults, override what matters). Every literal in a test
   body that is not the thing under test is noise.
4. **Property-based tests for the pure core** — round-trip, invariant, oracle, metamorphic; stateful
   machines for protocols. Example-based tests for the effectful shell.
5. **Inject nondeterminism, never reach for it.** Clock, seed, executor, event loop, network — all
   parameters. This is the single highest-leverage testability move.
6. **Test the error contract, not just the happy path.** Assert on the exception *type and its structured
   attributes*, on the group members for an `ExceptionGroup`, and on the typed-result variant. A new
   `raise` with no test is an untested branch.
7. **Make deprecation fail the build**: `filterwarnings = ["error::DeprecationWarning"]` in the pytest
   config **plus `-X dev` in the test command**. Both are required — `ResourceWarning` is filtered by
   default, so `filterwarnings` alone surfaces nothing.
8. **Snapshot/approval tests need canonical serialisation first.** Without a stable ordering and
   formatting, a snapshot test is a random failure generator.

## Configuration traps that make CI differ from your machine

- **Pin `pytest` to an exact-enough version.** `9.0.0`–`9.0.3` silently ignored `--strict-markers` and
  `--strict-config` when set via `addopts`, so suites that looked strict were not.
- **Exactly one config table.** `[tool.pytest.ini_options]` and the newer `[tool.pytest]` **cannot
  coexist** in one file, and a stray `pytest.ini` anywhere up the tree wins over `pyproject.toml`
  outright — candidates are never merged, first match wins.
- **Register every marker and enable `--strict-markers`**, or a typo silently skips nothing.
- **Hypothesis profiles rewrite your settings in CI**, and its health checks (notably the
  function-scoped-fixture check) will fail tests that pass locally. Choose the profile deliberately.
- **Coverage across subprocesses needs configuration**; a clean-looking report can simply be blind.
- **`--import-mode=importlib` with no `__init__.py` in `tests/`** is the recommended default; then keep
  test module basenames unique.

## Never

- **A test with no assertion.** Ban it as a gate; coverage cannot see the difference.
- **Time, randomness, network, filesystem location or execution order as an implicit input.**
- **`sleep` to wait for something.** Poll a condition or inject the clock.
- **A bare absolute tolerance for float comparison** — it is a latent flake. Choose relative or ULP
  deliberately.
- **A mock of a type you own** where the real object would do.
- **A coverage percentage as the objective.** Read the *missing* lines instead.
- **Deleting or `xfail`-ing a flaky test without recording why.** Quarantine is containment, not a fix.

## What a change owes

| change | verification it owes |
|---|---|
| new pure function | property or partition-based test of the contract |
| new error path / new `raise` | a test that reaches it and asserts type + attributes |
| new public API | a contract test, run against fake and real |
| bug fix | a test that fails before the fix |
| new dependency at a boundary | a fake + one integration test proving the fake matches |
| concurrency | a deterministic test with an injected scheduler/clock (`cards/concurrency.md`) |

## Decisions you must not invent

Where the unit/integration line falls · the target test mix · whether a coverage gate exists at all and
what it is *for* · which nondeterminism is injected vs quarantined · whether mutation testing is run,
and on which subset (it is expensive and it is honest about that).

## Go deeper

| question | where |
|---|---|
| the pytest configuration surface and its precedence chain | testing §1a |
| fixture scopes, finalisation, conftest resolution | testing §1 |
| the double taxonomy, and when each is right | testing §3 |
| named testability tactics, and which construct realises which | testing §7 |
| Hypothesis health checks and CI profiles | testing §4 |
| coverage mechanics, and the arithmetic that makes thresholds lie | testing §5a |
| verification beyond coverage: mutation, snapshot | testing §6 |
| gate wiring, thresholds, flake policy | `cards/gates-and-ci.md` |
