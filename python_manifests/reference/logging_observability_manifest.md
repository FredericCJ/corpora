# Logging & Observability — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for designing robust LOGGING and OBSERVABILITY into
small-scale, strictly-typed, **reuse-first** Python applications. It serves a feature with three
goals: **goal1** — a debugging aid for the developer/contributor *and* for downstream reusers;
**goal2** — monitoring the software in action operationally; **goal3** — per-component reusability,
so each component drops cleanly into a consuming application without dragging logging policy with it.
This file is **GROUNDING, not a rulebook**: cite a rule when it materially shapes a decision; reason
beyond it when the situation does not match. Every factual claim is tagged **ESTABLISHED** (normative
and stable in the cited primary source), **VERSION-DEPENDENT** (tied to a Python/library version or to
a derived phrasing not verbatim in the source), or **OPEN** (no authoritative python.org source; a
best-practice or project-policy call); **FLAGGED-SECONDARY** marks a claim whose only evidence was a
secondary source; Claude-Code mechanics are tagged **CC-FACT** where they arise.
Sibling manifests are cross-referenced by filename and **not duplicated**: spec discipline lives in
`software_spec_discipline_manifest.md`; architecture principles in `architecture_manifest_default.md`;
typing facts in `python_typing_contract_manifest.md`; test tooling in
`python_testing_tooling_manifest.md`; the exception-propagation contract this manifest composes with
lives in `error_tracing_contract_manifest.md`. The full deferral list is the final block of this file.

**Version anchor.** This file states logging **behaviour**; it never re-asserts release dates or
support phases. Those live in **`python_platform_baseline_manifest.md`** (re-verified 2026-08-08),
which owns the CPython release/support matrix and PEP-status-by-version for the whole collection.
Behaviour-relevant gates are carried inline as `VERSION-DEPENDENT (3.x)` and are read against the
project's declared minimum interpreter.

---

## TL;DR

- **Five emittable severities, six named constants.** DEBUG/INFO/WARNING/ERROR/CRITICAL are what you
  call; `NOTSET` (0) is a **sentinel** for "inherit the effective level", not a sixth severity, and a
  spec that enumerates six levels has conflated the constants with the severities. ESTABLISHED — §2,
  §2a.
- **A reusable component is silent and unopinionated: `getLogger(__name__)`, one `NullHandler` on its
  top-level logger, and nothing else** — no other handlers, no `basicConfig`, no level setting, because
  "configuration of handlers is the prerogative of the application developer". Handler, level and
  formatter choices belong to the consuming application. ESTABLISHED — §4, §5.
- **Pass `%`-style arguments and gate expensive ones with `isEnabledFor`.** Deferral of message
  formatting is python.org's documented behaviour; the f-string prohibition is ruff `G004`'s rule —
  cite each to its own source rather than attributing the f-string ban to python.org. ESTABLISHED —
  §9.
- **Log an exception exactly once, at the handling boundary**, with `logger.exception()` inside the
  `except` block (or `exc_info=True` to attach a traceback at a non-ERROR level); re-raising *and*
  re-logging at every layer produces duplicate stack traces, and "log once" is a rule about duplicate
  tracebacks, not licence to discard what only the error site knows. OPEN / best-practice (not stated
  verbatim in the docs) — §10.
- **Redact with a Filter attached to the LOGGER, never in a Formatter**, and cover all four leaking
  surfaces — `record.msg`, `record.args`, `record.exc_info`/`exc_text`, and every `extra` key — placed
  **upstream** of any `QueueHandler`, which has already merged msg+args and nulled the rest before the
  listener sees the record. ESTABLISHED (derived from the gating/propagation semantics of §3–§3a) —
  §11a.
- **There is no stdlib JSON formatter**, so decide the machine-readable route before writing
  `dictConfig`: a third-party formatter or a hand-written `Formatter` subclass. `logging.JSONFormatter`
  is an invented API. VERSION-DEPENDENT (still absent as of 3.15.0rc1) — §7a.

---

## 1. Scope and the three goals

Target: a small, strictly-typed, reuse-first Python codebase made of components meant to be lifted
into other applications. Logging is the observability seam; the design problem is to make the seam
*useful* (goals 1 and 2) without making it *opinionated* (goal 3). The whole architecture below is the
mechanical resolution of that tension: components emit richly and configure nothing; applications
configure once and own all routing.

The three goals map onto the severity model and architecture as follows, developed in §6:
- **goal1 (debug aid)** → DEBUG/INFO at component seams with descriptive context, source obvious from
  the logger name.
- **goal2 (operational monitoring)** → INFO/WARNING/ERROR/CRITICAL as the operational signal, plus
  structured/JSON output and correlation/trace IDs.
- **goal3 (per-component reuse)** → `NullHandler` + zero global configuration + propagation. **This is
  the load-bearing constraint** and the one most easily violated; it is **BEST-EFFORT, not absolute**
  (§4, §6).

---

## 2. The severity model: FIVE emittable levels

