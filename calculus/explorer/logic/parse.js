// parse.js — boundary parsing (js_typing_contract_manifest §5: parse, don't validate). The data
// modules are an inward boundary; a stale/old-shape file must fail loud here, not flow inward.
window.CALC = window.CALC || {};
CALC.parse = (function () {
  'use strict';
  class ValidationError extends Error {
    constructor(m, cause) { super(m, cause ? { cause } : undefined); this.name = 'ValidationError'; }
  }
  /**
   * @typedef {object} Node
   * @property {string} id @property {string} title @property {string} authors @property {string} edition
   * @property {string} year @property {string} publisher @property {number} tier @property {string} rigor
   * @property {string} role @property {string[]} flags @property {'kept'|'dropped'} status
   * @property {'verified'} verification @property {string|null} isbn @property {string|null} access
   * @property {string} note @property {string} bib
   *
   * @typedef {object} Tier @property {number} tier @property {string} name @property {string} focus @property {string} rigor
   * @typedef {object} Edge @property {string} s @property {string} t @property {string} seam
   * @property {'EVIDENCED'|'JUDGMENT'} tag @property {string} note
   *
   * @typedef {object} Corpus
   * @property {{title:string,source:string,access_date:string,compiled:string}} meta
   * @property {string[]} tldr @property {Tier[]} tiers @property {Node[]} nodes
   * @typedef {object} Relations
   * @property {Edge[]} edges @property {any[]} parallelSets @property {any[]} lineages
   * @property {any[]} gate @property {any[]} register @property {any[]} caveats @property {Record<string,any>} views
   */
  const isObj = (v) => v !== null && typeof v === 'object';
  const str = (v, w) => { if (typeof v !== 'string') throw new ValidationError(`${w}: expected string`); return v; };
  const arr = (v, w) => { if (!Array.isArray(v)) throw new ValidationError(`${w}: expected array`); return v; };

  /** @param {unknown} raw @returns {Corpus} */
  function parseCorpus(raw) {
    if (!isObj(raw)) throw new ValidationError('corpus: not an object');
    const c = /** @type {any} */ (raw);
    if (!isObj(c.meta)) throw new ValidationError('corpus.meta missing');
    const tiers = new Set();
    for (const t of arr(c.tiers, 'corpus.tiers')) {
      if (!isObj(t) || typeof t.tier !== 'number') throw new ValidationError('tier: bad shape');
      str(t.name, 'tier.name'); tiers.add(t.tier);
    }
    const seen = new Set();
    for (const n of arr(c.nodes, 'corpus.nodes')) {
      if (!isObj(n)) throw new ValidationError('node: not an object');
      str(n.id, 'node.id'); str(n.title, 'node.title'); str(n.bib, `node ${n.id}.bib`);
      if (n.status !== 'kept' && n.status !== 'dropped')
        throw new ValidationError(`node ${n.id}: bad status ${n.status}`);
      if (!tiers.has(n.tier)) throw new ValidationError(`node ${n.id}: unknown tier ${n.tier}`);
      arr(n.flags, `node ${n.id}.flags`);
      if (seen.has(n.id)) throw new ValidationError('corpus: duplicate id ' + n.id);
      seen.add(n.id);
    }
    return /** @type {Corpus} */ (c);
  }

  /** @param {unknown} raw @param {Map<string,any>} byId @returns {Relations} */
  function parseRelations(raw, byId) {
    if (!isObj(raw)) throw new ValidationError('relations: not an object');
    const r = /** @type {any} */ (raw);
    for (const e of arr(r.edges, 'relations.edges')) {
      if (!isObj(e)) throw new ValidationError('edge: not an object');
      str(e.s, 'edge.s'); str(e.t, 'edge.t'); str(e.seam, 'edge.seam');
      if (!byId.has(e.s)) throw new ValidationError(`edge source not a node: ${e.s}`);
      if (!byId.has(e.t)) throw new ValidationError(`edge target not a node: ${e.t}`);
      if (e.tag !== 'EVIDENCED' && e.tag !== 'JUDGMENT')
        throw new ValidationError(`edge ${e.s}->${e.t}: bad tag ${e.tag}`);
      if (byId.get(e.s).status !== 'kept' || byId.get(e.t).status !== 'kept')
        throw new ValidationError(`edge ${e.s}->${e.t}: touches a dropped node`);
    }
    for (const ps of arr(r.parallelSets, 'relations.parallelSets'))
      for (const m of arr(ps.members, `${ps.id}.members`))
        if (!byId.has(m)) throw new ValidationError(`${ps.id}: unknown member ${m}`);
    for (const ln of arr(r.lineages, 'relations.lineages'))
      for (const p of arr(ln.path, `lineage ${ln.id}.path`))
        if (!byId.has(p)) throw new ValidationError(`lineage ${ln.id}: unknown node ${p}`);
    if (!isObj(r.views)) throw new ValidationError('relations.views missing');
    return /** @type {Relations} */ (r);
  }
  return { ValidationError, parseCorpus, parseRelations };
})();
