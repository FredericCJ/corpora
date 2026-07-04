// parse.js — boundary parsing (js_typing_contract_manifest §5: parse, don't validate).
// The data modules are an inward boundary (generated, but treated as untrusted per the
// manifest — a stale/old-shape file must fail loud, not flow inward as `any`). Each parse
// function turns `unknown` into a typed value or throws a typed ValidationError once, at the edge.
window.DS = window.DS || {};
DS.parse = (function () {
  'use strict';
  const U = DS.util;

  class ValidationError extends Error {
    constructor(msg, cause) { super(msg, cause ? { cause } : undefined); this.name = 'ValidationError'; }
  }

  /**
   * @typedef {object} DSNode
   * @property {string} id @property {string} name @property {string} family
   * @property {'root'|'backfill'|'modern'} tier @property {number|null} year
   * @property {string} origin @property {'verified'|'flagged'} verification
   * @property {string} verdict @property {string[]} reports @property {string[]} flags @property {string} note
   *
   * @typedef {object} DSEdge
   * @property {string} s @property {string} t @property {string} kind @property {string} src
   * @property {string} cycle @property {string} note
   *
   * @typedef {object} Corpus
   * @property {Record<string,string>} families @property {string[]} familyOrder
   * @property {Record<string,string>} sources @property {DSNode[]} nodes
   *
   * @typedef {object} Relations
   * @property {string[]} kinds @property {DSEdge[]} edges
   * @property {Record<string,string>} cycles @property {object} model
   */

  const isObj = (v) => v !== null && typeof v === 'object';
  const str = (v, where) => { if (typeof v !== 'string') throw new ValidationError(`${where}: expected string, got ${typeof v}`); return v; };
  const arr = (v, where) => { if (!Array.isArray(v)) throw new ValidationError(`${where}: expected array`); return v; };

  /** @param {unknown} raw @returns {Corpus} */
  function parseCorpus(raw) {
    if (!isObj(raw)) throw new ValidationError('corpus: not an object');
    const c = /** @type {any} */ (raw);
    if (!isObj(c.families)) throw new ValidationError('corpus.families missing');
    arr(c.familyOrder, 'corpus.familyOrder');
    const nodes = arr(c.nodes, 'corpus.nodes').map(parseNode);
    const seen = new Set();
    for (const n of nodes) {
      if (seen.has(n.id)) throw new ValidationError('corpus: duplicate node id ' + n.id);
      seen.add(n.id);
      if (!(n.family in c.families)) throw new ValidationError(`corpus: node ${n.id} unknown family ${n.family}`);
    }
    return /** @type {Corpus} */ (c);
  }

  /** @param {unknown} raw @returns {DSNode} */
  function parseNode(raw) {
    if (!isObj(raw)) throw new ValidationError('node: not an object');
    const n = /** @type {any} */ (raw);
    str(n.id, 'node.id'); str(n.name, 'node.name'); str(n.family, 'node.family');
    if (n.tier !== 'root' && n.tier !== 'backfill' && n.tier !== 'modern')
      throw new ValidationError(`node ${n.id}: bad tier ${n.tier}`);
    if (n.year !== null && typeof n.year !== 'number')
      throw new ValidationError(`node ${n.id}: year must be number|null`);
    if (n.verification !== 'verified' && n.verification !== 'flagged')
      throw new ValidationError(`node ${n.id}: bad verification ${n.verification}`);
    arr(n.reports, `node ${n.id}.reports`); arr(n.flags, `node ${n.id}.flags`);
    return /** @type {DSNode} */ (n);
  }

  /** @param {unknown} raw @param {Set<string>} nodeIds @returns {Relations} */
  function parseRelations(raw, nodeIds) {
    if (!isObj(raw)) throw new ValidationError('relations: not an object');
    const r = /** @type {any} */ (raw);
    const kinds = new Set(arr(r.kinds, 'relations.kinds'));
    const cycles = isObj(r.cycles) ? r.cycles : {};
    for (const e of arr(r.edges, 'relations.edges')) {
      if (!isObj(e)) throw new ValidationError('edge: not an object');
      str(e.s, 'edge.s'); str(e.t, 'edge.t'); str(e.kind, 'edge.kind');
      if (!nodeIds.has(e.s)) throw new ValidationError(`edge source not a node: ${e.s}`);
      if (!nodeIds.has(e.t)) throw new ValidationError(`edge target not a node: ${e.t}`);
      if (!kinds.has(e.kind)) throw new ValidationError(`edge ${e.s}->${e.t}: unknown kind ${e.kind}`);
      if (e.cycle && !(e.cycle in cycles)) throw new ValidationError(`edge ${e.s}->${e.t}: unknown cycle ${e.cycle}`);
    }
    return /** @type {Relations} */ (r);
  }

  return { ValidationError, parseCorpus, parseRelations };
})();
