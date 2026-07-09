// parse.js — boundary parsing (js_typing_contract_manifest §5: parse, don't validate). The data
// modules are an inward boundary; a stale/old-shape file must fail loud here, not flow inward.
window.NET = window.NET || {};
NET.parse = (function () {
  'use strict';
  class ValidationError extends Error {
    constructor(m, cause) { super(m, cause ? { cause } : undefined); this.name = 'ValidationError'; }
  }
  /**
   * @typedef {object} Node
   * @property {string} id @property {string[]} corpus @property {Record<string,string>} item
   * @property {number} section @property {string} title @property {string} cite @property {string} note
   * @property {string[]} subfield @property {string[]} paradigm @property {string[]} type
   * @property {string|null} stratum @property {string} recency @property {string} recencyRaw
   * @property {'verified-web'|'verified-train'|'unverified'} verification @property {string} verRaw
   * @property {number|null} year @property {boolean} living @property {boolean} quarantined
   * @property {string[]} idents @property {object} [matTwin]
   *
   * @typedef {object} Corpus
   * @property {any} meta @property {Record<string,any>} corpora @property {any[]} anchorParts
   * @property {Record<string,any[]>} sections @property {Node[]} nodes
   * @typedef {object} Relations
   * @property {string[]} kinds @property {any[]} edges @property {any[]} anchorMap
   * @property {Record<string,string[]>} coverage @property {Record<string,string>} verificationLegend
   * @property {Record<string,any>} views
   */
  const isObj = (v) => v !== null && typeof v === 'object';
  const str = (v, w) => { if (typeof v !== 'string') throw new ValidationError(`${w}: expected string`); return v; };
  const arr = (v, w) => { if (!Array.isArray(v)) throw new ValidationError(`${w}: expected array`); return v; };
  const VERS = new Set(['verified-web', 'verified-train', 'unverified']);

  /** @param {unknown} raw @returns {Corpus} */
  function parseCorpus(raw) {
    if (!isObj(raw)) throw new ValidationError('corpus: not an object');
    const c = /** @type {any} */ (raw);
    if (!isObj(c.corpora) || !isObj(c.sections)) throw new ValidationError('corpus.corpora/sections missing');
    arr(c.anchorParts, 'corpus.anchorParts');
    const seen = new Set();
    for (const n of arr(c.nodes, 'corpus.nodes')) {
      if (!isObj(n)) throw new ValidationError('node: not an object');
      str(n.id, 'node.id'); str(n.title, 'node.title'); str(n.cite, `node ${n.id}.cite`);
      arr(n.corpus, `node ${n.id}.corpus`); arr(n.subfield, `node ${n.id}.subfield`);
      arr(n.paradigm, `node ${n.id}.paradigm`);
      if (!VERS.has(n.verification)) throw new ValidationError(`node ${n.id}: bad verification ${n.verification}`);
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
      str(e.s, 'edge.s'); str(e.t, 'edge.t');
      if (!ids.has(e.s)) throw new ValidationError(`edge source not a node: ${e.s}`);
      if (!ids.has(e.t)) throw new ValidationError(`edge target not a node: ${e.t}`);
      if (!kinds.has(e.kind)) throw new ValidationError(`edge ${e.s}->${e.t}: unknown kind ${e.kind}`);
    }
    arr(r.anchorMap, 'relations.anchorMap');
    if (!isObj(r.coverage) || !isObj(r.views) || !isObj(r.verificationLegend))
      throw new ValidationError('relations.coverage/views/verificationLegend missing');
    str(r.overlayProvenance, 'relations.overlayProvenance');
    for (const ov of arr(r.overlays, 'relations.overlays')) {
      str(ov.id, 'overlay.id'); arr(ov.levels, `overlay ${ov.id}.levels`);
      if (!isObj(ov.members)) throw new ValidationError(`overlay ${ov.id}: members missing`);
      for (const m in ov.members) if (!ids.has(m)) throw new ValidationError(`overlay ${ov.id}: member ${m} not a node`);
      for (const e of arr(ov.edges, `overlay ${ov.id}.edges`)) {
        if (!(e.s in ov.members) || !(e.t in ov.members))
          throw new ValidationError(`overlay ${ov.id}: edge ${e.s}->${e.t} endpoint not a member`);
        str(e.why, `overlay ${ov.id} edge ${e.s}->${e.t}.why`);
      }
    }
    return /** @type {Relations} */ (r);
  }
  return { ValidationError, parseCorpus, parseRelations };
})();
