# Audit findings for `python_platform_baseline_manifest.md`

8 findings: MAJOR 2, MINOR 6

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MAJOR] around line 297

**Quoted text being challenged:**

> | `os.path.realpath(strict=os.path.ALLOW_MISSING)` (added for CVE-2025-4517) | **3.15** | — | — | — |

**What is actually true:**

`os.path.ALLOW_MISSING` is NOT a 3.15 addition. The 3.14 docs carry "Changed in version 3.14: The ALLOW_MISSING value for the strict parameter was added." and the constant's own entry reads "Added in version 3.14." The 3.13 docs are more precise still: "Changed in version 3.13.4: The ALLOW_MISSING value for the strict parameter was added" — i.e. it shipped as a security backport in 3.13.4 and is documented as 3.14 in the current stable docs. The hub's ledger claims 'Since' = 'the CPython version that shipped the construct', so 3.15 is wrong by one to two feature lines. The error is inherited verbatim from the pack (_work/facts/r01_platform_baseline.md:91 tags the whole line VERSION-DEPENDENT (3.15)), so it was never independently checked against os.path. An agent on a 3.13/3.14 floor would conclude a security-relevant API is unavailable and hand-roll a symlink resolver.

**Source the auditor checked:**

https://docs.python.org/3/library/os.path.html (3.14 stable) and https://docs.python.org/3.13/library/os.path.html — realpath() version notes. Accessed 8 Aug 2026.

**Prescribed fix:**

Replace the Since cell with **3.13.4 / 3.14** and the note with: `os.path.realpath(strict=os.path.ALLOW_MISSING)` (added 3.13.4 as part of the CVE-2025-4517 fix; documented "Changed in version 3.14" in the 3.14 docs). Move the row out of the 3.15 block of §4a into the 3.14 block, and correct _work/facts/r01_platform_baseline.md:91, which mis-files it under 3.15.

---

## 2. [MAJOR] around line 702

**Quoted text being challenged:**

> The 3.15 docs contain **no** "Pending removal in Python 3.15" section, and the 3.15 What's New

**What is actually true:**

docs.python.org/3.15/deprecations/index.html — the exact page the hub names as re-verification source #8 for §7d/§7e — does contain a "Pending removal in Python 3.15" section. It sits under **C API deprecations** and lists `PyImport_ImportModuleNoBlock()`, `PyWeakref_GetObject()` / `PyWeakref_GET_OBJECT()`, `PyUnicode_AsDecodedObject()`, `PyUnicode_AsDecodedUnicode()`, `PyUnicode_AsEncodedObject()`, `PyUnicode_AsEncodedUnicode()` and others. The claim is true only of the Python-level half of the page. The hub does not scope C API out — §4a carries a C API row (PyBytesWriter, PyGILState soft-deprecation) and §7d/§7e are presented as the removal calendar — so the unqualified negative reads as 'nothing is pending removal in 3.15'. A C-extension maintainer acting on it skips a live migration.

**Source the auditor checked:**

https://docs.python.org/3.15/deprecations/index.html — table of contents ("C API deprecations → Pending removal in Python 3.15") and the section body. Accessed 8 Aug 2026.

**Prescribed fix:**

Rewrite as: "The 3.15 docs contain no *Python-level* \"Pending removal in Python 3.15\" section — everything the 3.14 docs listed as pending for 3.15 has landed. The **C API** half of the page still has one (`PyImport_ImportModuleNoBlock()`, `PyWeakref_GetObject()`/`PyWeakref_GET_OBJECT()`, `PyUnicode_As{Decoded,Encoded}{Object,Unicode}()`), so a C extension can still be depending on a name scheduled to go."

---

## 3. [MINOR] around line 727

**Quoted text being challenged:**

> | **3.19** | Implicit MSVC struct layout from `_pack_` without `_layout_` on non-Windows; the `string` keyword argument of hashlib constructors; `http.cookies.Morsel.js_output()` / `BaseCookie.js_output()`; altering `imaplib.IMAP4.file` |

**What is actually true:**

