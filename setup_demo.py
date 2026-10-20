# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Setup demo: README steps 1-7, checked from a notebook
#
# *Day 2, 20 October 2026 · Hands-on Python data exploration with a coding agent*
#
# Run the cells one by one (Shift+Enter). Each `%%bash` cell is a small terminal command.
# Two things stay in a **real terminal** (*File → New → Terminal*), because they are interactive:
# editing `~/.env` with `vi` (step 3) and talking to the agent with `ori claude` (steps 4 and 7).
#
# **No cell here prints your key.** Never paste the key into a notebook, a chat or a commit.

# %% [markdown]
# ## Step 1 · JupyterHub account
#
# <https://jupyterhub.acmad.amsaf.cloud/>: *Sign up*, wait for approval (about an hour), log in.
# If you are reading this on the hub, step 1 is done. Who and where am I?

# %% language="bash"
# whoami; hostname; echo "home: $HOME"

# %% [markdown]
# ## Step 2 · Install Claude Code and Ori
#
# The cell installs only what is missing (no sudo; everything goes to `~/.local/bin`), then shows the versions.

# %% language="bash"
# export PATH="$HOME/.local/bin:$PATH"
# grep -q '.local/bin' ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
# command -v claude >/dev/null || curl -fsSL https://claude.ai/install.sh | bash
# command -v ori >/dev/null || curl -fsSL https://openrouter.ai/labs/ori/install.sh | bash
# claude --version; ori --version

# %% [markdown]
# ## Step 3 · Your key in `~/.env`
#
# Do this part **in the terminal**, not here: `vi ~/.env`, press `i`, paste the 3 lines from the email, `Esc`, `:wq`, Enter.
#
# ```
# OPENROUTER_API_KEY=sk-or-v1-...your key from the email...
# ORI_FORCE_OPENROUTER_API_KEY=1
# ORI_MODEL=qwen/qwen3-coder-next
# ```
#
# Then this cell checks the file **without showing the key**: the variable names, the permissions, and the model.

# %% language="bash"
# [ -f ~/.env ] || { echo 'No ~/.env yet: create it in the terminal (step 3).'; exit 0; }
# chmod 600 ~/.env
# echo "permissions: $(stat -c %a ~/.env)  (600 = only you)"
# echo 'variables:'; sed -n 's/^\([A-Z_]*\)=.*/  \1=<set>/p' ~/.env
# grep -h '^ORI_MODEL=' ~/.env | grep -q 'qwen/qwen3-coder-next' && echo 'model: qwen/qwen3-coder-next (good)' || echo 'model: change ORI_MODEL to qwen/qwen3-coder-next'

# %% [markdown]
# Does OpenRouter accept the key? The cell sends it once and prints only *accepted* or *rejected*.

# %% language="bash"
# [ -f ~/.env ] || { echo 'No ~/.env yet (step 3).'; exit 0; }
# set -a; source ~/.env; set +a
# code=$(curl -s -o /dev/null -w '%{http_code}' -m 20 https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $OPENROUTER_API_KEY")
# [ "$code" = 200 ] && echo 'key: accepted' || echo "key: rejected (HTTP $code): check the line in ~/.env"

# %% [markdown]
# ---
#
# ## ▶ Step 4 · THE WORKSHOP STARTS HERE: start Claude Code with Ori (in the terminal)
#
# ```bash
# set -a; source ~/.env; set +a
# cd ~ && ori claude --model qwen/qwen3-coder-next
# ```
#
# - `/status`: the model line must show **`qwen/qwen3-coder-next`**, not a Claude model.
# - `say hello`: it should answer. Then `/exit`.
# - Ori asks you to sign in → `~/.env` was not loaded: run the `set -a ...` line again.
#
# ---

# %% [markdown]
# ## Step 5 · Download the workshop examples (the cell skips the clone if it is already there)

# %% language="bash"
# export PATH="$HOME/.local/bin:$PATH"
# cd ~
# [ -d python-workshop ] || git clone -q -b 2026-10 --single-branch https://github.com/icpac-igad/python-workshop.git
# git -C python-workshop log --oneline -1
# ~/python-workshop/setup-nosudo.sh --skip-env 2>&1 | tail -5
# ls ~/python-workshop/exercises

# %% [markdown]
# ## Step 6 · Your own repository (E0)
#
# Follow [GITHUB_SETUP.md](https://github.com/icpac-igad/python-workshop/blob/2026-10/GITHUB_SETUP.md). The token goes in
# with `gh auth login` **in the terminal**, never here. This cell only checks the result.

# %% language="bash"
# export PATH="$HOME/.local/bin:$PATH"
# gh auth status 2>&1 | grep -E 'Logged in|not logged' || echo 'gh: not logged in yet (GITHUB_SETUP.md)'
# R=~/ai-summer-school-2026
# [ -d $R/.git ] || { echo "No $R yet: GITHUB_SETUP.md section 3."; exit 0; }
# git -C $R remote get-url origin
# git -C $R log --oneline -3
# ls $R

# %% [markdown]
# ## Step 7 · Start the agent from your repository, for every exercise (in the terminal)
#
# ```bash
# cd ~/ai-summer-school-2026
# set -a; source ~/.env; set +a
# ori claude --model qwen/qwen3-coder-next --add-dir ~/python-workshop
# ```
#
# Then follow [workshop-prompts.md](https://github.com/icpac-igad/python-workshop/blob/2026-10/workshop-prompts.md),
# one task per conversation (`/clear` between them).

# %% [markdown]
# ## After the exercises · Measure your work (no agent, no sudo)

# %% language="bash"
# export PATH="$HOME/.local/bin:$PATH"
# cd ~/ai-summer-school-2026 2>/dev/null || cd ~/python-workshop
# uvx pygount --format=summary .
# echo "commits: $(git log --oneline | wc -l)"
