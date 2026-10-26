/* Thin @hermes/plugin-sdk mock for the harness.
   Real React (UMD) is loaded globally; host + atoms come from Part 1 of harness.html. */
const R = window.React;
const { useState, useEffect, useCallback } = R;

/* ---------------- query mini-cache ---------------- */
const CACHE = new Map(); // keyStr -> { data, error, status, promise, fn }
const SUBS = new Map(); // keyStr -> Set<forceUpdate>

const keyStr = (k) => JSON.stringify(k);

function notify(ks) {
  /* deferred: never re-render synchronously from inside an effect */
  queueMicrotask(() => {
    const set = SUBS.get(ks);
    if (set) for (const fn of Array.from(set)) { try { fn(); } catch (e) {} }
  });
}

async function runQuery(ks, fn) {
  let ent = CACHE.get(ks);
  if (!ent) {
    ent = { data: undefined, error: undefined, status: 'idle', promise: undefined, fn };
    CACHE.set(ks, ent);
  }
  if (ent.status === 'loading' && ent.promise) return ent.promise;
  ent.fn = fn;
  ent.status = 'loading';
  ent.error = undefined;
  notify(ks);
  ent.promise = (async () => {
    try {
      const data = await fn();
      const e = CACHE.get(ks);
      if (!e) return;
      e.data = data;
      e.status = 'success';
      e.promise = undefined;
      notify(ks);
      return data;
    } catch (err) {
      const e = CACHE.get(ks);
      if (!e) return;
      e.error = err;
      e.status = 'error';
      e.promise = undefined;
      notify(ks);
    }
  })();
  return ent.promise;
}

export function useQuery(opts) {
  const ks = keyStr(opts.queryKey);
  const [, force] = useState(0);

  /* register the latest queryFn for this key (refetch/invalidation use it) */
  let ent = CACHE.get(ks);
  if (!ent) {
    ent = { data: undefined, error: undefined, status: 'idle', promise: undefined, fn: opts.queryFn };
    CACHE.set(ks, ent);
  }
  ent.fn = opts.queryFn;

  /* subscribe */
  useEffect(() => {
    const set = SUBS.get(ks) || new Set();
    set.add(force);
    SUBS.set(ks, set);
    return () => { set.delete(force); };
  }, [ks]);

  /* fetch on mount — idle keys start; already-settled keys refetch like
     tanstack's default refetchOnMount (staleTime 0), so a mode switch on
     remount surfaces fresh results instead of showing stale data */
  useEffect(() => {
    const e = CACHE.get(ks);
    if (e && e.status !== 'loading') runQuery(ks, e.fn).catch(() => {});
  }, [ks]);

  /* interval refetch */
  const ms = opts.refetchInterval;
  useEffect(() => {
    if (!ms) return;
    const id = setInterval(() => {
      const e = CACHE.get(ks);
      if (e && e.status !== 'loading') runQuery(ks, e.fn).catch(() => {});
    }, ms);
    return () => clearInterval(id);
  }, [ks, ms]);

  const cur = CACHE.get(ks) || ent;
  const pending = cur.status === 'idle' || cur.status === 'loading';
  return {
    data: cur.status === 'error' ? undefined : cur.data,
    error: cur.error,
    isLoading: pending && cur.data === undefined,
    isFetching: cur.status === 'loading',
    isError: cur.status === 'error',
    refetch: () => runQuery(ks, cur.fn).catch(() => {}),
  };
}

export function useQueryClient() {
  return {
    invalidateQueries: (filt) => {
      const prefix = filt && filt.queryKey ? keyStr(filt.queryKey) : null;
      const targets = [];
      for (const [ks, ent] of CACHE.entries()) {
        if (prefix == null || ks === prefix || ks.startsWith(prefix.slice(0, -1) + ',')) targets.push([ks, ent]);
      }
      for (const [ks, ent] of targets) {
        if (ent.status !== 'loading') runQuery(ks, ent.fn).catch(() => {});
      }
      return Promise.resolve();
    },
  };
}