§7d's table stops at 3.19, but the cited page has a further Python-level bucket, "Pending removal in Python 3.20", which the table omits entirely. Its contents are broad: `struct.Struct.__new__()` without the `format` argument and `__init__()` on an initialised Struct; the `__version__` / `version` / `VERSION` attributes of 25 stdlib modules (argparse, csv, ctypes, ctypes.macholib, decimal, http.server, imaplib, ipaddress, json, logging (`__date__` too), optparse, pickle, platform, re, socketserver, tabnanny, tarfile, tkinter.font, tkinter.ttk, wsgiref.simple_server, xml.etree.ElementTree, xml.sax.expatreader, xml.sax.handler, zlib); PEP 829 `.pth` warnings; instantiating abstract `ast` nodes; and `isinstance()`/`issubclass()` on protocols that inherit runtime-checkability without their own `@runtime_checkable`. The last item interacts directly with `python_typing_contract_manifest.md`'s Protocol content. Verified 3.16, 3.17, 3.18 and 3.19 rows all match the page exactly, so this is a truncation, not a mis-read.

**Source the auditor checked:**

https://docs.python.org/3.15/deprecations/index.html — "Pending removal in Python 3.20" section. Accessed 8 Aug 2026.

**Prescribed fix:**

Add a row after the 3.19 row: "| **3.20** | `struct.Struct.__new__()` without `format`, and `__init__()` on an initialised `Struct`; the `__version__` / `version` / `VERSION` attributes of 25 stdlib modules (`argparse`, `csv`, `ctypes`, `ctypes.macholib`, `decimal` (use `decimal.SPEC_VERSION`), `http.server`, `imaplib`, `ipaddress`, `json`, `logging` (`__date__` too), `optparse`, `pickle`, `platform`, `re`, `socketserver`, `tabnanny`, `tarfile`, `tkinter.font`, `tkinter.ttk`, `wsgiref.simple_server`, `xml.etree.ElementTree`, `xml.sax.expatreader`, `xml.sax.handler`, `zlib`) — use `sys.version_info`; warnings for `import` lines in `<name>.pth` files (PEP 829); instantiating abstract `ast` nodes; `isinstance()`/`issubclass()` on a protocol that inherits runtime-checkability without its own `@runtime_checkable` |"

---

## 4. [MINOR] around line 288

**Quoted text being challenged:**

> | Builtin `sentinel(name, /, repr=None)` | **3.15** | 661 | `typing_extensions.sentinel` (4.16.0) | `python_typing_contract_manifest.md` |

**What is actually true:**

`repr` is keyword-only. The 3.15 builtins reference gives the signature as `class sentinel(name, /, *, repr=None)` (the `*` is rendered as an explicit "Keyword-only parameter" marker in the signature). The hub's spelling omits the `*`, which says `sentinel("MISSING", "<MISSING>")` is legal; it raises `TypeError`. The sibling that owns the construct gets it right — python_typing_contract_manifest.md writes `class sentinel(name, /, *, repr=None)` — so the hub and its sibling disagree on the same signature, and the hub is the wrong one. Same error repeats in the source list at line 997.

**Source the auditor checked:**

https://docs.python.org/3.15/library/functions.html — `class sentinel(name, /, *, repr=None)`. Accessed 8 Aug 2026.

**Prescribed fix:**

Change both line 288 and line 997 to `sentinel(name, /, *, repr=None)`.

---

## 5. [MINOR] around line 29

**Quoted text being challenged:**

> lines; `3.14.0` is ten months and roughly 1,400 bugfixes behind current. VERSION-DEPENDENT (3.14).

**What is actually true:**

The ten-month figure is right (3.14.0 on 2025-10-07; today 2026-08-08). The bugfix count is not: summing the per-release counts on the python.org release pages, each stated 'since <previous release>', gives 558 (3.14.1) + 18 (3.14.2) + 299 (3.14.3) + 337 (3.14.4) + 154 (3.14.5) + 179 (3.14.6) + 499 (3.14.7) ≈ **2,044**, not ~1,400. The figure is a ~30% undercount and has no source: it appears unsourced in _work/facts/r01_platform_baseline.md:237, whose only sourced number is the 499 for 3.14.7 alone. It is asserted with a VERSION-DEPENDENT tag rather than flagged, in a file whose §8c promises every claim 'was read off a primary page … not recalled'.

**Source the auditor checked:**

https://www.python.org/downloads/release/python-3141/ … /python-3147/ — 'containing around N bugfixes … since 3.14.x' on each page. Accessed 8 Aug 2026.

**Prescribed fix:**