**ESTABLISHED.** The stdlib `logging` module defines exactly five severities you actually emit at,
with these numeric values and official "when to use" semantics
(https://docs.python.org/3/library/logging.html; https://docs.python.org/3/howto/logging.html):

| Level | Numeric | Official semantics (verbatim) |
|---|---|---|
| **CRITICAL** | **50** | "A serious error, indicating that the program itself may be unable to continue running." |
| **ERROR** | **40** | "Due to a more serious problem, the software has not been able to perform some function." |
| **WARNING** | **30** | "An indication that something unexpected happened, or that a problem might occur in the near future (e.g. disk space low). The software is still working as expected." |
| **INFO** | **20** | "Confirmation that things are working as expected." |
| **DEBUG** | **10** | "Detailed information, typically only of interest to a developer trying to diagnose a problem." |

These are the levels you call via the convenience methods `logger.critical/error/warning/info/debug`.
The five values are literal module-level assignments in `Lib/logging/__init__.py`, alongside `NOTSET=0`
(§2a) (https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py). (ESTABLISHED)

**ESTABLISHED — the library reference and the HOWTO are NOT the same table; quote one page, not
"both".** The two pages carry **different wordings** of the same guidance and must be quoted
separately. Library reference DEBUG: "Detailed information, typically only of interest to a developer
trying to diagnose a problem."; HOWTO DEBUG: "Detailed information, typically of interest only when
diagnosing problems." Library reference WARNING: "…or that a problem might occur in the near future
(e.g. 'disk space low')."; HOWTO WARNING: "…or indicative of some problem in the near future (e.g.
'disk space low')." (https://docs.python.org/3/library/logging.html;
https://docs.python.org/3/howto/logging.html). **The table above quotes the library reference.** That
is also the table that includes NOTSET as a row, and it carries a meaning the HOWTO omits: "When set on
a handler, all events are handled." (§2a). A derived spec that cites "both pages" for one wording is
citing a page that does not contain it.

**ESTABLISHED — default threshold.** The default level of the root logger is **WARNING**; "only events
of this severity and higher will be tracked, unless the logging package is configured to do otherwise"
(https://docs.python.org/3/howto/logging.html). Consequence for every decision table below: **INFO and
DEBUG are silent by default** and require the consuming application to lower the threshold
(`basicConfig`/`dictConfig`). A component that "logs INFO" emits nothing until an application asks for
INFO.

### 2a. NOTSET (0) is a SENTINEL, not a sixth severity — explicit correction

**ESTABLISHED — the trap.** The module also defines `NOTSET = 0`. That makes **six named level
constants** but only **five emittable severities**. A specification that says "five levels" and then
enumerates six (including NOTSET) is **conflating the level CONSTANTS with the emittable SEVERITIES**.
The correct treatment, and the one this manifest adopts: enumerate the **five** severities you actually
call, and document NOTSET **separately** as a sentinel
(https://docs.python.org/3/library/logging.html). **You never write `logger.log(logging.NOTSET, ...)`
as a real severity** — NOTSET is not an emission level.

**ESTABLISHED — what NOTSET actually means.** It is the "no level explicitly set / defer to parent"
sentinel that drives the effective-level lookup. Verbatim docs: "When set on a logger, indicates that
ancestor loggers are to be consulted to determine the effective level. If that still resolves to
NOTSET, then all events are logged." And: "When a logger is created, the level is set to NOTSET (which
causes all messages to be processed when the logger is the root logger, or delegation to the parent
when the logger is a non-root logger)." So on a **non-root** logger NOTSET means *walk up*; on the
**root** logger NOTSET means *process everything*
(https://docs.python.org/3/library/logging.html). NOTSET configures the effective-level machinery; it
is meaningless as an emission severity.

**ESTABLISHED — the commonly-missed half: on a HANDLER, NOTSET means "handle everything", not
"defer".** The library-reference levels table gives NOTSET two meanings, and the second is "When set on
a handler, all events are handled." (https://docs.python.org/3/library/logging.html). Deferral is a
**logger-only** semantic: `handler.setLevel(logging.NOTSET)` is not an inert "inherit from somewhere",
it opens that handler to every record propagation offers it. An agent using NOTSET to mean "leave this
handler's level alone" has instead removed the handler's threshold.

### 2b. Decision table — which level, and print vs `warnings.warn` vs `logging`

**ESTABLISHED.** The dispatch below comes straight from the HOWTO's "what to use when" guidance
(https://docs.python.org/3/howto/logging.html):

| Situation | Use | Rationale |
|---|---|---|
| Console output for ordinary CLI usage | `print()` | Plain user-facing output, not an observability event. |
| Report events during normal operation; status monitoring / fault investigation | `logger.info()` or `logger.debug()` | INFO = "working as expected"; DEBUG = developer diagnostics. |
| Internal decision / input / branch point of interest to a contributor | `logger.debug()` | Developer-facing diagnostics; silent in production by default. |
| A component begins/ends a meaningful unit of work; public-API boundary crossed | `logger.info()` | The operational "things are working" signal (goal1/goal2 seam). |
| Issue a runtime warning the **client code should change** (avoidable misuse) | `warnings.warn()` | Library-code idiom for "fix your usage." |
| Something unexpected happened but the software still works, and the **client app can do nothing** about it, yet it should be noted | `logger.warning()` | WARNING semantics; not the caller's bug to fix. |
| A function could not be performed / a serious problem occurred | `raise` an exception, or `logger.error()` / `logger.exception()` / `logger.critical()` | Error reporting; see §10 for log-once discipline. |

The `print` vs `warnings.warn` vs `logging.warning` split is the most-missed part: `warnings.warn` is
for *avoidable* problems the **caller** should fix; `logger.warning` is for *unavoidable* notable
events the caller cannot act on. (ESTABLISHED.)

**ESTABLISHED — `warnings` and `logging` have exactly one supported bridge.**
`logging.captureWarnings(True)` redirects the `warnings` subsystem into logging: "a warning will be
formatted using `warnings.formatwarning()` and the resulting string logged to a logger named
`'py.warnings'` with a severity of `WARNING`" (https://docs.python.org/3/library/logging.html).
`'py.warnings'` is therefore the logger name an application configures in order to route dependency
deprecation noise. There is no other routing between the two subsystems.

### 2c. The level-constant surface: aliases, custom levels, and the global kill switch

Four facts about the level API that decide real behaviour, all read from the library reference and
`Lib/logging/__init__.py` (https://docs.python.org/3/library/logging.html;
https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py):

- **ESTABLISHED — `WARN` and `FATAL` exist, are exported, and are undocumented as levels.** `WARN = WARNING`
  and `FATAL = CRITICAL` are real module attributes exported in `logging.__all__`, yet absent from the
  documented levels table. The asymmetry that bites: `_levelToName` maps only
  CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET while `_nameToLevel` *additionally* maps `'WARN'` and
  `'FATAL'`. So `setLevel('WARN')` works, but `getLevelName(30)` **always** returns `'WARNING'` and can
  never return `'WARN'`. Code that round-trips a level name through `getLevelName` and compares against
  `'WARN'` silently never matches. Use the five documented names only.
- **ESTABLISHED — `Logger.warn` is a deprecation you cannot see.** It calls
  `warnings.warn("The 'warn' method is deprecated, use 'warning' instead", DeprecationWarning, 2)` and
  then delegates to `warning`. It is not removed, and `DeprecationWarning` is hidden by default warning
  filters, so the deprecation is **invisible at runtime**. The mechanical catch is lint, not the
  interpreter: ruff `LOG009` and `G010` (§12a).
- **ESTABLISHED — defining a custom level at an existing numeric value is destructive.** Verbatim: "If
  you define a level with the same numeric value, it overwrites the predefined value; the predefined
  name is lost." Custom levels are a global, process-wide mutation of a shared registry, so a *reusable
  component* should never define one (**OPEN** — derived from §4's stated rationale that configuration
  is the application developer's prerogative; the docs do not say this about levels verbatim).
  `getLevelName(level)` is also bidirectional (int→name and name→int, the string direction "reinstated in
  3.4.2") and, on no match, **returns the string** `'Level %s' % level` rather than raising, so a typo
  becomes a rendered field, not an error.
  `getLevelNamesMapping()` returns a fresh copy per call — safe to mutate, one dict copy per call.
  (VERSION-DEPENDENT (3.11) for `getLevelNamesMapping`; `setLevel` has accepted a string name since 3.2,
  but "levels are internally stored as integers", and `getEffectiveLevel()`/`isEnabledFor()`
  return/expect ints.)
- **ESTABLISHED — `logging.disable()` is a process-wide kill switch checked BEFORE everything else.**
  `logging.disable(level=CRITICAL)` installs an override that "takes precedence over the logger's own
  level"; `Logger.isEnabledFor` checks `self.disabled`, then `self.manager.disable >= level`, and only
  then the effective level. Nothing in the API scopes it: a library that calls it silences the entire
  application including loggers it does not own, and a test that calls it and forgets
  `logging.disable(logging.NOTSET)` silences the rest of the suite. **A reusable component should never
  call it** (**OPEN** — same derivation as above; §4). The `CRITICAL` default arrived in 3.7 —
  VERSION-DEPENDENT (3.7).

---

## 3. Architecture: Logger, Handler, Formatter, Filter

**ESTABLISHED — four object types** (https://docs.python.org/3/library/logging.html):
- **Logger** — "Loggers expose the interface that application code directly uses." This is what
  components hold and call.
- **Handler** — "Handlers send the log records (created by loggers) to the appropriate destination"
  (console, file, JSON sink, network).
- **Filter** — "Filters provide a finer grained facility for determining which log records to output."
  Filters may also *modify* records (used for contextual fields; §7, §8).
- **Formatter** — "Formatters specify the layout of log records in the final output."

**Named vocabulary (ESTABLISHED name, cited).** This four-object split is the pattern literature's
**Diagnostic Logger** — SWE corpus element `diagnostic-logger`, named in Harrison, "Patterns for Logging
Diagnostic Messages", in Martin, Riehle & Buschmann (eds.), *Pattern Languages of Program Design 3*,
1997 (Addison-Wesley, ISBN 978-0-201-31011-5). The name buys nothing technical; it buys a shared word
with every other logging framework an agent has met (log4j, SLF4J, `ILogger`), and it makes the
context mechanism of §7–§8 nameable as its documented companion, **Diagnostic Context** (§8).

**ESTABLISHED — two-stage level thresholds.** A `LogRecord` is gated **twice**
(https://docs.python.org/3/library/logging.html):
1. It is **created only if** its level ≥ the logger's **effective level** (walked up the hierarchy; root
   NOTSET ⇒ all events), and it passes any **logger** filters.
2. It is then offered to each handler reachable via propagation, and **each handler independently
   drops it** if it is below **that handler's own level**, and applies that handler's own filters and
   formatter.

**Manifest implication (ESTABLISHED).** Set the logger (or root) level to the **lowest** severity you
ever want to capture, and use **per-handler levels to fan out** — e.g. a console handler at INFO and a
file/JSON handler at DEBUG against the same root logger at DEBUG. The two-stage model is why one
configuration can route the same stream to multiple destinations at different verbosities.

### 3a. Logger hierarchy, `getLogger(__name__)`, effective level, propagation

**ESTABLISHED — singletons via `getLogger`.** "Loggers should NEVER be instantiated directly, but
always through the module-level function `logging.getLogger(name)`. Multiple calls to `getLogger()`
with the same name will always return a reference to the same `Logger` object." Convention is
`logging.getLogger(__name__)` so logger names track the package/module hierarchy
(https://docs.python.org/3/library/logging.html; https://docs.python.org/3/howto/logging.html).

**ESTABLISHED — dotted hierarchy and effective-level walk-up.** Names like `foo`, `foo.bar`,
`foo.bar.baz` form a parent/child hierarchy and "all loggers are descendants of the root logger." "If
a level is not explicitly set on a logger, the level of its parent is used instead as its effective
level… all ancestors are searched until an explicitly set level is found"
(https://docs.python.org/3/library/logging.html; https://docs.python.org/3/howto/logging.html). This
is the NOTSET sentinel (§2a) in action.

**ESTABLISHED — propagation.** `propagate` defaults to **True** (set in the constructor). "If this
attribute evaluates to true, events logged to this logger will be passed to the handlers of higher
level (ancestor) loggers… Messages are passed **directly** to the ancestor loggers' handlers — **neither
the level nor filters of the ancestor loggers in question are considered**"
(https://docs.python.org/3/library/logging.html). Two consequences:
- An ancestor's *handlers* receive the record, but the ancestor's *level/filters* are **not**
  re-checked — only the originating logger's effective level (stage 1) and each handler's own level
  (stage 2) gate the record. **Consequence agents trip on:** raising the *root* logger's level does not
  quiet a chatty child. Lower the child's level, or gate at the handler.
- **ESTABLISHED — a handler on both a logger and an ancestor duplicates output.** "If you attach a
  handler to a logger *and* one or more of its ancestors, it may emit the same record multiple times."
  Propagation stops at the first logger in the chain with `propagate` false: "If any logger in the chain
  `A.B.C`, `A.B`, `A` has its `propagate` attribute set to false, then that is the last logger whose
  handlers are offered the event to handle." (https://docs.python.org/3/library/logging.html).
  Duplicated log lines are almost always this, not a loop.
- Official best practice: "A common scenario is to attach handlers only to the root logger, and to let
  propagation take care of the rest." This is why a top-level application configures one set of
  handlers and child/module loggers need none — the mechanical foundation of goal3.

---

## 4. Reusable-component / library discipline (goal3 — the load-bearing part)

This is the heart of the feature. A reusable component must be **silent and unopinionated by default**
and hand *all* configuration to the consuming application. The rules below are quoted from the official
"Configuring Logging for a Library" guidance
(https://docs.python.org/3/howto/logging.html), tagged by how firmly the source states them.

- **ESTABLISHED — use `getLogger(__name__)`; do NOT log to root.** "It is strongly advised that you do
  not log to the root logger in your library. Instead, use a logger with a unique and easily
  identifiable name, such as the `__name__` for your library top-level package or module. Logging to
  the root logger will make it difficult or impossible for the application developer to configure the
  logging verbosity or handlers of your library as they wish."
- **ESTABLISHED — do NOT add handlers other than `NullHandler`, and do NOT call `basicConfig`.** "It is
  strongly advised that you do not add any handlers other than `NullHandler` to your library loggers.
  This is because the configuration of handlers is the prerogative of the application developer who
  uses your library." `basicConfig` adds a handler to the **root** logger, so it is forbidden in library
  code by the same rule.
- **ESTABLISHED — attach one `logging.NullHandler()` to the library's TOP-LEVEL logger.** Current docs
  describe `NullHandler` as a handler that "does not do any formatting or output… It is essentially a
  'no-op' handler for use by library developers", whose `emit()` and `handle()` "do nothing" and whose
  `createLock()` "returns `None` for the lock, since there is no underlying I/O to which access needs to
  be serialized" (https://docs.python.org/3/library/logging.handlers.html; Added in version 3.1).
  Canonical one-liner, on the **top-level package logger** only:
  `logging.getLogger('orgname.foo').addHandler(logging.NullHandler())`
  (https://docs.python.org/3/howto/logging.html). **This is the single permitted handler in library
  code — and the docs make it optional, not obligatory.** python.org states that WARNING+ reaching
  `sys.stderr` in the absence of configuration "is regarded as the best default behaviour", and frames
  the NullHandler conditionally: "If for some reason you *don't* want these messages printed in the
  absence of any logging configuration, you can attach a do-nothing handler to the top-level logger for
  your library" (https://docs.python.org/3/howto/logging.html). Adding it is a project choice about
  **default silence**; the prohibitions on root logging, non-Null handlers and `basicConfig` are the
  parts the docs state **unconditionally**.
- **VERSION-DEPENDENT (3.2) — do NOT justify the NullHandler with "No handlers could be found for
  logger XXX".** That message is a **pre-3.2 artefact**. Since 3.2, `logging.lastResort` "replaces the
  earlier error message saying that 'no handlers could be found for logger XYZ'"; `lastResort` is "a
  `StreamHandler` writing to `sys.stderr` with a level of `WARNING`", "No formatting is done on the
  message — just the bare event description message is printed", and it "is not associated with any
  logger" (https://docs.python.org/3/library/logging.html). What a NullHandler suppresses **today** is
  that `lastResort` output — nothing else. `logging.lastResort = None` restores pre-3.2 behaviour.
  Citing the old message as the rationale is a decade out of date, and it misleads about what the
  NullHandler actually changes.
- **VERSION-DEPENDENT / OPEN-wording — "no logging side-effects on import."** The docs contain no single
  sentence literally saying "no side effects on import," so treat the strict phrasing as
  **derived-best-practice**, not a verbatim quote. What **is** officially established and adds up to the
  same rule: do not call `basicConfig`, do not configure root, do not add non-Null handlers. The **only**
  logging actions a module may safely take at import are `logger = logging.getLogger(__name__)` and (at
  the package top level) `addHandler(NullHandler())`. **Tag the literal "no side-effects on import"
  bullet as best-practice/OPEN-wording in any derived spec while citing the handler/root rules as
  ESTABLISHED.**

**Why goal3 is BEST-EFFORT, not absolute (route: contract-only, plus the two lint rules of §12a).** The
discipline is enforced by convention and review, not by the type system or the runtime: a component
*can* call `basicConfig`, and nothing stops it. The rules
make reuse clean when followed; they do not make misconfiguration impossible. State goal3 as a
best-effort guarantee.

---

## 5. Application-side configuration (the consumer)

The complement of §4: the **application** owns logging policy and configures it **once, at startup**.

- **ESTABLISHED — configure handlers/levels/formats once, centrally.** Because components add no
  handlers and propagation (default True) carries their records upward, the recommended scenario is to
  "attach handlers only to the root logger, and to let propagation take care of the rest"
  (https://docs.python.org/3/library/logging.html). Configure the root logger to the **lowest** level
  you want to capture, then fan out via per-handler levels (§3).
- **ESTABLISHED — `basicConfig` vs `dictConfig`.** `basicConfig` is the quick path: it adds a handler
  to the root logger (hence forbidden in libraries, §4). For anything with multiple handlers,
  console-vs-file/JSON split, filters, or per-logger levels, prefer a declarative `dictConfig`. The
  cookbook's centralize-configuration guidance is explicit that "the application code does not care
  about multiple handlers" — configure them once to avoid duplicate output
  (https://docs.python.org/3/howto/logging-cookbook.html).
- **Typical fan-out (ESTABLISHED pattern).** Root at DEBUG; a console `StreamHandler` at INFO for
  humans; a file or JSON handler at DEBUG for machines/retention. This realizes goal1 (DEBUG for
  contributors) and goal2 (structured INFO+ for monitoring) from a single configuration.
- **VERSION-DEPENDENT — the old gate list has CLOSED. Which interpreters are supported when is owned by
  `python_platform_baseline_manifest.md`; this file states only the behaviour each gate unlocks.** On a
  **3.10** floor — the oldest branch still receiving fixes, and the `Requires-Python` of every current
  release of structlog, python-json-logger and every `opentelemetry-*` distribution —
  `basicConfig(encoding=)` (3.9), `exc_info`-accepts-an-instance (3.5), `stacklevel=` (**3.8**, not
  unversioned) and `lastResort` (3.2) are **unconditionally available** and are no longer project
  decisions. The gates that still bite on a 3.10 floor, each cited where it is used:
  `getLevelNamesMapping()` (3.11, §2c), `dictConfig` filters-as-instances (3.11, §5a), `asyncio` Task
  `context=` (3.11, §8a), `LogRecord.taskName` and `logAsyncioTasks` (3.12, §8a),
  `getHandlerByName`/`getHandlerNames` (3.12, §5a), `dictConfig` support for
  `QueueHandler`/`QueueListener` and formatter `defaults` (3.12, §9a), `LoggerAdapter(merge_extra=)`
  (3.13, §7), and `QueueListener` as a context manager plus `start()` raising `RuntimeError` when
  already running (3.14, §9a).
- **VERSION-DEPENDENT (3.14.7) — swapping handlers at runtime was racy until very recently.** 3.14.7
  fixed gh-79366: "Fixed a race condition in `logging`: if a handler was removed while a record was being
  emitted, the following handlers of the same logger could be skipped."
  (https://docs.python.org/3.14/whatsnew/changelog.html). A long-running process that reconfigures
  handlers in place needs that floor or its own lock. Configure once at startup and the question does
  not arise.

### 5a. `dictConfig`: the defaults that bite

**ESTABLISHED** unless marked, all from https://docs.python.org/3/library/logging.config.html :

| key / fact | default | what goes wrong |
|---|---|---|
| `version` | **required**; "The only valid value at present is 1" | Not a placeholder. `version: 2`, or omitting the key, is a configuration error — still true in the 3.14 and 3.15 docs. |
| `disable_existing_loggers` | **`True`** ("If absent, this parameter defaults to `True`") | A `dictConfig` call made *after* your modules imported and called `getLogger(__name__)` **silently disables every one of them**. Set it explicitly to `False` unless replacement is intended. |
| `incremental` | **`False`** ("the specified configuration replaces the existing configuration") | Two `dictConfig` calls do **not** merge; the second replaces the first. And `disable_existing_loggers` "is ignored if *incremental* is `True`". |
| `'()'` and `'.'` special keys | — | `'()'` names a factory by absolute import path and passes the remaining keys as keyword arguments; `'.'` maps attribute names to values set *after* construction. This is how a custom Filter or Formatter is wired declaratively, with no module-level globals. |
| `filters` accepting instances | VERSION-DEPENDENT (3.11) | Before 3.11 only ids were accepted. |
| `QueueHandler`/`QueueListener` configurable; formatter `defaults` | VERSION-DEPENDENT (3.12) | A 3.12 floor covers instances-in-`filters`, queue configuration and formatter `defaults` together (§9a). |

- **VERSION-DEPENDENT (3.12) — reach a configured handler without a global.**
  `logging.getHandlerByName(name)` and `logging.getHandlerNames()` are the supported way for application
  code to get at a handler that `dictConfig` created
  (https://docs.python.org/3/library/logging.html). Before 3.12 the usual workaround was a module-level
  global, which quietly defeats configure-once.
- **ESTABLISHED — `logging.config.listen()` is a remote-code-execution surface. Do not expose it.**
  "Because portions of the configuration are passed through `eval()`, use of this function may open its
  users to a security risk." The only mitigation is the `verify` callable, which "is called with a single
  argument — the bytes received across the socket — and should return the bytes to be processed, or
  `None`". At this scale there is no reason to open a configuration socket at all: ship a config file and
  restart.
- **ESTABLISHED — `logging.raiseExceptions` defaults to `True`, and flipping it buys silence, not
  tidiness.** Handler errors route through `Handler.handleError`, which writes to `sys.stderr` only when
  `raiseExceptions and sys.stderr`; "If `raiseExceptions` is `False`, exceptions get silently ignored"
  (https://docs.python.org/3/library/logging.html). A process that sets it `False` converts every handler
  fault — including full-queue record drops (§9a) — into nothing at all. It is a diagnosability decision
  with a real cost; prefer leaving it alone.

### 5b. Steady State: every accumulator needs a purge

**Named vocabulary (name imported, citation FLAGGED-SECONDARY / UNVERIFIED).** SWE corpus element
`steady-state`, named in Nygard, *Release It!*. The corpus's bibliographic record for that work carries
`year: UNRESOLVED, verification: unverified`, so the **name** is imported while the **citation stays
flagged** rather than presented as ground truth. The rule it names: *for every accumulator, a purge.* A
process that runs for weeks fails on whichever thing only ever grows, and logs are the accumulator this
manifest owns.

The stdlib ships the purge (ESTABLISHED, https://docs.python.org/3/library/logging.handlers.html — the
page documents Python 3.14.7):

- `logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
  delay=False, errors=None)` — size-triggered. **The defaults do nothing:** "if either of *maxBytes* or
  *backupCount* is zero, rollover never occurs, so you generally want to set *backupCount* to at least 1,
  and have a non-zero *maxBytes*." Bounded retention is then `maxBytes × (backupCount + 1)` —
  arithmetic over the documented scheme rather than a quoted figure, and a number you can defend on a
  disk budget.
- `logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0,
  encoding=None, delay=False, utc=False, atTime=None, errors=None)` — clock-triggered. `backupCount`:
  "If nonzero, at most *backupCount* files will be kept", oldest deleted at rollover. `utc=True` avoids a
  DST-shifted rollover; `atTime` (a `datetime.time`) pins the daily/weekly instant.
- One rotation mechanism per file — a rotating handler **or** the platform's `logrotate`, never both on
  the same path. (OPEN: which mechanism, and the retention numbers, are a project decision; nothing in
  the docs picks for you. See open questions.)
- **ESTABLISHED — rotation from multiple processes is not a supported configuration**, because writing to
  one file from multiple processes is not: "logging to a single file from multiple processes is *not*
  supported, because there is no standard way to serialize access to a single file across multiple
  processes in Python" (https://docs.python.org/3/howto/logging-cookbook.html). Rotation makes that
  worse rather than better — two processes rotating the same path rename it out from under each other.
  Use a single listener process (§9a) or a socket receiver plus one writer.

The same purge rule applies to the two accumulators a logging setup itself creates: any cache held by a
Filter or Formatter must be bounded (`functools.lru_cache(maxsize=...)`, never unbounded), and any
scratch file must be owned by a `tempfile.TemporaryDirectory` context manager rather than cleaned up by
hope. Non-log accumulators and the long-running-process question generally belong to
`python_runtime_diagnostics_manifest.md` (§14).

---

## 6. Goals mapping (severity + architecture → the three goals)

**goal1 — debugging aid for contributors and reusers (ESTABLISHED).** Use DEBUG/INFO at **component
seams** with descriptive context, and rely on `getLogger(__name__)` so "it is intuitively obvious
where events are logged just from the logger name"
(https://docs.python.org/3/howto/logging.html). Map: **INFO** when a component starts/finishes a
meaningful unit of work and at public-API boundaries; **DEBUG** for internal decisions, inputs, and
branch points. Using `logging` rather than `print` lets the reuser dial verbosity without touching the
component's code — the source is obvious from the logger name, and the level is the application's to
set.

**goal2 — monitor the software in action (ESTABLISHED).** Use **INFO/WARNING/ERROR/CRITICAL** as the
operational signal — WARNING/ERROR/CRITICAL are the alerting tiers per their official semantics (§2).
Prefer **structured/JSON** output and attach **correlation/trace IDs** so one logical request can be
stitched across components/services. Structured/contextual logging is supported via (a) `extra=` /
`LoggerAdapter`, (b) Filters that inject fields, (c) `contextvars`-backed filters for async/threaded
request scope, or (d) `structlog`/JSON formatters
(https://docs.python.org/3/howto/logging-cookbook.html;
https://www.structlog.org/en/stable/contextvars.html). Detailed in §7–§8.

**goal3 — per-component reuse (ESTABLISHED mechanism; BEST-EFFORT guarantee).** The NullHandler
discipline + zero global configuration in component code is exactly what makes components reusable.
Because each component uses `getLogger(__name__)`, adds no handlers (except a top-level NullHandler),
and never configures root/`basicConfig`, the consuming application owns all routing, levels, and
formats; propagation (default True) carries component records to the app's root handlers automatically
(https://docs.python.org/3/howto/logging.html; https://docs.python.org/3/library/logging.html). This is
the **direct mechanical link** between the official library guidance and goal3. As in §4, it is
**explicitly best-effort, not absolute** — enforced by discipline, not by the runtime.

---

## 7. Structured & contextual logging

**ESTABLISHED — `extra=` and `LoggerAdapter`.** Passing `extra={...}` to a log call injects keys onto
the `LogRecord` that a formatter can then render. `LoggerAdapter` is "an easy way in which you can pass
contextual information"; its `process()` "inserts an `extra` key in the keyword argument whose value is
the dict-like object passed to the constructor"
(https://docs.python.org/3/howto/logging-cookbook.html).
**ESTABLISHED — the reserved-key failure is a `KeyError` at the CALL SITE, not a dropped field.**
`Logger.makeRecord` executes
`if (key in ["message", "asctime"]) or (key in rv.__dict__):`
`raise KeyError("Attempt to overwrite %r in LogRecord" % key)`
(https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py, 3.14 branch). Because
`LogRecord.__init__` assigns every documented attribute, **all** of these raise: `name`, `msg`, `args`,
`levelname`, `levelno`, `pathname`, `filename`, `module`, `lineno`, `funcName`, `created`, `msecs`,
`relativeCreated`, `thread`, `threadName`, `process`, `processName`, `taskName`, `exc_info`,
`stack_info`. `message` and `asctime` are guarded by that explicit literal list because the `Formatter`
adds them later. Agents reach for `extra={"module": ...}`, `extra={"name": ...}` and
`extra={"taskName": ...}` constantly; each is a runtime crash on a *logging* call. **Namespace every
`extra` key** (`app_module`, `req_user`, or one nested dict under a single reserved-free key). The static
catch is ruff `G101` (§12a).

**ESTABLISHED — a MISSING custom key is a different failure, and it makes the field mandatory.** If a
handler's format string references an attribute that is absent from the record, "the message will not be
logged because a string formatting exception will occur"
(https://docs.python.org/3/library/logging.html). So a format string containing `%(request_id)s` makes
`request_id` **required on every record routed to that handler**, including records emitted by
third-party libraries that know nothing about it. Supply the default from a Filter (§8), not from
discipline at the call sites.

**VERSION-DEPENDENT (3.13) — `LoggerAdapter` silently discards call-site `extra` unless you ask it not
to.** Without `merge_extra=True`, `process()` "inserts an 'extra' key in the keyword argument whose value
is the dict-like object passed to the constructor" and "if you had passed an 'extra' keyword argument in
the call to the adapter, it will be silently overwritten"
(https://docs.python.org/3/library/logging.html; https://docs.python.org/3/howto/logging-cookbook.html).
Adapter context and per-call context do not compose before 3.13. On an older floor, use a Filter for the
standing context and reserve `extra=` for per-call fields.

**ESTABLISHED — Filters as field injectors.** "You can also add contextual information to log output
using a user-defined `Filter`. Filter instances are allowed to **modify** the LogRecords passed to
them, including adding additional attributes"
(https://docs.python.org/3/howto/logging-cookbook.html). A filter is the right place to stamp
process-wide or request-scoped fields onto every record without touching call sites.

**ESTABLISHED — `structlog` 26.1.0 (`Requires-Python >=3.10`; optional, for goal2 JSON pipelines).**
`structlog` is built from chains of **processors**, **bound loggers** that accumulate context, and
renderers for "JSON, logfmt, as well as pretty console output out-of-the-box". The processor contract is
exact and the ordering is load-bearing, not stylistic
(https://www.structlog.org/en/stable/processors.html):
- A processor is called with three positional arguments — `logger` (the wrapped logger), `method_name`
  (the name of the wrapped method) and `event_dict` (current context merged with the current event, so
  context `{"a": 42}` plus event `"foo"` yields `{"a": 42, "event": "foo"}`).
- **Only the last processor** knows about the output system, and it must return a `str`/`bytes`/
  `bytearray`, an `(args, kwargs)` tuple, or a dict of keyword arguments.
- Any processor may abort an event by raising `structlog.DropEvent`: "If a processor raises
  `structlog.DropEvent`, the event is silently dropped." This is the filtering mechanism and the hard-deny
  hook for redaction (§11).

**ESTABLISHED — the stdlib interop seam has three mandatory placements.**
`structlog.stdlib.ProcessorFormatter` runs structlog processors over arbitrary `logging.LogRecord`s, and
it only works wired one way: the structlog side must end with
`structlog.stdlib.ProcessorFormatter.wrap_for_formatter` (`render_to_log_kwargs()` is **not** a
substitute); non-structlog "foreign" records are pre-processed through the formatter's
`foreign_pre_chain`; and `ProcessorFormatter.remove_processors_meta` must be **first** in the formatter's
own chain. `structlog.stdlib.ExtraAdder` "adds data passed in the `extra` parameter of the `logging`
module's log methods to the event dictionary" — that is how `extra={...}` emitted by a third-party
library survives into a structlog-rendered pipeline
(https://www.structlog.org/en/stable/standard-library.html). For JSON output with usable tracebacks,
structlog's own guidance pairs `structlog.processors.dict_tracebacks` (backed by
`structlog.tracebacks.ExceptionDictTransformer`) with `structlog.processors.JSONRenderer()`.

**VERSION-DEPENDENT — what 26.1.0 changed.** It removed Python 3.8/3.9 support, added Python 3.15
support, added `structlog.stdlib.BoundLogger.is_enabled_for()` and `get_effective_level()`, added
`CallsiteParameter.QUAL_MODULE` to `CallsiteParameterAdder`, and deprecated better-exceptions support
("will be removed within a year")
(https://raw.githubusercontent.com/hynek/structlog/main/CHANGELOG.md).
**VERSION-DEPENDENT — configure once, then freeze.** structlog docs recommend
`cache_logger_on_first_use=True` to "effectively freeze configuration after creating the first bound
logger," implying one-time configuration at startup
(https://www.structlog.org/en/stable/standard-library.html).
**OPEN — library-vs-app split for structlog.** structlog publishes **no** explicit library-vs-app
guidance; by analogy with the stdlib rule, a reusable component should **not** call
`structlog.configure()` — that belongs to the application. Tag "libraries shouldn't configure structlog"
as **best-practice/project-policy**, not vendor doctrine. Note the mechanical reason it matters:
`cache_logger_on_first_use=True` "effectively freezes configuration after creating the first bound
logger", so a second `structlog.configure()` — from a library, or from a test — may simply not take
effect (https://www.structlog.org/en/stable/standard-library.html). Reconfiguration in tests needs an
explicit reset, not another `configure()` call.

### 7a. JSON output: there is no stdlib JSON formatter

**VERSION-DEPENDENT (3.15) — the stdlib does not ship one, as of 3.15.0rc1.** The documented formatter
classes are `logging.Formatter` and `logging.BufferingFormatter`, and nothing else
(https://docs.python.org/3.15/library/logging.html). `logging.JSONFormatter` does not exist, and a
`dictConfig` entry naming `class: logging.JsonFormatter` is an invented API. Machine-readable output
requires a third-party formatter or a hand-written `Formatter` subclass. Two supported routes:

| route | class path | fits when |
|---|---|---|
| python-json-logger 4.1.0 | `pythonjsonlogger.json.JsonFormatter` | You keep stdlib `logging` end to end and want JSON on one handler. Composes with `extra=` and a `dictConfig` `'()'` factory entry (§5a); no application-wide rewrite. |
| structlog 26.1.0 | `structlog.stdlib.ProcessorFormatter` | You want the processor chain (context merging, redaction, `dict_tracebacks`) as the emission pipeline (§7). |

- **ESTABLISHED — python-json-logger is maintained, and its import path MOVED.** 4.1.0 is current,
  maintained by Nicholas Hairs, classified "Development Status :: 6 - Mature",
  `Requires-Python >=3.10`, not yanked (https://pypi.org/pypi/python-json-logger/json). Since 3.1.0
  "`pythonjsonlogger.jsonlogger` is now `pythonjsonlogger.json`", so the current class path is
  `pythonjsonlogger.json.JsonFormatter`; `RESERVED_ATTRS` and `merge_record_extra` moved to
  `pythonjsonlogger.core`. **4.0.0 removed the ability to pass strings** instead of objects for
  `json_default`/`json_encoder`/`json_serializer`, so a `dictConfig` entry passing dotted-path strings
  for those now fails (https://nhairs.github.io/python-json-logger/latest/changelog/). Treating the
  project as abandoned, or emitting the pre-3.1.0 import path, are both stale.
- **OPEN — do not run both formatters on one handler.** `ProcessorFormatter` and `JsonFormatter` compete
  for the same slot; running both on a single handler is not a documented configuration and no source
  sanctions it. Pick one per handler.

---

## 8. Correlation / trace IDs

**ESTABLISHED — stdlib-native via `contextvars` + Filter.** For multithreaded/async code the cookbook
gives a `contextvars.ContextVar` pattern: request-scoped vars are set at the request boundary, and a
**Filter** reads them and stamps fields (e.g. `record.method`, `record.ip`, `record.user`) onto every
record. This is the stdlib-native correlation-ID mechanism — context-local, async-safe, and requires no
change at the individual call sites
(https://docs.python.org/3/howto/logging-cookbook.html).

**ESTABLISHED — `structlog.contextvars`.** structlog provides "a global structlog context that is local
to the current execution context": call `clear_contextvars()` at request start,
`bind_contextvars(request_id=...)` to stamp correlation IDs, and place the `merge_contextvars`
processor **first** so "any context-local binds get included in all of your log messages"
(https://www.structlog.org/en/stable/contextvars.html).

**Named vocabulary (ESTABLISHED names, cited).** The contextvars-plus-Filter mechanism above is the
pattern literature's **Diagnostic Context**, known industrially as **MDC/NDC** (mapped / nested
diagnostic context) after the log4j and SLF4J APIs — SWE corpus element `diagnostic-context`, named in
Harrison, "Patterns for Logging Diagnostic Messages", *Pattern Languages of Program Design 3*, 1997. The
*content* it carries, the id that ties every record from one logical operation together, is the
**Correlation Identifier** of Hohpe & Woolf, *Enterprise Integration Patterns*, 2003 (element
`correlation-identifier`). Two recorded relations matter here:
`diagnostic-context -composes-with-> diagnostic-logger` — "the logger auto-appends the thread-bound
context stash to every message emitted in scope", i.e. the Filter-stamps-contextvars mechanism, named;
and `diagnostic-context -enables-> log-aggregation` / `-enables-> distributed-tracing` — **in-process
correlation is the precondition for anything centralized.** A small app builds the cheap half and stops
there; that is the whole argument of §8b.

**Correlation transport is a scoping decision (OPEN / project policy).** Choose the lightest transport
that fits: a stdlib `contextvars` filter or `structlog.contextvars` for a single process; full
**OpenTelemetry** `trace_id`/`span_id` propagation **only if the application is actually distributed /
multi-service** — and note that for *logs* specifically the deciding fact is **implementation maturity,
not just topology** (§8b). Do not adopt OTel logs for a single-process app. See open question on
correlation-ID transport.

### 8a. asyncio and threads: what a record actually carries

A correlation design that is not explicit about these four facts breaks the first time work moves to a
thread pool.

- **VERSION-DEPENDENT (3.12) — `LogRecord.taskName` is `None` far more often than agents assume.** It is
  derived defensively: `self.taskName = None`, then only if `logAsyncioTasks` is true and `asyncio` is
  already in `sys.modules`, `self.taskName = asyncio.current_task().get_name()` inside a bare
  `try/except Exception: pass`
  (https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py;
  https://docs.python.org/3/library/logging.html). So it is `None` in any sync-only program (asyncio never
  imported) and `None` outside a running loop (the `RuntimeError` from `current_task()` is swallowed). A
  format string containing `%(taskName)s` then renders the literal string `None` — it does **not** fail,
  so the defect ships silently. Do not use `taskName` as a correlation key; use it as a debugging hint.
- **ESTABLISHED — `contextvars` is the async-and-thread-correct carrier, and "thread-correct" does not
  mean "inherited".** "Each thread has its own effective stack of `Context` objects" and "`ContextVar`
  objects behave in a similar fashion to `threading.local()` when values are assigned in different
  threads" (https://docs.python.org/3/library/contextvars.html). A `threading.Thread` or
  `ThreadPoolExecutor` worker therefore starts on its own context stack and **does not see** bindings made
  on the submitting thread. A correlation id bound on the request thread vanishes inside the executor
  callback. Re-bind explicitly at the worker entry point, or pass the id as an argument.
- **VERSION-DEPENDENT (3.11) — asyncio Tasks DO inherit, by copy.** "If no `context` is provided, the Task
  copies the current context and later runs its coroutine in the copied context"; the explicit `context=`
  keyword on `asyncio.create_task`/`Task` was added in 3.11
  (https://docs.python.org/3/library/asyncio-task.html). Because it is a **copy**, bindings made inside a
  Task do not leak back to the parent — which is what you want for per-request scope, and is also why
  "set it once in the parent after spawning" does not work.
- **ESTABLISHED — `ContextVar.get()` raises `LookupError` when unset with no default, and a Filter is the
  worst place for that.** (https://docs.python.org/3/library/contextvars.html). A correlation Filter that
  calls `.get()` bare raises **inside `Filter.filter()`** on the first record logged outside a request
  scope — startup, shutdown, a background task, a library's own logging. Always
  `var.get("-")`/`var.get(None)` with a default, and let the format string render the placeholder. Related:
  `ContextVar.set()` returns a `Token` for `reset()`, and `Token` objects became usable as **context
  managers in 3.14** (VERSION-DEPENDENT (3.14)), which is the cleanest way to scope a binding.

**ESTABLISHED — a Filter that forgets to `return True` drops every record.** `Filter.filter` is both the
field-injection hook and the survival predicate; the cookbook's `InjectingFilter` stamps attributes *and*
returns a boolean (https://docs.python.org/3/howto/logging-cookbook.html). A stamping filter used purely
for context must still return truthy. Nothing warns you: the log simply goes quiet.

### 8b. The OpenTelemetry adoption gate: spec-stable is not implementation-stable

This is the single place in this manifest where an agent is most likely to adopt something premature,
because the true statement "OpenTelemetry logs are stable" and the true statement "OpenTelemetry logs are
not stable in Python" refer to different artefacts.

- **ESTABLISHED — the SPECIFICATION treats logs as done.** The spec status summary lists Logging Bridge
  API `stable`, Logging SDK `stable` and Logging OTLP `stable`; the Logs API document is headed "Stable,
  except where otherwise specified" and the Logs Data Model document is headed "Stable"
  (https://opentelemetry.io/docs/specs/status/; https://opentelemetry.io/docs/specs/otel/logs/api/;
  https://opentelemetry.io/docs/specs/otel/logs/data-model/). Specification version 1.59.0
  (https://opentelemetry.io/docs/specs/otel/).
- **ESTABLISHED — the PYTHON IMPLEMENTATION does not.** opentelemetry.io/status lists Python as Traces
  `Stable`, Metrics `Stable`, **Logs `Development`**, Profiles not implemented, and the Python language
  page repeats "Traces [Stable], Metrics [Stable], Logs [Development]"
  (https://opentelemetry.io/status/; https://opentelemetry.io/docs/languages/python/). This has not moved
  across the two most recent releases.
- **ESTABLISHED — three pieces of corroborating evidence, so this is not one page's opinion.** (1) The
  Python logs SDK still lives at the **private** module path `opentelemetry.sdk._logs`
  (`LoggingHandler(level=0, logger_provider=None)`, `LoggerProvider`, `LogRecordProcessor`,
  `SimpleLogRecordProcessor`, `BatchLogRecordProcessor`, `ReadableLogRecord`) — the leading underscore *is*
  the API-stability signal (https://opentelemetry-python.readthedocs.io/en/latest/sdk/_logs.html).
  (2) `LoggingHandler` was **deprecated in opentelemetry-sdk 1.40.0** "in favor of
  `opentelemetry-instrumentation-logging`" — whose own version is `0.65b0`, i.e. beta
  (VERSION-DEPENDENT (1.40.0)). (3) The **Events API/SDK was removed outright in 1.44.0**: "Removed
  deprecated Events API/SDK. Use `LogRecord` with the `event_name` field set instead" — so code or
  tutorials written against the events module no longer import (VERSION-DEPENDENT (1.44.0))
  (https://github.com/open-telemetry/opentelemetry-python/releases/tag/v1.44.0).

**The house rule (OPEN — a project stance derived from the ESTABLISHED stability facts above; no source
prescribes it).** Adopt OTel **traces and metrics** freely once the application is genuinely
distributed — those are `Stable` in Python. Treat OTel **logs** as pre-stable: keep stdlib `logging` as
the emission surface (§3, §7) and put a bridge in front of it if and when a collector needs the records.
The application developer is not the intended caller of the bridge in any case: "As an application
developer, the Logs Bridge API should not be called by you directly, as it is provided for logging library
authors to build log appenders / bridges" (https://opentelemetry.io/docs/concepts/signals/logs/). For a
single-process app, none of this applies — §8's `contextvars` filter is the whole answer.

**ESTABLISHED — if you do adopt it, pin BOTH version lines.** OTel Python versions its packages on two
tracks that move together: stable **1.44.0** for `opentelemetry-api`/`opentelemetry-sdk`, and beta
**0.65b0** for `opentelemetry-semantic-conventions`, `opentelemetry-instrumentation` and every
`opentelemetry-instrumentation-*`. `opentelemetry-sdk==1.44.0` pins `opentelemetry-api==1.44.0`,
`opentelemetry-semantic-conventions==0.65b0` and `typing-extensions>=4.5.0`; pinning only the `1.x` line
leaves the beta line floating (https://pypi.org/pypi/opentelemetry-sdk/json). All current distributions
declare `Requires-Python >=3.10`.

**ESTABLISHED — Python severities are NOT SeverityNumber 1–5.** The logs data model defines ranges and a
mapping rule: use the range's **lowest** value when the source format offers one level per range
(https://opentelemetry.io/docs/specs/otel/logs/data-model/). An off-by-range mapping makes every record
look like TRACE.

| Python level | numeric | OTel SeverityNumber | OTel range |
|---|---|---|---|
| DEBUG | 10 | **5** | 5–8 DEBUG |
| INFO | 20 | **9** | 9–12 INFO |
| WARNING | 30 | **13** | 13–16 WARN |
| ERROR | 40 | **17** | 17–20 ERROR |
| CRITICAL | 50 | **21** | 21–24 FATAL |

Range 1–4 is TRACE, which Python has no level for. Additionally: "if the log record represents an
erroneous event and the source format does not define a severity or log level concept then it is
recommended to set `SeverityNumber` to ERROR (numeric 17)" (ESTABLISHED, same page).

**ESTABLISHED — trace correlation is a FIELD triple, not an attribute convention.** The OTel LogRecord
data-model fields are Timestamp, ObservedTimestamp, TraceId, SpanId, TraceFlags, SeverityText,
SeverityNumber, Body, Resource, InstrumentationScope, Attributes and EventName. TraceId/SpanId/TraceFlags
and EventName are **first-class fields**, which is why the stdlib-side `otelTraceID` format-string trick
below is a local convenience and not the wire format.

**ESTABLISHED — the stdlib-side injector and the switch that is off by default.**
`opentelemetry-instrumentation-logging` (`LoggingInstrumentor`) injects exactly four LogRecord attributes:
`otelTraceID`, `otelSpanID`, `otelServiceName`, `otelTraceSampled`. **`OTEL_PYTHON_LOG_CORRELATION`
defaults to `false`**, so installing the package and expecting trace ids in log lines — without setting
that variable or passing `set_logging_format=True` — produces nothing. Other knobs:
`OTEL_PYTHON_LOG_FORMAT`, `OTEL_PYTHON_LOG_LEVEL` (default `info`), `OTEL_PYTHON_LOG_HANDLER_LEVEL`
(default `notset`), `OTEL_PYTHON_LOG_AUTO_INSTRUMENTATION` (default `true`); constructor keywords are
`set_logging_format`, `inject_trace_context`, `logging_format`, `log_level`, `log_hook`, `tracer_provider`
(https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/logging/logging.html).

**ESTABLISHED — semantic conventions an emitter must get right (semconv 1.44.0).** These are the names an
agent is most likely to get wrong from memory, because the old spellings are still everywhere:

| emit this (Stable) | never this (Deprecated) | note |
|---|---|---|
| `code.function.name` | `code.function`, `code.namespace` | "The method or function fully-qualified name without arguments"; `code.function` "Value should be included in `code.function.name`", and `code.namespace` folds into it. |
| `code.file.path` | `code.filepath` | "Replaced by `code.file.path`". |
| `code.line.number` | `code.lineno` | "Replaced by `code.line.number`". |
| `code.column.number` | `code.column` | — |
| `code.stacktrace` | — | Stable. |
| `exception.type`, `exception.message`, `exception.stacktrace` | `exception.escaped` | On an exception log record, `exception.type` is "Required if `exception.message` is not set, recommended otherwise" and vice versa; `exception.stacktrace` is Recommended. `exception.escaped` is Deprecated: "It's no longer recommended to record exceptions that are handled and do not escape the scope of a span." |

(https://opentelemetry.io/docs/specs/semconv/registry/attributes/code/;
https://opentelemetry.io/docs/specs/semconv/registry/attributes/exception/;
https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/;
https://opentelemetry.io/docs/specs/semconv/). Two further facts: exception log records should carry an
event name describing the operation "with a `.exception` suffix", and exception recording is migrating off
span events behind an opt-in — instrumentations "SHOULD introduce an environment variable
`OTEL_SEMCONV_EXCEPTION_SIGNAL_OPT_IN`" with `logs` (logs only) or `logs/dup` (both, for a phased
rollout), with span events remaining the default for backward compatibility.

**ESTABLISHED — the whole `log.*` namespace is NOT stable ground for a schema.** `log.record.original`,
`log.record.uid`, `log.file.name`, `log.file.name_resolved`, `log.file.path`, `log.file.path_resolved`
and `log.iostream` are all marked Development, and the general log-conventions document is itself headed
"Development" (https://opentelemetry.io/docs/specs/semconv/general/logs/). Two consequences: do not build
a field schema on them, and note that `log.record.original` is for **collectors, not emitters** — include
it only "when processing a Log Record which was originally transmitted as a string or equivalent data
type AND the Body field of the Log Record does not contain the same value".

### 8c. Signal choice: what belongs in a metric or a span instead of a log line

**ESTABLISHED — logs are the weakest of the three signals for the questions agents most often ask them.**
OTel states the limit directly: "Logs aren't enough for tracking code execution, as they usually lack
contextual information, such as where they were called from. They become far more useful when they are
included as part of a span, or when they are correlated with a trace and a span"
(https://opentelemetry.io/docs/concepts/observability-primer/). The definitions decide the routing: a log
is "a timestamped message emitted by services or other components"; metrics are "aggregations over a
period of time of numeric data about your infrastructure or application"; a span "represents a single unit
of work or operation… contains name, time-related data, structured log messages, and other metadata (that
is, Attributes)"; a trace "records the path taken by a single request… as it propagates through multiple
services" (same page).

| the question you actually have | the right signal | the anti-pattern this replaces |
|---|---|---|
| how many / how often / what rate | **metric** (counter) | `logger.info("processed record %d", n)` per item, then `grep \| wc -l` at 3 a.m. |
| what is the p95 / how long did it take | **metric** (histogram) — or a span, if you need *which* call | logging a duration per call and computing percentiles from text. |
| how much is in the queue / cache / pool right now | **metric** (gauge) | a periodic "status" log line nobody reads until it is missing. |
| where did the time go; which call caused which | **span** | interleaved start/finish log lines reassembled by timestamp. |
| what exactly happened to *this* input, once | **log line** | (correct — this is the log's job.) |
| why did this specific run fail, with the values involved | **log line** at ERROR with traceback (§10) | a counter increment that tells you it happened but not what. |

**Scale discipline (this file's default target).** For a small-to-mid single-process app, adopting a
metrics pipeline to answer counting questions is usually **over-engineering**: the cheap correct answer is
one in-process counter exposed by the diagnostic surface owned by
`python_runtime_diagnostics_manifest.md`, or one summary log line at the end of a run instead of one per
item. What is **not** acceptable is answering a counting question by emitting a log line per event and
grepping — that is a metric implemented in the most expensive medium available. Structured output is the
minimum discipline that keeps the option open: "Structured logs are preferred in production because their
stable schema makes them straightforward to validate, parse, correlate with traces and metrics, and
analyze at scale", while unstructured logs are "not preferred… for production observability purposes"
(ESTABLISHED, https://opentelemetry.io/docs/concepts/signals/logs/).

---

## 9. Performance: lazy `%`-style args and `isEnabledFor`

**ESTABLISHED — lazy `%`-style formatting, in the source's own words.** Use the `%`-style argument form,
e.g. `logging.warning('%s before you %s', 'Look', 'leap!')`. The HOWTO's sentence is "Formatting of
message arguments is deferred until it cannot be avoided"
(https://docs.python.org/3/howto/logging.html). The call form `logger.debug('Message with %s, %s', a, b)`
is what makes that deferral possible; pre-formatting the message defeats it.

**ESTABLISHED — the f-string prohibition is ruff's rule, NOT python.org's.** The stdlib docs never
mention f-strings in this context. The citable authority for "an f-string is evaluated eagerly regardless
of level" is ruff `G004 logging-f-string`, which "Checks for uses of f-strings to format logging
messages" and argues that passing arguments (or `extra`) "is more consistent, more efficient, and less
error-prone than formatting the string directly"
(https://docs.astral.sh/ruff/rules/logging-f-string/). **Cite ruff for the prohibition and python.org for
the deferral** — attributing the f-string rule to python.org is a fabricated citation, and this manifest
previously made that mistake.

**ESTABLISHED — guard expensive arguments with `isEnabledFor`.** When building an argument is itself
costly, gate the whole call:
`if logger.isEnabledFor(logging.DEBUG): logger.debug("Message with %s, %s", expensive1(), expensive2())`
(https://docs.python.org/3/howto/logging.html). This avoids evaluating the expensive arguments when
DEBUG is disabled — which, given the default WARNING threshold (§2), is the common case in production.

**ESTABLISHED — but the level check itself is already memoised inside CPython, so guard for the ARGUMENTS
and nothing else.** `Logger.isEnabledFor` returns `self._cache[level]` on a hit and only recomputes under
`_lock`, checking `self.disabled`, then `self.manager.disable >= level`, then
`level >= self.getEffectiveLevel()`
(https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py). The HOWTO's note
advising callers to cache the result themselves predates that cache. (**Inference, not a documented
statement:** the `_cache` code is verbatim from the source, but the reading that the HOWTO note is thereby
superseded is this manifest's inference.) The practical rule: a hand-rolled `_debug_enabled` boolean buys
almost nothing and goes **stale on reconfiguration** — the interpreter invalidates its own `_cache`, not
yours. Guard only to avoid *building* the arguments.

**CORRECTION (ESTABLISHED) — linters push the OPPOSITE way, and no lint exception is required.** The
earlier claim in this manifest, that mypy/pyright/ruff flag `%`-style args and need an exemption, was
**backwards**. ruff flags the *eager* forms of the message string and leaves the lazy argument form
alone: `G004` f-strings, `G001` `str.format`, `G002` eager `%` **applied to the message**, `G003` `+`
concatenation. In particular `G002 logging-percent-format` targets `logger.info("%s" % x)` — eager
pre-formatting — which is the **opposite** of the recommended `logger.info("%s", x)`; nothing flags the
recommended form (https://docs.astral.sh/ruff/rules/;
https://docs.astral.sh/ruff/rules/logging-f-string/). Do not add a suppression for the correct idiom: a
blanket "exception for %-style logging" would suppress `G002`, a genuine rule. Enable the `LOG` and `G`
families instead — the full mapping is §12a, and `python_linting_practices_manifest.md` owns the rule set.

### 9a. Queue-based handoff: the four defaults that bite

`QueueHandler` + `QueueListener` is the standard way to keep logging off a hot path, and **every default
in it surprises people.** Treat the four facts below as one unit, because they fail together
(https://docs.python.org/3/library/logging.handlers.html — the page documents Python 3.14.7).

1. **ESTABLISHED — `prepare()` is destructive by design, so the structured formatter must live on the
   HANDLER side.** Verbatim: it "overwrites the record's `msg` and `message` attributes with the merged
   message (obtained by calling the handler's `format()` method), and sets the `args`, `exc_info` and
   `exc_text` attributes to `None`", and the documented consequence is that "a handler on the
   `QueueListener` side won't have the information to do custom formatting, e.g. of exceptions." A JSON
   formatter placed on the *listener's* handlers therefore receives a **pre-rendered string, not fields**.
   Put the JSON/structured formatter on the `QueueHandler`, or subclass and override `prepare()` (the docs
   suggest overriding it "to e.g. avoid setting `exc_text` to `None`"). The same ordering constraint
   governs redaction — §11a.
2. **VERSION-DEPENDENT (3.5) — `respect_handler_level` defaults to `False`, so per-handler fan-out
   silently stops working behind a queue.** `QueueListener(queue, *handlers, respect_handler_level=False)`
   ignores handler levels unless you opt in: only "If `respect_handler_level` is `True`, a handler's level
   is respected." The parameter was added in 3.5 and the default kept the legacy behaviour. An agent that
   moves an existing console-INFO / file-DEBUG fan-out (§3, §5) behind a queue will emit **every** record
   to **every** handler and get no warning. Always pass `respect_handler_level=True` unless you mean
   otherwise.
3. **ESTABLISHED — the drop path is real and can be silent.** `QueueHandler.emit` enqueues via
   `put_nowait()`; "Should an exception occur (e.g. because a bounded queue has filled up), the
   `handleError()` method is called to handle the error. This can result in the record silently being
   dropped (if `logging.raiseExceptions` is `False`) or a message printed to `sys.stderr` (if
   `logging.raiseExceptions` is `True`)." So the choice is explicit and unavoidable: a **bounded** queue
   trades record loss for a memory bound, an **unbounded** one (`queue.Queue(-1)`) trades unbounded memory
   for no loss. Pick deliberately, keep `raiseExceptions` `True` (§5a) so a drop is at least visible, and
   record the choice. (OPEN — bound and size are a project decision; nothing in the docs picks for you.)
4. **ESTABLISHED — `stop()` is a correctness requirement, not tidiness.** "Note that if you don't call
   this before your application exits, there may be some records still left on the queue, which won't be
   processed." The records you lose are exactly the ones written during shutdown — i.e. the failure you
   are trying to diagnose. **VERSION-DEPENDENT (3.14):** `QueueListener` is now a context manager — "When
   entering the context, the listener is started. When exiting the context, the listener is stopped.
   `__enter__()` returns the `QueueListener` object" — which is the form to prefer, because it cannot be
   forgotten. Also on 3.14, `QueueListener.start()` "Raises `RuntimeError` if called and the listener is
   already running", so a defensive idempotent-start helper that worked on 3.13 now throws.

**ESTABLISHED — the reason to adopt this in async code is not only "slow handlers".** The cookbook is
explicit: "when logging from async code, network and even file handlers could lead to problems (blocking
the event loop) because some logging is done from `asyncio` internals. It might be best, if any async code
is used in an application, to use the above approach for logging, so that any blocking code runs only in
the `QueueListener` thread." (https://docs.python.org/3/howto/logging-cookbook.html). You cannot avoid
this by disciplining your own call sites, because the emitting code is not all yours.

**ESTABLISHED — with multiple processes, the queue is the supported answer and the type matters.**
"logging to a single file from multiple processes is *not* supported, because there is no standard way to
serialize access to a single file across multiple processes in Python"; the documented alternatives are a
`SocketHandler` plus a receiver, `QueueHandler` with a listener process, or a custom handler using
`multiprocessing.Lock`. With `multiprocessing`, use a `multiprocessing.Queue`, **not** a
`queue.SimpleQueue` (same page). §5b covers why rotation does not rescue the unsupported case.

**Cheaper than a queue, and usually tried too late (ESTABLISHED).** Four module-level flags default to
`True` — `logThreads`, `logMultiprocessing`, `logProcesses`, `logAsyncioTasks` — and setting them `False`
is the documented way to cut per-record cost
(https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py;
https://docs.python.org/3/library/logging.html). `logMultiprocessing=False` in particular skips a
`sys.modules.get('multiprocessing')` lookup and a `current_process()` call **on every record**. In a hot
single-process path that is a real saving agents never consider — and turning off `logAsyncioTasks` also
removes the misleading `taskName` of §8a. Measure before adding a queue;
`python_runtime_diagnostics_manifest.md` owns the measurement tools.

---

## 10. Exceptions: log ONCE at the handling boundary

**ESTABLISHED — `logger.exception()` and `exc_info`.** `logger.exception()` "logs a message with level
ERROR… Exception info is added to the logging message. This method should **only** be called from an
exception handler." `exc_info`: "If exc_info does not evaluate as false, it causes exception information
to be added to the logging message… otherwise, `sys.exc_info()` is called"
(https://docs.python.org/3/library/logging.html). So: use `logger.exception('...')` inside an `except`
block to log at ERROR **with traceback**; use `logger.warning('...', exc_info=True)` (or any level) to
attach a traceback at a **non-ERROR** level. **VERSION-DEPENDENT (3.5):** `exc_info` accepts an exception
**instance** directly, in addition to a `sys.exc_info()` triple or a truthy flag — a closed gate on any
supported interpreter (§5). **VERSION-DEPENDENT (3.2):** `stack_info` is **independent of `exc_info`** and
prints frames under the header "Stack (most recent call last):", from the bottom of the stack up to the
logging call — which is how you capture *how you got here* on a record that has no exception at all
(https://docs.python.org/3/library/logging.html).

**OPEN / best-practice — log once at the handling boundary, not at every re-raise.** The cookbook's
centralize-configuration guidance ("the application code does not care about multiple handlers";
configure once to avoid duplicate output) **supports** the principle, but the docs do not state "log
once at the handling boundary" verbatim
(https://docs.python.org/3/howto/logging-cookbook.html). The design rule: let exceptions **propagate
carrying context** (`raise` / `raise … from …`), and log them **exactly once** with
`logger.exception()` at the layer that actually **handles/swallows** them (or at the top-level
boundary). Re-raising **and** re-logging at every layer produces duplicate stack traces and noise.
**CROSS-REFERENCE `error_tracing_contract_manifest.md`:** that manifest owns the propagation/chaining
contract (`raise … from …`, preserving the original cause); this rule is its natural logging
complement — the error-tracing layer preserves the cause, this layer logs it **once** where it is
handled. Where exactly the "handling boundary" sits in this codebase's layering (per public-API call?
per CLI/HTTP entrypoint?) must be pinned to that sibling manifest (open question).

**REFINEMENT (named, cited) — "log once" is a rule about duplicate TRACEBACKS, not a reason to throw away
what only the error site knows.** Stated flatly, log-once pushes authors to discard detail that exists
nowhere else. The pattern literature names the opposite placement: **Log Errors** — SWE corpus element
`log-errors`, named in Preschern, *Fluent C: Principles, Practices, and Patterns*, O'Reilly, 2022
(ISBN 978-1492097334). As the corpus renders the pattern: "record error details on a separate diagnostic
channel **at the point where the error occurs**, instead of forcing all debug information through return
values to the caller", because "callers need only actionable error information, but programmers debugging
the system need full detail".
The corpus records `log-errors -alternative-to-> return-status-code`. The resolution this manifest adopts
is **two audiences on two levels**:

| where | level | content | audience |
|---|---|---|---|
| at the error site (inside the `except`, before re-raising or returning a typed error) | **DEBUG** | the locals and inputs the boundary can no longer see; **no** traceback | the contributor debugging it |
| at the handling boundary (the layer that swallows it, or the top-level entrypoint) | **ERROR**, exactly once, `logger.exception()` | the traceback and the operational fact | the operator |

That keeps exactly one stack trace per failure while preserving the information that only existed at the
raise site. It costs nothing in production, because DEBUG is silent by default (§2). What remains
forbidden is a *second ERROR with a traceback* at each re-raise. (The two-level split is this manifest's
synthesis of the log-once rule and the cited `log-errors` pattern — **OPEN** as to which layers count as
boundaries in this codebase, per the open question above.)

---

## 11. Security: never log secrets or PII

**ESTABLISHED as OWASP guidance; absent from the python.org logging pages — cite OWASP, not
python.org.** The cited python.org logging pages say nothing about secrets, so do **not** attribute the
rule to them. The citable authority is the **OWASP Logging Cheat Sheet**
(https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), whose "Data to exclude"
list is concrete (ESTABLISHED, as OWASP guidance): application source code, session
identification values, access tokens, "Sensitive personal data and some forms of personally identifiable
information (PII)", authentication passwords, database connection strings, "Encryption keys and other
primary secrets", bank account or payment card holder data, "Data of a higher security classification than
the logging system is allowed to store", commercially-sensitive information, and "Information it is
illegal to collect in the relevant jurisdictions". The last two are the ones a Python-only reading always
misses: the log sink has a classification, and collection can itself be unlawful.

### 11a. Redaction placement: a Filter at the LOGGER, never the Formatter

The previous edition of this section left the mechanism as a coin-flip ("a Filter or a structlog
processor"). The mechanics decide it.

**ESTABLISHED (derived from the documented gating and propagation semantics of §3/§3a rather than from a
single quoted sentence) — coverage ordering: logger-Filter > handler-Filter > Formatter.** A `Filter`
attached to the **logger** sees every record before propagation offers it to *any* handler, so it protects
all sinks including ones added later. A Filter attached to a **handler** protects only that handler. A
**Formatter** protects only the sinks that use it. Since propagation passes records to ancestor handlers
without re-consulting ancestor levels or filters (§3a), the only placement that cannot be bypassed by a
newly-added handler is the logger. **Attach the redaction Filter at the logger** (the application's root
logger for a whole-process guarantee); use a structlog processor placed **before the renderer** in a
structlog pipeline, where a hard deny is `raise structlog.DropEvent` (§7).

**ESTABLISHED — the surface is four things, and `record.msg` is only one of them.** Because `%(message)s`
renders `record.msg % record.args`, rewriting only `record.msg` **leaves the secret in `record.args`**;
and `record.exc_info` / `record.exc_text` embed argument values inside rendered tracebacks. A redaction
implementation must cover:

| field | why it leaks |
|---|---|
| `record.msg` | the obvious one. |
| `record.args` | `%(message)s` is `msg % args`; a masked `msg` with intact `args` still prints the secret. |
| `record.exc_info` / `record.exc_text` | traceback frames carry argument values; `exc_text` is the cached rendering. |
| every `extra` key | arbitrary application fields, including nested dicts a JSON formatter will serialise. |

**ESTABLISHED — ordering: redaction must sit UPSTREAM of any `QueueHandler`.** `QueueHandler.prepare()`
has already merged msg+args and set `args`/`exc_info`/`exc_text` to `None` before the listener thread sees
anything (§9a), so "a handler on the `QueueListener` side won't have the information to do custom
formatting" — a redacting *formatter* on the listener side receives a pre-rendered string and cannot
recover the fields it was supposed to mask
(https://docs.python.org/3/library/logging.handlers.html). Logger-level Filter, then queue, then
listener — in that order.

**ESTABLISHED — log injection is a SEPARATE obligation from secret redaction.** OWASP requires the step
most redaction designs omit: "Perform sanitization on all event data to prevent log injection attacks e.g.
carriage return (CR), line feed (LF) and delimiter characters" (same page). A filter that masks values but
passes a multi-line attacker-controlled string still lets that string **forge whole log entries** in any
line-delimited plain-text sink. Strip or escape CR, LF and the sink's delimiter on every field that can
carry user input. A JSON serialiser escapes control characters inside string values, so a JSON sink is
**less** exposed to entry forgery than a plain-text one — which is a reason to prefer structured output
(§7a), not a reason to skip sanitisation: the field values are still attacker-controlled wherever they are
finally rendered, and non-JSON console handlers usually sit on the same logger. OWASP also asks
for time synchronisation across hosts, which is an operations task, not an application one.

**Reminders that make the above cheaper.** A Filter must `return True` or it drops the record (§8a); and
the strongest form of this rule is still structural — never put a secret into the message or `extra` in
the first place, so redaction is defence in depth rather than the only line. (OPEN — the field allow/deny
list and the masking format are project policy; see open questions.)

### 11b. An audit log is not an application log

**Named vocabulary (ESTABLISHED name, cited).** SWE corpus element `audit-log`, named in Fowler, *Further
Enterprise Application Architecture development* (eaaDev pattern drafts, living). The corpus record notes
that the element's prose additionally names Core Security Patterns (2005) and Schneier & Kelsey (1999)
**with no backing work records** — so only the Fowler attribution is carried here. The distinction the
name buys, in the corpus record's own words (not a quotation from Fowler): "ordinary debug logging is
neither complete, attributable, nor protected against tampering."

If the application has to answer *who did what to which record, and when*, that is a **different log with
different rules**, and satisfying it by grepping the application log is a design error. The four
properties that differ:

| property | application log (§3–§9) | audit log |
|---|---|---|
| level-suppressible | yes — that is the point (§2) | **no.** An audit event is not DEBUG-or-INFO; it must not vanish when someone raises a threshold. |
| schema | useful, evolving | fixed and schema'd: **actor, action, target, time, source** at minimum. |
| write pattern | rotated, purged, best-effort (§5b) | **append-only**, with retention driven by policy, not disk. |
| dropped under load | acceptable (§9a) | **not acceptable** — a dropped audit record is a compliance failure, not a missing hint. |

**Mechanically, in stdlib terms (OPEN — this shape is derived, not prescribed by any source):** a separate
named logger (e.g. `getLogger("audit")`) with **`propagate = False`** so audit records never reach the
application handlers, its own handler and its own formatter, and its own retention. Because it must not be
level-suppressible, do **not** rely on the level to gate it: emit at a single fixed level and let the
dedicated handler take everything. Whether this application needs an audit log at all, what the retention
is, and whether tamper-evidence (append-only storage, signing) is in scope are project decisions — see
open questions. **Scale discipline:** for a small single-process tool with no multi-user surface, an audit
log is usually **over-engineering** — but if you find yourself reconstructing who-did-what from the
application log, you have already needed one.

---

## 12. Strict-typing notes

- **CORRECTED (ESTABLISHED) — `%`-style lazy args need NO lint exception.** The earlier text here claimed
  mypy/pyright/ruff flag the lazy argument form and that a suppression must be agreed. That is backwards:
  ruff flags the *eager* message forms (`G001`–`G004`) and leaves `logger.debug("...%s", value)` alone
  (§9, §12a). Do not configure an exemption; it would suppress `G002`, which catches the genuinely wrong
  `logger.info("%s" % x)`.
- **Typing around loggers and adapters.** `logging.getLogger(__name__)` returns a `logging.Logger`;
  `LoggerAdapter` is generic over the underlying logger. Keep the `extra=`/adapter context dicts typed
  where the strict-typing posture in `python_typing_contract_manifest.md` requires it. Note what the type
  checker **cannot** catch here: the reserved-key `KeyError` (§7), a format string demanding a field that
  a call site omits (§7), a Filter that forgets `return True` (§8a), and every string that lands in a log
  message. `extra=` is typed as a mapping; its *keys* are not checked against `LogRecord`. That gap is
  exactly what §12a's lint rules exist to close, and where they cannot, the routing says
  **contract-only**.
- **Version-gated APIs (VERSION-DEPENDENT) — routed to the hub.** The support matrix lives in
  `python_platform_baseline_manifest.md`; the behaviour-relevant gates for this file are listed once, in
  §5, and cited again at each point of use. Do not maintain a second list here.

### 12a. The lint contract: what mechanically enforces the rules in this file

**The governing test.** A rule stated in a manifest and not mechanically enforced decays to zero. Below,
every rule this file states is routed either to an exact ruff rule code or to an honest **contract-only**.
`python_linting_practices_manifest.md` **owns the rule set** — which families are enabled, severity, and
suppression hygiene; `python_quality_gates_manifest.md` owns where the check runs and how it fails. This
table is only the mapping from *this manifest's* rules to the codes that enforce them.

**ESTABLISHED — all of the following are stable ruff rules, none in preview**
(https://docs.astral.sh/ruff/rules/; https://docs.astral.sh/ruff/rules/logging-f-string/):

| rule stated here | § | mechanical enforcer | route |
|---|---|---|---|
| Never log to the root logger | §4 | `LOG015 root-logger-call` | lint-catchable |
| Always obtain loggers via `getLogger()`, never `Logger(...)` | §3a | `LOG001 direct-logger-instantiation` | lint-catchable |
| `getLogger(__name__)`, not `getLogger(__file__)` or an expression | §3a | `LOG002 invalid-get-logger-argument` | lint-catchable |
| Lazy args: no f-string in a log call | §9 | `G004 logging-f-string` | lint-catchable |
| Lazy args: no `str.format`, no eager `%`, no `+` on the message | §9 | `G001`, `G002 logging-percent-format`, `G003` | lint-catchable |
| `extra` keys must not collide with `LogRecord` attributes | §7 | `G101 logging-extra-attr-clash` (the static form of the runtime `KeyError`) | lint-catchable |
| Exception logging belongs inside an `except` handler | §10 | `LOG004 log-exception-outside-except-handler`, `LOG014 exc-info-outside-except-handler` | lint-catchable |
| `logger.exception()` carries the traceback; don't hand-roll `exc_info` | §10 | `G201 logging-exc-info`, `G202 logging-redundant-exc-info`, `LOG007 exception-without-exc-info` | lint-catchable |
| Never call the deprecated `.warn()` | §2c | `LOG009 undocumented-warn`, `G010 logging-warn` | lint-catchable |

**Contract-only — nothing mechanical catches these. Say so rather than implying coverage:**

| rule stated here | § | why no tool catches it |
|---|---|---|
| No `basicConfig` / no non-Null handler / no `logging.disable()` in library code | §4, §2c | These are legal API calls; only review or a project-specific fitness function distinguishes library from application code. |
| `QueueListener(..., respect_handler_level=True)` | §9a | A default-valued keyword; no rule knows you wanted the non-default. |
| `QueueListener.stop()` is called (or the 3.14 context-manager form is used) | §9a | Lifetime discipline; a test that asserts drain-on-exit is the only mechanical catch — **test-catchable**. |
| Redaction Filter attached at the logger, upstream of the queue | §11a | Placement, not syntax. A test that logs a canary secret through the configured pipeline and asserts it is masked is the mechanical form — **test-catchable**. |
| Log injection: CR/LF/delimiter sanitisation | §11a | Data-dependent. Same canary-test route. |
| `disable_existing_loggers: False` in `dictConfig` | §5a | A missing key with a surprising default; a config-schema test can assert it — **test-catchable**. |
| Secrets never entering a message in the first place | §11 | Semantic. Review plus the canary test. |
| Choosing the right *signal* (metric vs span vs log) | §8c | A design judgement; no tool has the intent. |
| Level choice (INFO vs WARNING vs ERROR) | §2, §2b | Semantic. Review only. |

**Settled (2026-08-08):** enable the `LOG` and `G` families wholesale. The remaining decision is only
which of `LOG004`/`LOG007`/`LOG014` to enforce as errors given where this codebase draws its log-once
boundary (§10) — see open questions.

---

## 13. Checklists

### Library / reusable-component author checklist
- [ ] `logger = logging.getLogger(__name__)` at module top — never instantiate `Logger` directly. (ESTABLISHED)
- [ ] **Never** log to the root logger. (ESTABLISHED)
- [ ] **Never** call `basicConfig` or otherwise configure root. (ESTABLISHED)
- [ ] Add **no handlers** except a single `logging.NullHandler()` on the **top-level package** logger. (ESTABLISHED)
- [ ] No logging side-effects at import beyond `getLogger(__name__)` and the top-level `NullHandler`. (best-practice / OPEN-wording)
- [ ] Emit DEBUG/INFO at seams with descriptive context (goal1); leave WARNING/ERROR/CRITICAL for genuine operational events (goal2). (ESTABLISHED)
- [ ] Use lazy `%`-style args; guard expensive args with `isEnabledFor`; do not use f-strings in hot paths. (ESTABLISHED)
- [ ] Log exceptions **once**, at the handling boundary, with `logger.exception()`; let them propagate carrying context elsewhere (cross-ref `error_tracing_contract_manifest.md`). (OPEN/best-practice)
- [ ] Never put secrets/PII into messages or `extra`. (ESTABLISHED as OWASP guidance; §11)
- [ ] Do **not** call `structlog.configure()` in component code. (OPEN/project-policy)
- [ ] Namespace every `extra` key — a collision with a `LogRecord` attribute raises `KeyError` at the call site. (ESTABLISHED; §7)
- [ ] Never call `logging.disable()`, and never define a custom level: both are process-wide mutations you do not own. (ESTABLISHED; §2c)
- [ ] Never call the deprecated `.warn()`; its `DeprecationWarning` is invisible under default filters. (ESTABLISHED; §2c)
- [ ] Pass `stacklevel=2` (or more) from any logging helper or wrapper, or every record names the helper's own file and line. (VERSION-DEPENDENT 3.8; §5)
- [ ] Do not rely on `%(taskName)s` — it renders the literal `None` in sync code and outside a running loop. (VERSION-DEPENDENT 3.12; §8a)

### Application / consumer author checklist
- [ ] Configure logging **once at startup** (prefer `dictConfig` for any multi-handler setup; `basicConfig` for the trivial case). (ESTABLISHED)
- [ ] Attach handlers to the **root** logger and let propagation route component records. (ESTABLISHED)
- [ ] Set the root/logger level to the **lowest** severity you want to capture; fan out via **per-handler levels** (e.g. console INFO, file/JSON DEBUG). (ESTABLISHED)
- [ ] Choose console vs file/JSON handlers; add a JSON formatter (`pythonjsonlogger.json.JsonFormatter` from python-json-logger 4.1.0, or `structlog.stdlib.ProcessorFormatter`) for goal2 machine consumption — there is still **no JSON formatter in the stdlib** as of 3.15.0rc1. If any handler sits behind a `QueueHandler`, put the JSON formatter on the **QueueHandler**, not on the listener's handlers, and pass `QueueListener(..., respect_handler_level=True)` — it defaults to `False`, which silently ignores per-handler levels. (ESTABLISHED / VERSION-DEPENDENT 3.5, 3.15; §7a, §9a)
- [ ] Set `disable_existing_loggers: False` explicitly in `dictConfig`, and include `version: 1`. (ESTABLISHED; §5a)
- [ ] Inject correlation/trace IDs via a `contextvars` Filter or `structlog.contextvars` (`clear`/`bind`/`merge_contextvars`); read every `ContextVar` **with a default** so the Filter cannot raise `LookupError`; re-bind at worker-thread entry, because contextvars do not cross into threads. (ESTABLISHED; §8, §8a)
- [ ] Adopt OpenTelemetry traces/metrics only if distributed; treat OTel **logs** as pre-stable in Python and keep stdlib `logging` as the emission surface. (ESTABLISHED; §8b)
- [ ] Add the redaction Filter **at the logger**, upstream of any `QueueHandler`, covering `msg`, `args`, `exc_info`/`exc_text` and every `extra` key; sanitise CR/LF/delimiters separately. (ESTABLISHED; §11a)
- [ ] Bound the log accumulator: a rotating handler with non-zero `maxBytes` **and** `backupCount` (or `logrotate`), never both on one path. (ESTABLISHED; §5b)
- [ ] If a queue is used: `respect_handler_level=True`, a deliberate bounded-vs-unbounded choice, `raiseExceptions` left `True`, and `stop()` guaranteed (prefer the 3.14 context-manager form). (ESTABLISHED / VERSION-DEPENDENT 3.14; §9a)
- [ ] Enable ruff's `LOG` and `G` families; add **no** exception for `%`-style args. (ESTABLISHED; §12a)
- [ ] Route `warnings` into logging with `captureWarnings(True)` and configure the `'py.warnings'` logger. (ESTABLISHED; §2b)
- [ ] Claim `sys.excepthook`, `threading.excepthook` and `sys.unraisablehook` at startup, or lose those exceptions to stderr. (ESTABLISHED / VERSION-DEPENDENT 3.8; §14)
- [ ] Decide whether an audit log is in scope; if so, a separate logger with `propagate = False` and its own retention. (OPEN; §11b)

---

## 14. Diagnosis beyond logging (cross-reference stub)

Four failure classes cannot be diagnosed from log output at all, and adding log lines is the wrong move
for every one: a **fatal signal** (the process is gone before a handler flushes), a **hang** (silence *is*
the symptom), a **leak** (the records look normal; memory does not), and **"it is slow"** (logging the
durations changes them). The stdlib answers — `faulthandler`, `sys._current_frames()`, `tracemalloc`, and
`profiling.sampling` / `cProfile` — belong with their version gates and hazards to
**`python_runtime_diagnostics_manifest.md`**. (VERSION-DEPENDENT: `profiling.sampling` is 3.15.)

One overlap is this file's business, because a logging setup either claims it or loses the records
permanently: **three interpreter hooks must be routed into logging at startup** — `sys.excepthook`
(uncaught on the main thread), `threading.excepthook` (escaping `Thread.run()`), and `sys.unraisablehook`
(exceptions the interpreter cannot raise: `__del__`, weakref callbacks, GC). All three default to printing
on **stderr**, so in a JSON-only or file-only deployment they are simply lost. (ESTABLISHED for the first
two; VERSION-DEPENDENT (3.8) for `unraisablehook`, whose handler hazards the diagnostics manifest owns.)

---

## 15. Anti-patterns (rejection list)

One line each; the § names the rule violated.

- Enumerating six severities including NOTSET, or calling `logger.log(logging.NOTSET, ...)`. → §2, §2a
- Quoting "both the library reference and the HOWTO" for one wording of the level table. → §2
- Setting `handler.setLevel(logging.NOTSET)` expecting "inherit"; it means *handle everything*. → §2a
- Comparing `getLevelName(30)` against `'WARN'`; it can only ever return `'WARNING'`. → §2c
- Calling `logger.warn()`; the deprecation is invisible under default warning filters. → §2c
- Defining a custom level at an existing numeric value; the built-in name is destroyed. → §2c
- Calling `logging.disable()` from a library or leaving it set after a test. → §2c
- Raising the **root** logger's level to quiet a chatty child; propagation does not re-check ancestors. → §3a
- Attaching a handler to both a logger and an ancestor, then debugging "duplicate log lines". → §3a
- Logging to the root logger, or calling `basicConfig`, from a reusable component. → §4
- Justifying a `NullHandler` with "No handlers could be found for logger XXX" (pre-3.2 artefact). → §4
- Presenting the `NullHandler` as obligatory; the docs frame it conditionally. → §4
- Omitting `version: 1` from a `dictConfig` dict, or writing `version: 2`. → §5a
- Calling `dictConfig` after imports without `disable_existing_loggers: False`. → §5a
- Expecting two `dictConfig` calls to merge; `incremental` defaults to `False`. → §5a
- Exposing `logging.config.listen()`; it passes configuration through `eval()`. → §5a
- Setting `logging.raiseExceptions = False` for tidiness, converting handler faults into silence. → §5a
- A file handler with no rotation and no retention, in a process that runs for weeks. → §5b
- Rotating one file from several processes. → §5b, §9a
- `extra={"module": ...}` / `{"name": ...}` / `{"taskName": ...}`; each raises `KeyError`. → §7
- A format string with `%(request_id)s` and no Filter supplying a default. → §7
- Relying on `LoggerAdapter` to merge call-site `extra` before 3.13's `merge_extra=True`. → §7
- Writing `logging.JSONFormatter` or `class: logging.JsonFormatter`; neither exists. → §7a
- Importing `pythonjsonlogger.jsonlogger`, or passing dotted-path strings for `json_default`. → §7a
- Reordering a structlog chain: `merge_contextvars` not first, `wrap_for_formatter` not last. → §7
- A second `structlog.configure()` expected to take effect under `cache_logger_on_first_use=True`. → §7
- `ContextVar.get()` with no default inside a Filter. → §8a
- Assuming a correlation id bound on the request thread is visible in a `ThreadPoolExecutor` worker. → §8a
- Using `%(taskName)s` as a correlation key. → §8a
- A Filter that stamps fields and forgets `return True`. → §8a
- "OpenTelemetry logs are stable" — true of the spec, false of the Python implementation. → §8b
- Importing from `opentelemetry.sdk._logs` in a production path, or from the removed Events API. → §8b
- Pinning only the `1.x` OTel line and letting the `0.65b0` beta line float. → §8b
- Mapping Python's five levels onto SeverityNumber 1–5. → §8b
- Emitting `code.function`, `code.filepath`, `code.lineno`, `code.namespace`, or `exception.escaped`. → §8b
- Building a field schema on the Development-status `log.*` namespace. → §8b
- Installing `opentelemetry-instrumentation-logging` and expecting trace ids without `OTEL_PYTHON_LOG_CORRELATION`. → §8b
- Answering a counting or percentile question by emitting one log line per event and grepping. → §8c
- f-strings in log calls — and equally, adding a lint exemption for the correct `%`-args form. → §9, §12a
- Attributing the f-string prohibition to python.org rather than ruff `G004`. → §9
- Hand-rolling a cached `_debug_enabled` boolean; CPython already memoises the level check. → §9
- A JSON or redacting formatter on the **listener** side of a queue. → §9a, §11a
- `QueueListener(...)` without `respect_handler_level=True` after moving a fan-out behind a queue. → §9a
- Letting a process exit without `QueueListener.stop()`. → §9a
- A defensive second `QueueListener.start()`; it raises `RuntimeError` on 3.14+. → §9a
- Adding a queue before trying `logMultiprocessing = False` on a hot path. → §9a
- Logging an ERROR with a traceback at every re-raise. → §10
- Discarding the error site's locals because "we log once at the boundary". → §10
- Redacting in a Formatter, or masking `record.msg` while leaving `record.args` intact. → §11a
- Masking secrets but not sanitising CR/LF, leaving log-entry forgery open. → §11a
- Reconstructing who-did-what from the application log instead of an audit log. → §11b
- Adding more log lines to diagnose a hang, a leak, a fatal signal, or "it is slow". → §14
- Leaving `sys.excepthook`, `threading.excepthook` and `sys.unraisablehook` unclaimed in a file-only deployment. → §14

---

## Open questions

Each is a **decision the project must make and record**; none has an authoritative source that decides
it. Tagged **OPEN** throughout, and addressed per the discipline in
`software_spec_discipline_manifest.md` §G5.

1. **structlog/JSON mandate for goal2?** Mandate structlog/JSON, or keep stdlib-only as the baseline
   with structlog optional? structlog gives no library-vs-app guidance, so "components never call
   `structlog.configure()`" is **project policy**, not vendor doctrine. If JSON is mandated, §7a's
   choice between `pythonjsonlogger.json.JsonFormatter` and `structlog.stdlib.ProcessorFormatter` must be
   made once, per handler, and written down.
2. **Where is the "handling boundary"?** The log-once rule (§10) needs the boundary pinned to this
   codebase's layering (per public-API call? per CLI/HTTP entrypoint?) against
   `error_tracing_contract_manifest.md`. This also decides which of `LOG004`/`LOG007`/`LOG014` are
   enforced as errors (§12a) — the only lint question this manifest leaves open.
3. **Correlation-ID transport in scope?** stdlib `contextvars` filter, `structlog.contextvars`, or full
   OpenTelemetry trace/span propagation — adopt OTel only if the app is actually distributed/multi-service,
   and even then treat OTel **logs** as pre-stable in Python (§8b).
4. **Secret-redaction field lists and masking format.** *Settled by §11a:* the mechanism is a Filter at
   the logger (or a structlog processor before the renderer), upstream of any queue, covering `msg`,
   `args`, `exc_info`/`exc_text` and `extra`. Still open: which keys are denied, what the mask looks like
   (fixed token? length-preserving? hashed for correlation?), and whether a canary-secret test is a
   required gate (§12a routes it as test-catchable).
5. **Log retention and rotation policy (§5b).** Size- or time-triggered; `maxBytes`/`backupCount` or
   `when`/`interval`/`backupCount`; handler-side or `logrotate`; and the retention window. Nothing in the
   docs picks for you, and the defaults (`maxBytes=0`, `backupCount=0`) rotate nothing.
6. **Queue bound (§9a).** Bounded (records may drop under load) or unbounded (memory may grow)? A
   deliberate answer, plus keeping `raiseExceptions` `True` so a drop is visible, is required before a
   queue goes into a production path.
7. **Is an audit log in scope (§11b)?** If yes: its schema (actor/action/target/time/source), its
   retention, whether tamper-evidence is required, and where its records go — none of which the
   application log's policy can answer.
8. **Interpreter floor.** *Routed, not open here:* the supported range is owned by
   `python_platform_baseline_manifest.md`. What this file needs from that decision is only whether the
   floor is ≥3.12 (which unlocks `taskName`, queue configuration via `dictConfig`, and
   `getHandlerByName`) and ≥3.14 (the `QueueListener` context manager, `Token` as a context manager, and
   the gh-79366 handler-removal fix). See §5.

**Retired questions**, kept visible so they are not re-opened:

- *"Strict-typing tooling stance on `%`-style lazy args."* **Settled 2026-08-08:** enable ruff's `LOG` and
  `G` families and add **no** exception. ruff flags f-strings (`G004`), `str.format` (`G001`), eager `%`
  on the message (`G002`) and `+` concatenation (`G003`), and does **not** flag the lazy
  `logger.debug("...%s", value)` form. The earlier assumption to the contrary was wrong (§9, §12a).
- *"Which version-gated logging APIs to freeze."* **Settled:** the pre-3.10 gates have closed; the list
  that still matters is in §5 and the support matrix belongs to the hub.

---

## Sources (re-verified 8 Aug 2026)

Version and support-phase facts are **not** sourced here; they belong to
`python_platform_baseline_manifest.md`. What follows are the behaviour sources this file rests on.

**Python standard library**

- Python `logging` — Logging facility (library reference): level constants and numeric values, NOTSET
  sentinel semantics (both the logger and the handler meaning), the level table wording, four object
  types, two-stage thresholds, `getLogger` singleton rule, dotted hierarchy, propagation defaults and the
  duplicate-emission note, `exception()`/`exc_info`, the `extra`-clash and missing-key wording,
  `isEnabledFor`/`getEffectiveLevel`/`setLevel`/`disable`, `getLevelName`/`getLevelNamesMapping`,
  `lastResort`, `raiseExceptions`, `getHandlerByName`/`getHandlerNames`, `captureWarnings` and the
  `'py.warnings'` logger, `LoggerAdapter(merge_extra=)` —
  https://docs.python.org/3/library/logging.html . Accessed 17 Jun 2026; re-verified 8 Aug 2026.
- Python `logging` HOWTO: when-to-use table, default WARNING level, print vs `warnings.warn` vs logging,
  effective-level walk-up, "Configuring Logging for a Library" (no root logging, no non-Null handlers, no
  `basicConfig`, and the **conditional** `NullHandler` framing plus "is regarded as the best default
  behaviour"), logger-name intuition, and the Optimization section ("Formatting of message arguments is
  deferred until it cannot be avoided", the `isEnabledFor` example) —
  https://docs.python.org/3/howto/logging.html . Accessed 17 Jun 2026; re-verified 8 Aug 2026.
- Python `logging` Cookbook: `LoggerAdapter`/`extra=` and `process()` silently overwriting call-site
  `extra`, Filters that modify records, the `contextvars` `InjectingFilter` correlation recipe, centralized
  configuration / avoid-duplicate-output guidance, the `QueueHandler`/`QueueListener` recipe and the
  asyncio event-loop-blocking paragraph, and the unsupported multi-process single-file statement —
  https://docs.python.org/3/howto/logging-cookbook.html . Accessed 17 Jun 2026; re-verified 8 Aug 2026.
- Python `logging.handlers` (page documents 3.14.7): current `NullHandler` wording and `createLock()`
  returning `None`; `RotatingFileHandler` and `TimedRotatingFileHandler` signatures with the
  `maxBytes`/`backupCount`/`when`/`interval`/`utc`/`atTime` semantics and the "rollover never occurs"
  default; `QueueHandler.prepare()` destructiveness verbatim, `enqueue()` via `put_nowait()` and the
  `handleError` drop path; `QueueListener` `respect_handler_level=False`, the 3.14 context-manager form,
  `start()` raising `RuntimeError`, and the `stop()` drain warning —
  https://docs.python.org/3/library/logging.handlers.html . Accessed 17 Jun 2026; re-verified and
  re-loaded 8 Aug 2026.
- Python `logging.handlers` (3.14-pinned URL, used to resolve a wording discrepancy between the
  `prepare()` body and its Note: the body says `args`, **`exc_info`** and `exc_text` are set to `None`) —
  https://docs.python.org/3.14/library/logging.handlers.html . Accessed 8 Aug 2026.
- Python `logging.config`: `version` "The only valid value at present is 1"; `disable_existing_loggers`
  defaulting to `True` and ignored when `incremental`; `incremental` defaulting to `False`; the `'()'`
  factory key and `'.'` attribute key; filters-as-instances (3.11); QueueHandler/QueueListener config and
  formatter `defaults` (3.12); the `listen()` `eval()` warning and `verify` semantics —
  https://docs.python.org/3/library/logging.config.html . Accessed 8 Aug 2026.
- Python `logging` (3.15-pinned): confirms **no stdlib JSON formatter** as of 3.15.0rc1 — the documented
  formatter classes are `Formatter` and `BufferingFormatter` — and no 3.15 logging changes —
  https://docs.python.org/3.15/library/logging.html . Accessed 8 Aug 2026.
- CPython `Lib/logging/__init__.py` (3.14 branch): the level constants with `WARN = WARNING` /
  `FATAL = CRITICAL`, `_levelToName` vs `_nameToLevel`, `Logger.makeRecord` with the exact
  `KeyError("Attempt to overwrite %r in LogRecord")`, `Logger.warn`'s `DeprecationWarning`,
  `logThreads`/`logMultiprocessing`/`logProcesses`/`logAsyncioTasks = True`, the `LogRecord.__init__`
  `taskName` derivation, `Logger.isEnabledFor` with `self._cache`, `raiseExceptions = True` —
  https://raw.githubusercontent.com/python/cpython/3.14/Lib/logging/__init__.py . Accessed 8 Aug 2026.
- CPython 3.14 changelog: gh-79366, the handler-removed-during-emit race fix —
  https://docs.python.org/3.14/whatsnew/changelog.html . Accessed 8 Aug 2026.
- Python `contextvars`: "Each thread has its own effective stack of `Context` objects"; `ContextVar`
  behaving like `threading.local()` across threads; the `get()` `LookupError` rule; `Token` usable as a
  context manager (3.14) — https://docs.python.org/3/library/contextvars.html . Accessed 8 Aug 2026.
- Python `asyncio` Tasks: "If no `context` is provided, the Task copies the current context and later runs
  its coroutine in the copied context"; the `context=` parameter (3.11) —
  https://docs.python.org/3/library/asyncio-task.html . Accessed 8 Aug 2026.

**Lint (the enforcement rung)**

- ruff `G004 logging-f-string` — the citable authority for the f-string prohibition, with its `extra`
  rationale; stable rule — https://docs.astral.sh/ruff/rules/logging-f-string/ . Accessed 8 Aug 2026.
- ruff rules index — the `LOG` family (`LOG001`, `LOG002`, `LOG004`, `LOG007`, `LOG009`, `LOG014`,
  `LOG015`) and the `G` family (`G001`–`G004`, `G010`, `G101`, `G201`, `G202`), all stable, none preview —
  https://docs.astral.sh/ruff/rules/ . Accessed 8 Aug 2026.

**Structured logging libraries**

- structlog — overview (processors, bound loggers, JSON/logfmt/console renderers) —
  https://www.structlog.org/en/stable/ . Accessed 17 Jun 2026.
- structlog — Processors: the `(logger, method_name, event_dict)` signature, the first/last processor
  rules and allowed return types, `structlog.DropEvent` semantics —
  https://www.structlog.org/en/stable/processors.html . Accessed 8 Aug 2026.
- structlog — Context Variables (`clear_contextvars`/`bind_contextvars`/`merge_contextvars`) —
  https://www.structlog.org/en/stable/contextvars.html . Accessed 17 Jun 2026.
- structlog — Standard Library integration (`LoggerFactory`, `BoundLogger`, `ProcessorFormatter` with
  `foreign_pre_chain`, mandatory `wrap_for_formatter`, `remove_processors_meta` first; `ExtraAdder`;
  `cache_logger_on_first_use` freezing configuration) —
  https://www.structlog.org/en/stable/standard-library.html . Accessed 17 Jun 2026; re-verified
  8 Aug 2026.
- structlog changelog — 26.1.0: Python 3.8/3.9 removed, 3.15 support added,
  `BoundLogger.is_enabled_for()`/`get_effective_level()` added, `CallsiteParameter.QUAL_MODULE` added,
  better-exceptions deprecated —
  https://raw.githubusercontent.com/hynek/structlog/main/CHANGELOG.md . Accessed 8 Aug 2026.
- python-json-logger on PyPI — 4.1.0 current, `Requires-Python >=3.10`, "Development Status :: 6 -
  Mature", maintained (not abandoned) — https://pypi.org/pypi/python-json-logger/json . Accessed
  8 Aug 2026.
- python-json-logger changelog — the `pythonjsonlogger.jsonlogger` → `pythonjsonlogger.json` move (3.1.0),
  `RESERVED_ATTRS`/`merge_record_extra` relocated to `pythonjsonlogger.core`, and 4.0.0 removing
  string-valued `json_default`/`json_encoder`/`json_serializer` —
  https://nhairs.github.io/python-json-logger/latest/changelog/ . Accessed 8 Aug 2026.

**OpenTelemetry (the adoption gate, §8b)**

- OTel specification index — specification version 1.59.0 — https://opentelemetry.io/docs/specs/otel/ .
  Accessed 8 Aug 2026.
- OTel spec status — Logging Bridge API, Logging SDK and logs OTLP all `stable` —
  https://opentelemetry.io/docs/specs/status/ . Accessed 8 Aug 2026.
- OTel implementation status — **Python: Traces Stable, Metrics Stable, Logs Development**, Profiles not
  implemented — https://opentelemetry.io/status/ . Accessed 8 Aug 2026.
- OTel Python language page — "Traces [Stable], Metrics [Stable], Logs [Development]"; supports Python
  3.10 and higher — https://opentelemetry.io/docs/languages/python/ . Accessed 8 Aug 2026.
- OTel Logs API spec — "Stable, except where otherwise specified"; the API is "provided for logging
  library authors to build log appenders" — https://opentelemetry.io/docs/specs/otel/logs/api/ .
  Accessed 8 Aug 2026.
- OTel Logs Data Model — Status Stable; the LogRecord field list; the SeverityNumber ranges
  (1–4/5–8/9–12/13–16/17–20/21–24), the lowest-value-in-range mapping rule, and "SeverityNumber to ERROR
  (numeric 17)" — https://opentelemetry.io/docs/specs/otel/logs/data-model/ . Accessed 8 Aug 2026.
- OTel logs concept page — "As an application developer, the Logs Bridge API should not be called by you
  directly"; the structured-vs-unstructured preference; automatic log/trace correlation —
  https://opentelemetry.io/docs/concepts/signals/logs/ . Accessed 8 Aug 2026.
- OTel observability primer — the definitions of log, metrics, span and trace, and "Logs aren't enough for
  tracking code execution…" — https://opentelemetry.io/docs/concepts/observability-primer/ . Accessed
  8 Aug 2026.
- OTel semantic conventions index — semconv version 1.44.0 —
  https://opentelemetry.io/docs/specs/semconv/ . Accessed 8 Aug 2026.
- OTel semconv `code.*` registry — Stable `code.function.name`, `code.file.path`, `code.line.number`,
  `code.column.number`, `code.stacktrace`; Deprecated `code.function`, `code.filepath`, `code.lineno`,
  `code.column`, `code.namespace` with their replacement notes —
  https://opentelemetry.io/docs/specs/semconv/registry/attributes/code/ . Accessed 8 Aug 2026.
- OTel semconv `exception.*` registry — `exception.type`/`exception.message`/`exception.stacktrace`
  Stable; `exception.escaped` Deprecated with its rationale —
  https://opentelemetry.io/docs/specs/semconv/registry/attributes/exception/ . Accessed 8 Aug 2026.
- OTel semconv exceptions-on-logs — the type-or-message conditional requirement, the `.exception`
  event-name suffix, and `OTEL_SEMCONV_EXCEPTION_SIGNAL_OPT_IN` (`logs`, `logs/dup`) —
  https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/ . Accessed 8 Aug 2026.
- OTel semconv general logs — Status Development for the whole `log.*` namespace, and the collector-only
  guidance for `log.record.original` — https://opentelemetry.io/docs/specs/semconv/general/logs/ .
  Accessed 8 Aug 2026.
- opentelemetry-python 1.44.0 release — Events API/SDK removed ("Use `LogRecord` with the `event_name`
  field set instead") — https://github.com/open-telemetry/opentelemetry-python/releases/tag/v1.44.0 .
  Accessed 8 Aug 2026.
- opentelemetry-python CHANGELOG — 1.40.0 "deprecate `LoggingHandler` in favor of
  `opentelemetry-instrumentation-logging`" —
  https://raw.githubusercontent.com/open-telemetry/opentelemetry-python/main/CHANGELOG.md . Accessed
  8 Aug 2026.
- opentelemetry-sdk on PyPI — 1.44.0 pins `opentelemetry-api==1.44.0`,
  `opentelemetry-semantic-conventions==0.65b0`, `typing-extensions>=4.5.0`; `Requires-Python >=3.10` —
  https://pypi.org/pypi/opentelemetry-sdk/json . Accessed 8 Aug 2026.
- opentelemetry-python SDK logs API reference — the private `opentelemetry.sdk._logs` module path and
  `LoggingHandler(level=0, logger_provider=None)` —
  https://opentelemetry-python.readthedocs.io/en/latest/sdk/_logs.html . Accessed 8 Aug 2026.
- opentelemetry-instrumentation-logging reference — the four injected attributes (`otelTraceID`,
  `otelSpanID`, `otelServiceName`, `otelTraceSampled`), `OTEL_PYTHON_LOG_CORRELATION` defaulting to
  `false`, and the other environment variables and constructor keywords —
  https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/logging/logging.html .
  Accessed 8 Aug 2026.

**Security**

- OWASP Logging Cheat Sheet — the "Data to exclude" list verbatim, and the log-injection sanitisation
  requirement (CR/LF/delimiter characters) plus time synchronisation —
  https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . Accessed 8 Aug 2026.

**Named vocabulary (SWE corpus elements, cited to their naming works)**

- `diagnostic-logger`, `diagnostic-context` — Harrison, "Patterns for Logging Diagnostic Messages", in
  Martin, R. C., Riehle, D. & Buschmann, F. (eds.), *Pattern Languages of Program Design 3*, 1997,
  Addison-Wesley, ISBN 978-0-201-31011-5. Verified in the corpus. Accessed 8 Aug 2026.
- `correlation-identifier` — Hohpe, G. & Woolf, B., *Enterprise Integration Patterns*, 2003. Verified in
  the corpus. Accessed 8 Aug 2026.
- `log-errors` — Preschern, C., *Fluent C: Principles, Practices, and Patterns*, O'Reilly, 2022,
  ISBN 978-1492097334. Verified in the corpus. Accessed 8 Aug 2026.
- `audit-log` — Fowler, M., *Further Enterprise Application Architecture development* (eaaDev pattern
  drafts), living. Verified in the corpus; the element's prose also names Core Security Patterns (2005)
  and Schneier & Kelsey (1999), which have **no backing work records** and are therefore not cited here.
  Accessed 8 Aug 2026.
- `steady-state` — Nygard, M., *Release It!*. **UNVERIFIED / FLAGGED-SECONDARY:** the corpus's
  bibliographic record carries `year: UNRESOLVED, verification: unverified`, so the name is imported but
  the citation is not presented as verified ground truth. Accessed 8 Aug 2026.

### Sibling manifests (cross-referenced, not duplicated)

- `python_platform_baseline_manifest.md` — **the version hub.** CPython release dates, support phases,
  PEP-status-by-version, interpreter switches. Every "when" in this file resolves there.
- `error_tracing_contract_manifest.md` — the error contract: the two propagation channels, exception
  chaining and cause preservation, exhaustiveness, and errors as a version-stable public API. This file
  owns only how an error is *logged* (§10).
- `python_runtime_diagnostics_manifest.md` — everything that inspects a running or crashed process:
  `faulthandler`, thread dumps, `tracemalloc`, profilers, post-mortem, self-test and health surfaces
  (§14). Logs and telemetry stay here; live diagnosis goes there.
- `python_linting_practices_manifest.md` — **owns the rule set.** Which lint families are enabled, at what
  severity, and suppression hygiene. §12a states only the mapping from this file's rules to rule codes.
- `python_quality_gates_manifest.md` — owns where a check runs, how it fails, and how a standard is
  adopted incrementally. The test-catchable routes in §12a become gates there, not here.
- `python_concurrency_determinism_manifest.md` — the execution models, structured concurrency and
  cancellation. §8a states only what a `LogRecord` and a `ContextVar` carry across those boundaries.
- `python_module_boundaries_manifest.md` — the unit of change: package layout, the import system as a
  boundary, and the public-API contract that makes §4's library discipline meaningful.
- `python_typing_contract_manifest.md` — union/narrowing/protocol type-system facts; §12 states only what
  the checker cannot see about logging.
- `python_testing_tooling_manifest.md` — test framework facts and the double taxonomy; the canary-secret
  and drain-on-exit tests §12a routes as test-catchable are specified there.
- `python_language_hazards_manifest.md` — the hazard catalogue and the maximal-safety modern subset;
  logging-specific hazards stay in this file's §15.
- `architecture_manifest_default.md` — paradigms, the functional-core/imperative-shell rationale, and
  debuggability as an architectural property.
- `software_spec_discipline_manifest.md` — epistemic tagging, the reusability ledger, and the §G5
  discipline the open questions above are written against.
