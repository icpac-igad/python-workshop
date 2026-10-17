#!/usr/bin/env bash
# One-time GitHub setup for a beginner. The PARTICIPANT runs this in their own terminal, never inside Claude.
# gh uses GitHub's browser device flow: you type a short code on github.com; no token is ever pasted anywhere.
# Run it inside your clone of icpac-igad/python-workshop (branch 2026-10). It creates YOUR OWN GitHub repository
# from that clone, so `git push` goes to your account; the workshop repository stays as the `upstream` remote.
#   ./setup-github.sh <github-username> [repo-name, default acmad2026-python]
set -euo pipefail
user="${1:?usage: ./setup-github.sh <github-username> [repo-name]}"; name="${2:-acmad2026-python}"
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

if git remote get-url origin 2>/dev/null | grep -q 'icpac-igad/python-workshop'; then
  git remote rename origin upstream                 # keep the workshop repo for `git pull upstream 2026-10`
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  gh repo create "$name" --public --source=. --remote=origin --push \
    --description "ACMAD summer school 2026: Python data exploration with a coding agent"
  echo "Created https://github.com/$user/$name and pushed this branch to it."
else
  echo "origin already set: $(git remote get-url origin)"
fi
echo
gh auth status
echo "Done. Next: ./claude-workshop.sh   (then ask the agent to 'commit my work with a clear message and push')"
