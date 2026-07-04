// parse.js — boundary parsing (js_typing_contract_manifest §5: parse, don't validate). The data
// modules are an inward boundary; a stale/old-shape file must fail loud here, not flow inward.
window.SWE = window.SWE || {};
SWE.parse = (function () {
  'use strict';
  class ValidationError extends Error {
    constructor(m, cause) { super(m, cause ? { cause } : undefined); this.name = 'ValidationError'; }
  }
  /**
   * @typedef {object} Node
   * @property {string} id @property {string} title @property {string} authors @property {string} year
   * @property {'verified'|'unverified'} verification @property {string[]} corpora
   * @property {Record<string,any>} per @property {string} [ident] @property {string[]} [unresolved]
   * @property {string} [type] @property {string[]} [branches] @property {string[]} [themes]
   * @property {string[]} [role] @property {string|null} [lane] @property {string|null} [scope]
   * @property {string|null} [access] @property {boolean} [automotive] @property {string} [note]
   *
   * @typedef {object} Edge
   * @property {string} s @property {string} t @property {string} kind @property {string} src
   * @property {string} [note] @property {string} [cycle]
   *
   * @typedef {object} Corpus @property {Record<string,string>} corpora @property {Node[]} nodes
   * @typedef {object} Relations @property {string[]} kinds @property {Edge[]} edges @property {Record<string,any>} views
   */
  const isObj = (v) => v !== null && typeof v === 'object';
  const str = (v, w) => { if (typeof v !== 'string') throw new ValidationError(`${w}: expected string`); return v; };
  const arr = (v, w) => { if (!Array.isArray(v)) throw new ValidationError(`${w}: expected array`); return v; };

  /** @param {unknown} raw @returns {Corpus} */
  function parseCorpus(raw) {
    if (!isObj(raw)) throw new ValidationError('corpus: not an object');
    const c = /** @type {any} */ (raw);
    if (!isObj(c.corpora)) throw new ValidationError('corpus.corpora missing');
    const seen = new Set();
    for (const n of arr(c.nodes, 'corpus.nodes')) {
      if (!isObj(n)) throw new ValidationError('node: not an object');
      str(n.id, 'node.id'); str(n.title, 'node.title');
      if (n.verification !== 'verified' && n.verification !== 'unverified')
        throw new ValidationError(`node ${n.id}: bad verification ${n.verification}`);
      arr(n.corpora, `node ${n.id}.corpora`);
      if (seen.has(n.id)) throw new ValidationError('corpus: duplicate id ' + n.id);
      seen.add(n.id);
    }
    return /** @type {Corpus} */ (c);
  }

  /** @param {unknown} raw @param {Set<string>} ids @returns {Relations} */
  function parseRelations(raw, ids) {
    if (!isObj(raw)) throw new ValidationError('relations: not an object');
    const r = /** @type {any} */ (raw);
    const kinds = new Set(arr(r.kinds, 'relations.kinds'));
    for (const e of arr(r.edges, 'relations.edges')) {
      if (!isObj(e)) throw new ValidationError('edge: not an object');
      str(e.s, 'edge.s'); str(e.t, 'edge.t'); str(e.kind, 'edge.kind');
      if (!ids.has(e.s)) throw new ValidationError(`edge source not a node: ${e.s}`);
      if (!ids.has(e.t)) throw new ValidationError(`edge target not a node: ${e.t}`);
      if (!kinds.has(e.kind)) throw new ValidationError(`edge ${e.s}->${e.t}: unknown kind ${e.kind}`);
    }
    return /** @type {Relations} */ (r);
  }
  return { ValidationError, parseCorpus, parseRelations };
})();
