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

  const EL_KINDS = new Set(['realizes', 'enables', 'constrains', 'implements', 'specializes', 'composes-with', 'alternative-to', 'uses']);
  const REALMS = new Set(['design', 'architecture']);
  /**
   * The element layer (design + architecture realms + the bridge). Inward boundary — a stale
   * data/elements.js must fail loud here. @param {unknown} raw @returns {any}
   */
  function parseElements(raw) {
    if (!isObj(raw)) throw new ValidationError('elements: not an object');
    const e = /** @type {any} */ (raw);
    const ids = new Set();
    for (const n of arr(e.nodes, 'elements.nodes')) {
      if (!isObj(n)) throw new ValidationError('element: not an object');
      str(n.id, 'element.id'); str(n.name, 'element.name'); str(n.kind, 'element.kind');
      if (!REALMS.has(n.realm)) throw new ValidationError(`element ${n.id}: bad realm ${n.realm}`);
      if (ids.has(n.id)) throw new ValidationError('elements: duplicate id ' + n.id);
      ids.add(n.id);
    }
    for (const ed of arr(e.edges, 'elements.edges')) {
      str(ed.from, 'element-edge.from'); str(ed.to, 'element-edge.to'); str(ed.kind, 'element-edge.kind');
      if (!EL_KINDS.has(ed.kind)) throw new ValidationError(`element-edge ${ed.from}->${ed.to}: unknown kind ${ed.kind}`);
      if (!ids.has(ed.from)) throw new ValidationError('element-edge source not an element: ' + ed.from);
      if (!ids.has(ed.to)) throw new ValidationError('element-edge target not an element: ' + ed.to);
    }
    arr(e.unbridged, 'elements.unbridged');
    if (!isObj(e.works)) throw new ValidationError('elements.works missing');
    if (!isObj(e.meta)) throw new ValidationError('elements.meta missing');
    return e;
  }

  /**
   * The atlas layer (islands + precomputed geography). Inward boundary — a stale data/atlas.js must
   * fail loud here. @param {unknown} raw @returns {any} */
  function parseAtlas(raw) {
    if (!isObj(raw)) throw new ValidationError('atlas: not an object');
    const a = /** @type {any} */ (raw);
    if (!isObj(a.meta) || !Array.isArray(a.meta.families)) throw new ValidationError('atlas.meta.families missing');
    const seen = new Set();
    for (const isl of arr(a.islands, 'atlas.islands')) {
      if (!isObj(isl)) throw new ValidationError('island: not an object');
      str(isl.id, 'island.id'); str(isl.name, 'island.name'); str(isl.family, 'island.family');
      if (typeof isl.cx !== 'number' || typeof isl.cy !== 'number' || typeof isl.r !== 'number')
        throw new ValidationError(`island ${isl.id}: bad geometry`);
      for (const m of arr(isl.members, `island ${isl.id}.members`)) {
        str(m.id, 'island member.id');
        if (typeof m.x !== 'number' || typeof m.y !== 'number') throw new ValidationError(`member ${m.id}: bad coords`);
      }
      if (seen.has(isl.id)) throw new ValidationError('atlas: duplicate island ' + isl.id);
      seen.add(isl.id);
    }
    arr(a.routes, 'atlas.routes');
    if (!isObj(a.bridgeFlow)) throw new ValidationError('atlas.bridgeFlow missing');
    return a;
  }

  return { ValidationError, parseCorpus, parseRelations, parseElements, parseAtlas };
})();
