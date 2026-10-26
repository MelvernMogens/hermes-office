# hermes-office: agent notes

**What this is.** This is the public release of the Office pane plugin for Hermes Desktop: a pixel-art building with one floor per profile, driven by real gateway data. Melvern's live install is a separate working copy at `~/.hermes/desktop-plugins/hermes-office/`, which holds the private briefs, handoff notes, logs and shots. Port changes into this repo deliberately. The working copy stays private and must never be pushed.

**Stack.**
- One ESM file, `plugin.js`, using React through `@hermes/plugin-sdk` with all art embedded as data URIs. The desktop loader takes a single file, so there is no bundler.
- An optional core patch in `core-patch/` for the two read-only RPCs.
- **Rejected:** a build step or multiple files. The runtime loader only allows the SDK/React specifiers.

## Commands

- Syntax: `cp plugin.js /tmp/p.mjs && node --check /tmp/p.mjs`
- Loader import scan (must say `imports OK`): `node test/check_imports.cjs plugin.js`
- Secret scan: `gitleaks dir . --no-banner`
- Harness: serve the repo root with `python3 -m http.server 8766`, then run `PLAYWRIGHT_PATH=... CHROME_PATH=... node test/run_headless.cjs full out.json`. This takes several minutes, so run it in the background.
- Core patch: `bash core-patch/reapply.sh [hermes-agent dir]`, then Cmd+Q.

## Rules

- Never write `import`/`from` followed by a quoted string anywhere in `plugin.js` except the real SDK/React imports. The loader regex-scans comments too.
- Every character on screen maps to a real entity. No filler agents and no invented counts.
- Before pushing, run gitleaks. Harness fixtures that contain fake credentials carry `gitleaks:allow`.
