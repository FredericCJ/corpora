# Deep-Research Prompt 04 — Dependencies & Supply-Chain Hygiene

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target, version anchor (mid-2026), epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**How do you manage JavaScript/TypeScript dependencies for safety and maintainability — the package
manager and lockfile discipline, the hygiene that keeps the graph small and current, and the
supply-chain defenses (script control, provenance, audit, SBOM) that treat every dependency as a
liability — as of mid-2026?**

## The mess this addresses

`node_modules` is the largest attack surface and the largest untracked liability in most JS/TS
projects. Dependencies bring transitive bloat, phantom dependencies, version drift, and a supply chain
where a single compromised or typosquatted package — executing an install script with full user
privileges — can exfiltrate secrets or backdoor a build (the xz-style lesson, arriving in npm form).
The narrow `../js/` program sidesteps this by design ("API calls / dependencies only where
unavoidable"); the general program must instead *manage* it deliberately. Every dependency is code you
are responsible for, a supply-chain node you must trust, and bytes you ship.

## Scope

- **In:** package managers + workspaces; lockfile discipline; version-range & update policy;
  dependency evaluation, minimization, and dead/duplicate detection; the supply-chain threat surface
  and its defenses (script control, provenance, audit, SBOM, integrity).
- **Out / defer:** *bundling/tree-shaking* of what's installed → prompt 03; *monorepo task
  orchestration / workspace protocols at scale* → prompt 07 (this prompt owns dependency *hygiene*; 07
  owns monorepo *structure & release*); the *runtime* constraints on native deps → prompt 02.
- **Do NOT duplicate** prompt 07's monorepo tooling; reference it.

## Research decomposition (find answers to these)

### A. Package managers & workspaces (survey + verdict, VERSION-DEPENDENT)
- **npm** vs **pnpm** vs **Yarn (Berry)**: install model and correctness — pnpm's
  **content-addressable store + strict, symlinked `node_modules`** that prevents **phantom
  (undeclared-transitive) dependencies**; npm/yarn's flat hoisting and its phantom-dependency hazard;
  Yarn PnP. **Workspaces** (`workspaces`/`pnpm-workspace.yaml`) and the `workspace:` protocol.
  **Corepack** for pinning the package manager itself. Recommend a default and name the tradeoff.

### B. Lockfile discipline
- **Always commit the lockfile**; **`npm ci` / `pnpm i --frozen-lockfile` / `yarn --immutable`** in CI
  (fail on drift, never mutate); lockfile as the reproducibility root (cross-ref 03 determinism);
  reviewing lockfile diffs; lockfile churn and conflict handling; integrity hashes.

### C. Version ranges & update policy
- Caret/tilde/exact/pinned ranges and what each risks; **`overrides`/`resolutions`** for forcing
  transitive versions (security patches, dedupe); **`engines`** and enforcing them; automated updates
  (**Renovate/Dependabot**) and the cadence tradeoff (stay-current-for-security vs churn/breakage);
  grouping and auto-merge policy.

### D. Dependency evaluation & minimization (the hygiene that keeps the graph small)
- **Before adding a dependency:** maintenance health, transitive weight, install size and
  tree-shakeability (bundlephobia/pkg-size/`npm ls`), **types quality** (bundled `.d.ts` vs
  `@types/*` vs none — ties to 01/02), license, native/postinstall footprint. The
  **build-vs-borrow** and "**is this a one-liner I'm importing a liability for?**" discipline.
- **Detecting waste:** unused dependencies and dead code (**knip**, depcheck); **duplicate** packages
  (`npm dedupe`/pnpm dedupe, `why`/`npm ls`); bundle-impact attribution (cross-ref 03).

### E. The supply-chain threat surface (mechanisms, then defenses — cite incidence, not FUD)
- **Threats:** typosquatting; **dependency confusion** (internal-name hijack via public registry);
  **malicious install scripts** (`preinstall`/`postinstall`/`prepare` running arbitrary code at
  install); compromised maintainer accounts / hijacked packages; protestware; the transitive-trust
  problem.
- **Defenses:**
  - **Script control** — `npm config set ignore-scripts true` / pnpm's **`onlyBuiltDependencies`**
    allowlist + `approve-builds`; running installs with scripts disabled by default.
  - **Provenance & integrity** — **npm provenance / SLSA attestations**, **Sigstore** signing,
    lockfile integrity hashes, `--strict-peer-dependencies`.
  - **Scanning** — `npm audit` and its limits; **OSV-Scanner**, **Socket**, Snyk; the false-positive/
    noise problem and how to gate without alert-fatigue.
  - **SBOM** — **CycloneDX/SPDX** generation for inventory and incident response.
  - **Isolation** — vendoring/allow-listing critical deps; private registry/proxy; scoped-registry
    config in `.npmrc` to prevent confusion.
- The **defense-in-depth posture** for a small team vs an enterprise (scale the recommendation).

## Controversies to resolve (positions first, then a recommendation)

- **pnpm vs npm vs Yarn** as the default in 2026.
- **`ignore-scripts` by default** — safety win vs the breakage tax of packages that need a build step.
- **Aggressive auto-update (Renovate)** vs deliberate, staged updates — which is *safer* net of both
  vulnerability exposure and breakage risk?
- **`npm audit`'s** signal-to-noise and whether to gate CI on it vs a better scanner.
- Minimal-dependency purism vs pragmatic reuse (reconcile with `../web_manifests/` reuse doctrine).

## Sources to prioritize

npm / **pnpm** / Yarn docs (install models, workspaces, script control); npm **provenance/SLSA** and
**Sigstore** docs; **OSV-Scanner**, **Socket**, Snyk docs; **CycloneDX/SPDX** SBOM specs; OWASP
(dependency/supply-chain, dependency confusion); **knip**/depcheck docs; empirical supply-chain
studies and post-incident write-ups (cite incidence + mechanism, master brief §10.6). Changelogs for
version-dependent facts.

## Output contract

Produce a ground-truth manifest (suggested filename `js_dependencies_supply_chain_manifest.md`): TL;DR
(the package-manager + lockfile + script-control + evaluate-before-adding thesis); the **package-manager
decision** table; the **lockfile & CI-install** discipline; the **version-range/update policy**; the
**dependency-evaluation checklist** (add-decision gate) and the **minimization/dead-dep** tooling; the
**supply-chain threat→defense** matrix; a **defense-in-depth posture** scaled small→enterprise; a
version matrix; an anti-pattern checklist (uncommitted/ignored lockfile, install-scripts-on-by-default,
unpinned package manager, phantom-dependency reliance, `npm audit`-as-only-defense, dependency-bloat);
sources; cross-references.

## Cross-references

Its lockfile is prompt 03's determinism root and prompt 07's CI-install foundation; its runtime
constraints come from prompt 02 (native deps, edge); dependency-*dead-code* overlaps prompt 06 (knip)
and *monorepo workspaces* hand off to prompt 07. References `../web_manifests/` reuse/minimal-dependency
doctrine and `../js/` (which deferred this domain).
