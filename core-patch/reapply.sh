#!/usr/bin/env bash
# Re-apply the hermes-office v5.1 core patch (session.children RPC) after `hermes update`.
# Idempotent: already present -> skip. Always `git apply --check` before touching anything.
# Usage: bash reapply.sh [HERMES_AGENT_DIR]   (default ~/.hermes/hermes-agent)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PATCH="$HERE/office_core.patch"   # v5.1 session.children + v5.7 session.activity
AGENT="${1:-$HOME/.hermes/hermes-agent}"

[ -f "$PATCH" ] || { echo "patch not found: $PATCH" >&2; exit 2; }
git -C "$AGENT" rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "not a git checkout: $AGENT" >&2; exit 2; }
cd "$AGENT"

# Present == the method is registered in the handler module AND the SessionDB reader exists.
if grep -q '@method("session.children")' tui_gateway/methods_session.py 2>/dev/null \
   && grep -q '@method("session.activity")' tui_gateway/methods_session.py 2>/dev/null \
   && grep -q 'def list_active_tool_calls' hermes_state_sessions.py 2>/dev/null; then
  echo "session.children + session.activity already present — skip"
  exit 0
fi

# Reverse-applies cleanly == exactly this patch is already in the tree.
if git apply --reverse --check "$PATCH" >/dev/null 2>&1; then
  echo "patch already applied — skip"
  exit 0
fi

if ! git apply --check "$PATCH" 2>/tmp/hermes-office-patch-check.log; then
  echo "patch does NOT apply cleanly on $(git rev-parse --short HEAD) — nothing changed." >&2
  echo "Details: /tmp/hermes-office-patch-check.log. Upstream moved; regenerate the patch." >&2
  exit 1
fi

git apply "$PATCH"
echo "applied session.children patch on $(git rev-parse --short HEAD)"
echo "Restart Hermes Desktop (Cmd+Q, reopen) so its backend loads the new method."
