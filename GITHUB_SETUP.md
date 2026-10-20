# Your own GitHub repository: a personal record of your scripts

*African Summer School on Artificial Intelligence for Weather and Climate Modelling 2026 · Theme: Introduction in
Artificial Intelligence for Climate Modelling · 19–23 October 2026 · AIMS, Kigali, Rwanda*

In this session, GitHub is your **lab notebook**. Every script you and the coding agent write is saved as a
*commit* with a message that says what changed and why. Each commit is then *pushed* to your own repository
on GitHub.

This workshop repository (`python-workshop`) is **not** where you work. It contains solved examples that you
and your agent read for inspiration. You never commit or push to it.

## 1. Git and GitHub in five words

| Word | Meaning |
|---|---|
| **repository** (repo) | A project folder whose full history git keeps. |
| **commit** | A saved snapshot of your files, with a message explaining the change. It is a restore point. |
| **push** | Copies your new commits from your computer to GitHub. |
| **remote** (`origin`) | The GitHub address your repository pushes to. |
| **token** | A password-like key that lets git on your computer push to your GitHub repository, and nothing more. |

```
your computer                                    github.com/<you>/ai-summer-school-2026
~/ai-summer-school-2026  --git commit-->  history  --git push (uses token)-->  backup, sharing, record
~/python-workshop   (read-only examples, inspiration only)
```

## 2. On github.com (in your browser)

1. **Account.** Sign in, or create a free account at <https://github.com/signup>.
2. **Private email for commits.** Go to *Settings → Emails* and tick **Keep my email addresses private**.
   Copy the address shown, which looks like `12345678+you@users.noreply.github.com`. You need it in step 3.
3. **Create your empty repository.** Click *+ → New repository* and fill it in as follows:
   - Name: `ai-summer-school-2026`
   - Visibility: Public (or Private)
   - Do **not** add a README, .gitignore or licence. The repository must start empty.
4. **Create a fine-grained token** at *Settings → Developer settings → Personal access tokens →
   Fine-grained tokens → Generate new token* (<https://github.com/settings/personal-access-tokens/new>):
   - **Token name:** `ai-summer-school-2026-laptop`
   - **Expiration:** custom, `2026-10-31`. A short life limits the damage if it leaks.
   - **Repository access:** *Only select repositories* → `ai-summer-school-2026`
   - **Permissions → Repository permissions → Contents:** *Read and write*. GitHub adds *Metadata: Read-only*
     automatically. Leave everything else at *No access*.
   - Click **Generate token** and copy it (`github_pat_...`). GitHub shows it **only once**.

   This token can only read and write files in that one repository, until 31 October. It cannot delete the
   repository, see your other repositories or change your account.

> **Keep the token secret.** Never paste it into the agent's chat, a script, a commit, a slide or a message.
> You paste it exactly once, at a hidden prompt in your own terminal (step 3 below).

## 3. In your own terminal (not inside Claude Code)

Store the token with the GitHub CLI. `gh` was installed by `setup-nosudo.sh`. Git then pushes without asking
for it again.

```bash
gh auth login --hostname github.com --git-protocol https
#   ? How would you like to authenticate GitHub CLI?  ->  Paste an authentication token
#   ? Paste your authentication token:                ->  (paste; nothing is shown)
gh auth setup-git                       # git now uses gh to supply the token when you push
gh auth status                          # shows "Logged in to github.com account <you>"; never add --show-token

git config --global user.name  "<your name or GitHub username>"
git config --global user.email "<the noreply address from step 2.2>"
git config --global init.defaultBranch main
```

Clone your empty repository next to the workshop folder. Then copy in only the **rules and environment** files.
Do not copy the exercises: your agent writes your own scripts.

```bash
cd ~
git clone https://github.com/<you>/ai-summer-school-2026.git      # "You appear to have cloned an empty repository" is fine
cd ai-summer-school-2026
cp ~/python-workshop/{CLAUDE.md,pyproject.toml,uv.lock,.gitignore} .
mkdir -p .claude scripts && cp ~/python-workshop/.claude/settings.json .claude/
uv sync --extra virtual                                      # the Python environment for your repository
git add -A
git commit -m "Start my AI Summer School 2026 workshop repository" \
           -m "Agent rules (CLAUDE.md), the Python environment (pyproject.toml, uv.lock) and what git must ignore."
git push -u origin main                                      # first push: proves the token works
```

Open `https://github.com/<you>/ai-summer-school-2026`. Your first commit should be there.

If `git push` asks for a username and password, `gh auth setup-git` did not run. Run it, then push again.

## 4. Start the agent from your repository, then ask it to explain and check

```bash
cd ~/ai-summer-school-2026
set -a; source ~/.env; set +a              # your OpenRouter key and model, from the welcome email
ori claude --model qwen/qwen3-coder-next --add-dir ~/python-workshop
                                           # Claude Code starts here and may READ ~/python-workshop for inspiration
```

Ask the agent to explain the setup to you and check it. **The agent never sees the token**: the project rules
forbid reading `~/.config/gh` or running `gh auth token`. It can only see that a login exists.

- *"Run `git remote -v`, `git log --oneline` and `gh auth status`. Explain each line to me as a beginner, without
  showing any token."*
- *"When I push, where do my files go, who can see them, and what does my token allow and not allow?"*
- *"Run `uv run python ~/python-workshop/exercises/07_review_before_push.py`. Is anything secret or large tracked?"*
- *"Read ~/python-workshop/exercises/. In 5 bullets: what does each example do? Then tell me what you must never do
  here."*

## 5. One commit per working step, each with a detailed message

Your commit history is the record of your work. Ask for a commit after **every** step that works, and ask
for a message with a short title plus a body that covers four things:

1. **What** changed (which file, which plot)
2. **Why** you made the change
3. **What came out** (key numbers)
4. **How you checked it**

```
Add Kisumu exceedance plot against the CMORPH 2-year 24 h level

Why: E6, compare the ECMWF ensemble from 2025-07-16 with Kisumu's observed extremes.
Result: threshold 86.9 mm (CMORPH 2-year, 24 h); 0 of 51 members exceed it on days 1-10;
wettest member 20.7 mm on day 6 (dry season, so plausible).
Checked: Kisumu lies inside both domains; units are mm in 24 h for both; the forecast grid
(0.25 deg) and CMORPH (8 km) nearest points do not cover the same area.
Inspired by python-workshop/exercises/06_forecast_vs_local_extremes.py; written for my town.
```

The prompt to use every time:

> *"Show me git status and the diff. Then commit with a title and a body that say what changed, why, the
> key result and how we checked it. Then push."*

Then read the message the agent wrote and correct it if it is wrong. It is your record.

## 6. After the school

- The token stops working on 31 October. To revoke it earlier, go to *Settings → Developer settings → Personal
  access tokens*. Your repository and its history stay on GitHub.
- To keep working later, create a new fine-grained token the same way and run `gh auth login` again.
- On Day 3 your group can start from this repository: *Settings → Collaborators* adds teammates.
