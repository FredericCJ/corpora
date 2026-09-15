# Audit findings for `python_typing_contract_manifest.md`

1 findings: MINOR 1

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MINOR] around line 3

**Quoted text being challenged:**

> Every factual claim is tagged **ESTABLISHED** (normative and stable in the cited primary source), **VERSION-DEPENDENT** (bound to an exact Python/checker/library version), **OPEN** (no authoritative source — a convention the project must pin), or **CC-FACT** (Claude-Code mechanics; none arise here). **FLAGGED-SECONDARY** marks a claim whose only evidence was secondary or vendor-published. An untagged factual claim in this file is a defect.

**What is actually true:**

Two markers used in the ground-truth files are absent from the legends of the files that use them. (a) `UNVERIFIED` is used 19 times outside error_tracing — twice in python_typing_contract (L508, L509), ten times in python_runtime_diagnostics (L1025–L1453), seven times in python_concurrency_determinism (L103–L1629) — but appears in none of those three legends; only error_tracing_contract_manifest.md L3 declares it ('the citation is marked **UNVERIFIED**'). Each of the three does explain it locally where first used (typing L497, runtime-diagnostics L1434, concurrency L1564), so the meaning is recoverable, but a reader who takes the legend as the closed tag set meets an undeclared sixth marker. (b) python_typing_contract_manifest.md additionally uses a `(decision)` / `(principle)` parenthetical 12 times (L100, L184, L205, L212, L230, L251, L280, L285, L289, L298, L329, L333) in the position a tag would occupy, with no legend entry — where python_runtime_diagnostics_manifest.md L17-18 handles the same problem explicitly ('Statements about which sibling file owns a topic, and pointers between sections, are collection conventions rather than factual claims and carry no tag'). Note python_linting_practices_manifest.md does this correctly, declaring its sixth marker `MEASURED` in the legend at L22-25.

**Source the auditor checked:**

grep -c '\*\*UNVERIFIED\*\*' across the 11 ground-truth files; legend text at python_typing_contract_manifest.md L3, python_runtime_diagnostics_manifest.md L13-18, python_concurrency_determinism_manifest.md L14-18; contrast python_linting_practices_manifest.md L22-25 and error_tracing_contract_manifest.md L3

**Prescribed fix:**

Add to the legend of python_typing_contract_manifest.md L3, python_runtime_diagnostics_manifest.md L13-18 and python_concurrency_determinism_manifest.md L14-18 the sentence already present in error_tracing's legend, e.g.: '**UNVERIFIED** marks an imported vocabulary citation whose bibliographic record the SWE corpus itself records as unverified; it must not be presented as verified ground truth.' And in python_typing_contract_manifest.md L3, after 'An untagged factual claim in this file is a defect.', add the carve-out runtime-diagnostics already uses: 'Blocks marked **(decision)** or **(principle)** are this file's synthesis rather than factual claims, and carry no tag; where such a block rests on a fact, the fact is tagged at its point of establishment above.'

---
