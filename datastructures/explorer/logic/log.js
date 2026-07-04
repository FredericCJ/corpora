// log.js — the injected-logger seam (browser_observability_manifest §4).
// The browser has no logging architecture; components emit through an injected logger and
// configure nothing. The default is a frozen NO-OP (the NullHandler analogue): a component
// with no logger injected is silent, not chatty. The application builds ONE console router at
// bootstrap. No component calls console.* directly; no logging side effects at import.
window.DS = window.DS || {};
DS.log = (function () {
  'use strict';

  /**
   * @typedef {object} Logger
   * @property {(msg:string,data?:unknown)=>void} debug
   * @property {(msg:string,data?:unknown)=>void} info
   * @property {(msg:string,data?:unknown)=>void} warn
   * @property {(msg:string,data?:unknown)=>void} error
   */

  /** @type {Logger} */
  const NOOP = Object.freeze({ debug() {}, info() {}, warn() {}, error() {} });

  const LEVELS = { debug: 10, info: 20, warn: 30, error: 40 };

  /**
   * The application-side console router (the dictConfig analogue), built once at bootstrap.
   * @param {string} name  child-logger name (recovers getLogger(__name__) as a `logger` field)
   * @param {keyof typeof LEVELS} [threshold]
   * @returns {Logger}
   */
  function consoleLogger(name, threshold) {
    const min = LEVELS[threshold || 'info'];
    /** @param {keyof typeof LEVELS} level @param {'debug'|'info'|'warn'|'error'} method */
    const at = (level, method) => (msg, data) => {
      if (LEVELS[level] < min) return;           // gate BEFORE building the payload (§2)
      const entry = { level, logger: name, msg };
      if (data !== undefined) entry.data = data; // caller passes snapshots, not live refs
      // eslint-disable-next-line no-console -- the one designated app sink
      console[method](`[${name}] ${msg}`, data !== undefined ? data : '');
      return entry;
    };
    return Object.freeze({
      debug: at('debug', 'debug'), info: at('info', 'info'),
      warn: at('warn', 'warn'), error: at('error', 'error'),
    });
  }

  return { NOOP, consoleLogger };
})();
