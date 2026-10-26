/* 'react' ESM wrapper over the UMD global — same instance ReactDOM uses. */
const R = window.React;
export const useState = R.useState;
export const useEffect = R.useEffect;
export const useMemo = R.useMemo;
export const useCallback = R.useCallback;
export const useRef = R.useRef;
export const Fragment = R.Fragment;
export default R;
