#!/usr/bin/env bash
# One-time GitHub setup for a beginner. The PARTICIPANT runs this in their own terminal, never inside Claude.
# gh uses GitHub's browser device flow: you type a short code on github.com; no token is ever pasted anywhere.
# Run it inside the downloaded workshop folder. It copies the workshop files (no git history) into a NEW folder,
# starts a fresh git repository there, and creates YOUR OWN GitHub repository for it. You then work, commit and push
# only in that new folder; the downloaded workshop folder is just the starting material and can be deleted.
#   ./setup-github.sh <github-username> [repo-name, default acmad2026-python]
set -euo pipefail
user="${1:?usage: ./setup-github.sh <github-username> [repo-name]}"; name="${2:-acmad2026-python}"
dest="${DEST:-$HOME/$name}"
cd "$(dirname "$0")"
command -v gh >/dev/null || { echo "gh not found: run ./setup-nosudo.sh first"; exit 1; }

if ! gh auth status >/dev/null 2>&1; then
  echo "A code and a URL will appear. Open the URL in your own browser, enter the code, approve."
  gh auth login --hostname github.com --git-protocol https --web
fi
gh auth setup-git                                    # git uses gh as its credential helper

# Commit identity: GitHub's noreply address, so no personal email lands in public history.
id=$(gh api user --jq .id)
git config --global user.name "$user"
git config --global user.email "${id}+${user}@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global push.default current

if [ -e "$dest" ]; then echo "$dest already exists: remove it or pick another repo name"; exit 1; fi
if gh repo view "$user/$name" >/dev/null 2>&1; then echo "github.com/$user/$name already exists: pick another repo name"; exit 1; fi

# Copy only the committed workshop files: no .git history, no out/, no .venv.
mkdir -p "$dest"
if [ -d .git ]; then git archive HEAD | tar -x -C "$dest"          # a git clone: committed files only
else tar --exclude=.venv --exclude=out --exclude=__pycache__ --exclude='.env*' -cf - . | tar -x -C "$dest"; fi   # a ZIP download
cd "$dest"
git init -q -b main
git add -A
git commit -q -m "Start from the ACMAD 2026 workshop materials"
gh repo create "$name" --public --source=. --remote=origin --push \
  --description "ACMAD summer school 2026: Python data exploration with a coding agent"
echo "Created https://github.com/$user/$name and your working folder $dest"
echo
gh auth status
echo "Done. Next:  cd $dest && ./setup-nosudo.sh && ./claude-workshop.sh   (then ask the agent to 'commit my work with a clear message and push')"
