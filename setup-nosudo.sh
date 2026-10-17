#!/usr/bin/env bash
# Install uv, GitHub CLI and Claude Code into ~/.local/bin, then build the Python environment. No sudo.
# Works on a locked-down JupyterHub terminal. Re-running is safe.
#   ./setup-nosudo.sh [--skip-claude] [--skip-env] [--check-only]
set -euo pipefail
BIN="$HOME/.local/bin"; mkdir -p "$BIN"; export PATH="$BIN:$PATH"
SKIP_CLAUDE=0; SKIP_ENV=0; CHECK=0
for a in "$@"; do case $a in --skip-claude) SKIP_CLAUDE=1;; --skip-env) SKIP_ENV=1;; --check-only) CHECK=1;; esac; done
say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
ok()  { printf '  ok   %s\n' "$*"; }
bad() { printf '  FAIL %s\n' "$*"; FAILED=1; }
FAILED=0

say "1. Network (a locked-down hub may block these hosts)"
for u in https://github.com https://api.github.com https://astral.sh https://downloads.claude.ai https://openrouter.ai https://data.source.coop https://pypi.org; do
  code=$(curl -s -o /dev/null -m 10 -w '%{http_code}' "$u" || echo 000)
  if [ "$code" != "000" ]; then ok "$u ($code)"; else bad "$u unreachable: ask the hub admin to allow it"; fi
done
[ "$CHECK" = 1 ] && { [ "$FAILED" = 0 ] && echo "all reachable" || echo "some hosts blocked"; exit $FAILED; }

say "2. uv (Python + environments)"
if ! command -v uv >/dev/null; then curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null; fi
export PATH="$BIN:$PATH"; ok "$(uv --version)"

say "3. GitHub CLI (gh)"
if ! command -v gh >/dev/null; then
  case "$(uname -m)" in x86_64) arch=amd64;; aarch64|arm64) arch=arm64;; *) bad "unsupported CPU $(uname -m)"; exit 1;; esac
  tag=$(curl -s https://api.github.com/repos/cli/cli/releases/latest | python3 -c 'import sys,json;print(json.load(sys.stdin)["tag_name"])' 2>/dev/null || echo v2.102.0)
  tmp=$(mktemp -d); curl -sL "https://github.com/cli/cli/releases/download/$tag/gh_${tag#v}_linux_${arch}.tar.gz" | tar xz -C "$tmp"
  cp "$tmp"/gh_*/bin/gh "$BIN/gh"; rm -rf "$tmp"
fi
ok "$(gh --version | head -1)"

if [ "$SKIP_CLAUDE" = 0 ]; then
  say "4. Claude Code"
  command -v claude >/dev/null || curl -fsSL https://claude.ai/install.sh | bash >/dev/null
  command -v claude >/dev/null && ok "claude $(claude --version 2>/dev/null | head -1)" || bad "claude not on PATH (open a new terminal)"
fi

if [ "$SKIP_ENV" = 0 ]; then
  say "5. Python environment (Python 3.12 is fetched by uv if the system one is older)"
  cd "$(dirname "$0")"
  uv sync --python 3.12 --extra virtual
  uv run python -c "import icechunk, xarray, xclim, zarr; print('  ok   icechunk', icechunk.__version__, '| xarray', xarray.__version__, '| xclim', xclim.__version__)"
fi

say "Make the PATH permanent"
grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
[ "$FAILED" = 0 ] && echo "Setup complete." || { echo "Finished with problems (see FAIL lines)."; exit 1; }
