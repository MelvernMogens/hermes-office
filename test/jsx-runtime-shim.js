/* jsx-runtime shim → real React (UMD). Exports exactly what plugin.js imports. */
const R = window.React;
/* v5.4 fix: honor the 3rd `key` arg like the real react/jsx-runtime (dropping it made React
   reconcile agents by index -> a capsule node got reused for another agent = fake desync). */
export const jsx = (type, props, key) => {
  const p = key === undefined ? props : Object.assign({}, props, { key });
  return R.createElement(type, p, props && props.children);
};
export const jsxs = jsx;
export const Fragment = R.Fragment;