Replace with: "`3.14.0` is ten months and roughly 2,000 bugfixes behind current (the sum of the per-release counts on the 3.14.1–3.14.7 release pages)". Correct _work/facts/r01_platform_baseline.md:237 to match, or drop the aggregate and cite only the sourced 499-since-3.14.6.

---

## 6. [MINOR] around line 611

**Quoted text being challenged:**

> | — | `PYTHONDUMPREFS`, `PYTHONDUMPREFSFILE` | 3.11 | Requires a `--with-trace-refs` build (§5g) |

**What is actually true:**

Only `PYTHONDUMPREFSFILE` carries "Added in version 3.11". `PYTHONDUMPREFS` has no version-added note at all in the cmdline reference — it long predates 3.11. Pairing them in one row under an 'Added: 3.11' column makes the older variable look 3.11-gated, which matters because the §6a table is explicitly described as 'the inventory and the version gate'. Same conflation at line 547.

**Source the auditor checked:**

https://docs.python.org/3/using/cmdline.html — 'Debug-mode variables': PYTHONDUMPREFS (no version note) then PYTHONDUMPREFSFILE ("Added in version 3.11"). Accessed 8 Aug 2026.

**Prescribed fix:**

Split the row, or set the Added cell to `PYTHONDUMPREFSFILE`: 3.11 — e.g. "| — | `PYTHONDUMPREFS` (no version note; predates 3.11), `PYTHONDUMPREFSFILE` (3.11) | — | Requires a `--with-trace-refs` build (§5g) |". Adjust line 547 similarly.

---

## 7. [MINOR] around line 595

**Quoted text being challenged:**

> | `-X utf8=0\|1` | `PYTHONUTF8=0\|1` | added-version not re-verified this pass (**OPEN**) | UTF-8 mode.

**What is actually true:**

An honest OPEN is normally correct behaviour, but here the primary page the section header says the whole table was 'Confirmed against' states the answer outright: "-X utf8 enables the Python UTF-8 Mode. -X utf8=0 explicitly disables Python UTF-8 Mode … Added in version 3.7." §8c (lines 812–815) then justifies this OPEN with "they are OPEN because nothing authoritative was found this pass" — an assertion about the evidence that the cited page contradicts. The defect is the justification, not the caution: the gap is one line down from the rows that were read.

**Source the auditor checked:**

https://docs.python.org/3/using/cmdline.html — '-X utf8 … Added in version 3.7'. Accessed 8 Aug 2026.

**Prescribed fix:**

Set the Added cell to `3.7` and remove `-X utf8` from the OPEN list in §8c line 813, leaving §5f's JIT build mode, the pre-3.14 free-threaded wheel tags and the exceptiongroup/TOML backport versions (all genuinely absent from primary pages) as the file's OPENs.

---

## 8. [MINOR] around line 508

**Quoted text being challenged:**

> | 3.15 performance | "8-9% geometric mean performance improvement on x86-64 Linux" and "12-13% speedup on AArch64 macOS" | From the 3.15.0rc1 announcement. VERSION-DEPENDENT (3.15) |

**What is actually true:**

The two figures are quoted with their platforms but with their baselines stripped, and the baselines differ. The announcement reads: "The JIT compiler has been significantly upgraded, with 8-9% geometric mean performance improvement on x86-64 Linux **over the standard interpreter**, and 12-13% speedup on AArch64 macOS **over the tail-calling interpreter**." Presented side by side without that, the pair reads as one comparison against one baseline, and the 12–13% looks like a bigger JIT win than the 8–9% when it is measured against a faster reference. The file itself makes this exact error a rejection at line 793 ('Comparing profiles or benchmarks across build configurations') and devotes §5e to a benchmark number that was wrong precisely because of a mis-stated baseline.

**Source the auditor checked:**

https://www.python.org/downloads/release/python-3150rc1/ (and https://blog.python.org/2026/08/python-3150-rc1/) — 'Major new features of the 3.15 series' bullet. Accessed 8 Aug 2026.

**Prescribed fix:**

Restore the baselines: "8-9% geometric mean performance improvement on x86-64 Linux **over the standard interpreter**" and "12-13% speedup on AArch64 macOS **over the tail-calling interpreter**" — two different baselines, so the numbers are not comparable to each other. Apply the same fix at line 942 in the source list.

---