/* ---------------- host / atoms / i18n ---------------- */
/* v5.7b: 'session.activity' handler (core RPC, read-only). Served here so every harness host gets it.
   Fixtures: window.__OFFICE_ACTIVITY__ = { <profile>: rows | () => rows }.
   Knobs: __OFFICE_ACTIVITY_THROW__ (sync throw, like an old backend's "unknown method"), __OFFICE_ACTIVITY_DELAY__ (ms).
   Log: __OFFICE_ACTV_LOG__ = [{ profile, t }], __OFFICE_ACTV_INFLIGHT__ {profile: n}, __OFFICE_ACTV_MAXPAR__ {profile: max}. */
(function installActivity(h) {
  if (!h || h.__actv) return;
  const orig = h.request.bind(h);
  h.__actv = true;
  h.request = function (method, params) {
    if (method !== 'session.activity') return orig(method, params);
    const c = window.__OFFICE_RPC__ && window.__OFFICE_RPC__.counts;
    if (c) c[method] = (c[method] || 0) + 1;
    const prof = String((params && params.profile) || 'default');
    (window.__OFFICE_ACTV_LOG__ = window.__OFFICE_ACTV_LOG__ || []).push({ profile: prof, t: Date.now() });
    if (window.__OFFICE_ACTIVITY_THROW__) throw new Error('unknown method: session.activity');
    if (window.__OFFICE_RPC__ && window.__OFFICE_RPC__.mode === 'error') return Promise.reject(new Error('gateway down (mock)'));
    const inf = (window.__OFFICE_ACTV_INFLIGHT__ = window.__OFFICE_ACTV_INFLIGHT__ || {});
    const mx = (window.__OFFICE_ACTV_MAXPAR__ = window.__OFFICE_ACTV_MAXPAR__ || {});
    inf[prof] = (inf[prof] || 0) + 1; mx[prof] = Math.max(mx[prof] || 0, inf[prof]);
    const src = (window.__OFFICE_ACTIVITY__ || {})[prof];
    const rows = typeof src === 'function' ? src() : (src || []);
    const delay = +window.__OFFICE_ACTIVITY_DELAY__ || 0;
    return new Promise((ok) => setTimeout(() => { inf[prof] -= 1; ok({ activity: rows.slice(0, (params && params.limit) || 20) }); }, delay));
  };
})(window.__OFFICE_HOST__);
export const host = window.__OFFICE_HOST__;

export function useValue(atom) {
  const [v, setV] = useState(() => (atom && atom.get ? atom.get() : undefined));
  useEffect(() => {
    if (!atom || !atom.subscribe) return undefined;
    return atom.subscribe(setV);
  }, [atom]);
  return v;
}

export function usePluginI18n(pid) {
  /* locale is harness-controlled; re-resolve when harness bumps watchers */
  const [, force] = useState(0);
  useEffect(() => {
    const bump = () => force((v) => v + 1);
    const watchers = (window.__OFFICE_I18N_WATCH__ = window.__OFFICE_I18N_WATCH__ || new Set());
    watchers.add(bump);
    return () => watchers.delete(bump);
  }, []);
  return (key, ...args) => {
    const bundles = window.__OFFICE_I18N__ && window.__OFFICE_I18N__[pid];
    const loc = window.__OFFICE_LOCALE__ || 'en';
    const b = bundles && (bundles[loc] || bundles.en);
    let s = b && b[key] != null ? b[key] : key;
    if (args && args.length) {
      s = String(s).replace(/\{(\d+)\}/g, (m, i) => (args[i] != null ? String(args[i]) : m));
    }
    return s;
  };
}

/* ---------------- small UI components ---------------- */
export function StatusDot({ color }) {
  return R.createElement('span', { className: 'office-dot', style: { background: String(color) } });
}
export function EmptyState({ title, description }) {
  return R.createElement(
    'div',
    { className: 'office-empty', 'data-state': 'empty', style: { textAlign: 'center', padding: '18px 10px' } },
    R.createElement('div', { style: { fontSize: '24px', marginBottom: 6 } }, '🏢'),
    R.createElement('div', { style: { fontWeight: 600, fontSize: '12.5px' } }, title),
    R.createElement('div', { style: { fontSize: '11px', opacity: 0.8, marginTop: 3 } }, description)
  );
}
export function GlyphSpinner() {
  return R.createElement('span', { className: 'office-glyph-spinner' }, '◌');
}
export function cn(...xs) { return xs.filter(Boolean).join(' '); }
export function haptic() {}
