#!/usr/bin/env bash
# Launch Claude Code against OpenRouter for the workshop. No Anthropic subscription needed.
# Run it from YOUR OWN repository; the workshop folder is added read-only, as inspiration (see GITHUB_SETUP.md).
# Usage:  cd ~/ai-summer-school-2026 && ~/python-workshop/claude-workshop.sh
#         MODEL=qwen/qwen3-coder-next ~/python-workshop/claude-workshop.sh
set -euo pipefail

command -v claude >/dev/null || { echo "Claude Code not found. Install it first (see workshop handout)."; exit 1; }

# 0. Work happens in your own repository, never in the workshop folder.
WORKSHOP="$(cd "$(dirname "$0")" && pwd)"
if [ "$PWD" = "$WORKSHOP" ]; then
  echo "You are inside the workshop folder. Start from your own repository: cd ~/ai-summer-school-2026"; exit 1
fi
[ -f CLAUDE.md ] || echo "No CLAUDE.md here: copy the rules first (GITHUB_SETUP.md, step 3)."

# 1. Key: env var, else ~/.env (the Claude Code + OpenRouter file from the welcome email), else hidden prompt.
#    The file lives outside every repository; the agent's rules deny reading .env* files.
for ENV_FILE in "$HOME/.env" "$HOME/.env.openrouter"; do
  if [ -z "${OPENROUTER_API_KEY:-}" ] && [ -f "$ENV_FILE" ]; then
    [ -n "$(find "$ENV_FILE" -perm /077)" ] && chmod 600 "$ENV_FILE"
    OPENROUTER_API_KEY=$(sed -nE 's/^[[:space:]]*(export[[:space:]]+)?OPENROUTER_API_KEY=//p' "$ENV_FILE" | head -1 | tr -d "\"' \r")
  fi
done
if [ -z "${OPENROUTER_API_KEY:-}" ]; then
  read -rsp "Paste the workshop OpenRouter key: " OPENROUTER_API_KEY; echo
fi

# 2. Check the key and show what is left on it.
info=$(curl -s -m 15 https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $OPENROUTER_API_KEY" || true)
if ! echo "$info" | grep -q '"data"'; then echo "Key rejected or OpenRouter unreachable."; exit 1; fi
echo "$info" | python3 -c 'import sys,json
d=json.load(sys.stdin)["data"]
lim, rem = d.get("limit"), d.get("limit_remaining")
share = rem / lim if lim and rem is not None else 1
credit = ("plenty left" if share >= 0.5 else "running low: keep prompts short, /clear between topics"
          if share >= 0.15 else "almost used up: tell the instructor")
print("Key OK. Workshop credit: " + credit + ". Valid until: " + (str(d["expires_at"])[:10] if d.get("expires_at") else "the end of the school"))' 2>/dev/null || echo "Key OK."

# 3. Model choice (tested with Claude Code tool use). Override with MODEL=...
if [ -z "${MODEL:-}" ]; then
  echo
  echo "Pick a model:"
  echo "  1) deepseek/deepseek-v4-pro      (default, best coder of the cheap ones)"
  echo "  2) qwen/qwen3-coder-next         (cheaper, good for short tasks)"
  echo "  3) qwen/qwen3.8-27b:free         (free, but shared 1000 requests/day for the whole class)"
  read -rp "Choice [1]: " c
  case "${c:-1}" in 2) MODEL=qwen/qwen3-coder-next;; 3) MODEL=qwen/qwen3.8-27b:free;; *) MODEL=deepseek/deepseek-v4-pro;; esac
fi
echo "Using $MODEL"

# 4. Point Claude Code at OpenRouter, keep every model slot on the chosen model.
export ANTHROPIC_BASE_URL=https://openrouter.ai/api
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL"
export ANTHROPIC_SMALL_FAST_MODEL="$MODEL"
# Cost guards: compact earlier (shorter context = cheaper turns), no background traffic.
export CLAUDE_CODE_MAX_CONTEXT_TOKENS="${CLAUDE_CODE_MAX_CONTEXT_TOKENS:-120000}"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
export DISABLE_TELEMETRY=1

echo
echo "Tip: /cost is inaccurate for non-Anthropic models. Keep prompts short; use /clear between topics."
exec claude --add-dir "$WORKSHOP" "$@"     # the agent may read the workshop examples
