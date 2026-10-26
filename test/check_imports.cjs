// Mirror of Hermes Desktop contrib/runtime-loader.ts unsupportedImports(): the loader regex also matches
// inside comments/strings, so ANY `from "x"` / `import "x"` / `import("x")` text in plugin.js must be an allowed spec.
const src = require('fs').readFileSync(process.argv[2] || 'plugin.js', 'utf8');
const ok = new Set(['@hermes/plugin-sdk', 'react/jsx-dev-runtime', 'react/jsx-runtime', 'react']);
const re = /(from\s*|import\s*\(\s*|import\s+)(['"])([^'"]+)\2/g; const bad = [];
for (const m of src.matchAll(re)) { const s = m[3]; if (s && !/^[./]/.test(s) && !/^[a-z][a-z0-9+.-]*:/i.test(s) && !ok.has(s)) bad.push(s + '  @line ' + src.slice(0, m.index).split('\n').length); }
if (bad.length) { console.log('UNSUPPORTED IMPORTS (plugin will FAIL TO LOAD):\n' + bad.join('\n')); process.exit(1); } else console.log('imports OK');
