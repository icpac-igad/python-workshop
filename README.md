# Hands-on Python data exploration with a coding agent

**African Summer School on Artificial Intelligence for Weather and Climate Modelling 2026**\
*Theme: Introduction in Artificial Intelligence for Climate Modelling*\
19–23 October 2026 · AIMS, Kigali, Rwanda · Day 2, 20 October 2026 · branch `2026-10`

Session by Nishadh Kalladath, IGAD Climate Prediction and Applications Centre (ICPAC).

In this session you load, inspect, explore and visualise real weather and climate data from the cloud:
- ECMWF ensemble forecasts (51 members, East Africa)
- 27 years of CMORPH satellite rainfall extremes (1998–2024)

You do not type Python in this session. Instead you direct a coding agent, [Claude Code](https://docs.claude.com/claude-code), in plain language:
1. You read what it writes.
2. You run it.
3. You check the result against physics.
4. Git keeps the record.

This repository is **inspiration, not your workspace**. The numbered scripts in `exercises/` are solved examples.
You work in **your own new repository**, and your agent reads these examples to write **your own** scripts there
for your town, dates or question. Every step is committed with a detailed message and pushed to your GitHub,
which becomes your personal record of the work.

## Before the session: steps 1-3 (from the welcome email)

These are the same steps as the welcome email *"Hands-on Python data exploration with Claude code and git/github"*.
Your personal key is **only in that email**: it is never in this repository.

### Step 1 · Create your account on the school JupyterHub

<https://jupyterhub.acmad.amsaf.cloud/>

1. On the login page, click **Sign up** and choose a username and password. You will use them all week.
2. An administrator approves new accounts, usually within an hour. Until then, logging in will not work.
3. Once approved, log in and open a terminal: *File → New → Terminal*.

### Step 2 · Install Claude Code and Ori (in that terminal)

Ori is OpenRouter's launcher ([Ori harness](https://openrouter.ai/docs/guides/ori/harness)). It starts Claude Code on
the workshop model with your key, so you need no Claude subscription.

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc; export PATH="$HOME/.local/bin:$PATH"
curl -fsSL https://claude.ai/install.sh | bash
curl -fsSL https://openrouter.ai/labs/ori/install.sh | bash
claude --version; ori --version
```

### Step 3 · Put your key in `~/.env`

Open the file with `vi ~/.env`. Press `i`, paste these 3 lines with **your key from the email**, press `Esc`, then
type `:wq` and press Enter:

```
OPENROUTER_API_KEY=sk-or-v1-...your key from the email...
ORI_FORCE_OPENROUTER_API_KEY=1
ORI_MODEL=qwen/qwen3-coder-next
```

Then make the file private with `chmod 600 ~/.env`.
- `ORI_FORCE_OPENROUTER_API_KEY=1` makes Ori use your workshop key instead of asking you to sign in.
- If your `~/.env` still says `ORI_MODEL=deepseek/deepseek-v4-pro` from an earlier email, change it to
  `qwen/qwen3-coder-next`. The `--model` option below also takes precedence over it.

---

> ## ▶ THE WORKSHOP STARTS HERE: Step 4 · Start Claude Code with Ori
>
> ```bash
> set -a; source ~/.env; set +a
> cd ~ && ori claude --model qwen/qwen3-coder-next
> ```
>
> - Type `/status`. The model line must show **`qwen/qwen3-coder-next`**, not a Claude model.
> - Type `say hello`. It should answer. Then type `/exit`.
> - If Ori asks you to sign in, `~/.env` was not loaded: run the `set -a ...` line again.
> - If you see `ori: command not found`, run the `export PATH=...` line from Step 2.

---

### Step 5 · Download the workshop examples

```bash
cd ~
git clone -b 2026-10 --single-branch https://github.com/icpac-igad/python-workshop.git
~/python-workshop/setup-nosudo.sh --skip-env      # installs uv and gh (and Claude Code if missing); no sudo
```

You never commit or push to `~/python-workshop`.

### Step 6 · Create your own repository (E0)

Follow **[GITHUB_SETUP.md](GITHUB_SETUP.md)**. It covers:
- the basic ideas of git and GitHub;
- creating an empty repository `ai-summer-school-2026` on github.com;
- creating a **fine-grained token** limited to that one repository, and storing it with `gh auth login` in your own terminal;
- cloning your repository, copying in only the agent rules and environment files, and making your first commit and push.

### Step 7 · Start the agent from your repository, for every exercise

Start it from your own repository, never from `~/python-workshop`:

```bash
cd ~/ai-summer-school-2026
set -a; source ~/.env; set +a
ori claude --model qwen/qwen3-coder-next --add-dir ~/python-workshop
```

- `--add-dir ~/python-workshop` lets the agent **read** the examples. The project rules forbid it to edit them.
- **Model: `qwen/qwen3-coder-next` (Qwen3 Coder Next).** In a cost test on 20 October 2026, the whole workshop
  used about 12% of a participant's credit with it. Do not switch to other models: they can use up the credit
  within a few exercises.
- **Never paste a key or token into the agent's chat, a script, or a commit.**
- Each OpenRouter key carries a small workshop credit and is switched off after the school. Your GitHub token
  expires on 31 October. Keep prompts short, and use `/clear` between topics.
- Every prompt, step by step: **[workshop-prompts.md](workshop-prompts.md)**.

## How every exercise works: ask, look, check and commit

1. **Ask**: give the agent an instruction in plain language, naming the example that inspires it.
2. **Look**: read the output and the figure in `out/` yourself.
3. **Check and commit**: are the values finite, the units right, the sizes plausible? Then commit with a
   detailed message (what, why, result, how checked) and push.

The general prompt pattern:

> *Read `~/python-workshop/exercises/0N_....py` for inspiration (you may run it). Write my own
> `scripts/eN_<short_name>.py` for \<my question\>, borrowing only what is needed. Run it and show me the result.
> Then show the diff and commit with a title and a body: what changed, why, the key result and how we checked it.
> Then push.*

The agent follows the project rules in [`CLAUDE.md`](CLAUDE.md), which you copied into your repository:
- Run code with `uv run` only.
- Select small slices before computing.
- Never touch keys or tokens.
- Never commit `out/` or data.
- Never edit, copy wholesale or push the workshop examples.

### Cost: the six habits

Your key carries a small credit. **[workshop-prompts.md](workshop-prompts.md)** gives every step's prompt in order,
written to be cheap:
1. `/clear` before each new step.
2. Name the file you mean.
3. Ask for "3 lines" or "only the numbers".
4. Never let the agent read notebooks or images.
5. Run the example before asking about it.
6. Type the plain git commands (`status`, `log`, `switch`, `revert`, `tag`) yourself.

### Explore a script as a notebook (no agent, no credit)

Your scripts are written with `# %%` cell markers, so jupytext turns them into notebooks:

```bash
uv run python -m ipykernel install --user --name ai-school-2026 --display-name "AI school 2026"   # once
uv run jupytext --set-formats ipynb,py:percent scripts/e6_<town>_exceedance.py                   # pair .py and .ipynb
# explore in JupyterLab with the "AI school 2026" kernel, then copy your changes back into the script:
uv run jupytext --sync scripts/e6_<town>_exceedance.ipynb
```

Commit the `.py`, not the `.ipynb`: notebooks are in `.gitignore`, because their outputs bloat diffs and history.
Never ask the agent to read a notebook or a plot image. Look yourself, and tell it what you see.

### Measure your work: files and lines of code (no agent, no sudo)

`pygount` counts files and lines of code per language. `uvx` runs it without installing anything and without sudo.
It skips hidden folders such as `.venv` and `.git`.

```bash
cd ~/ai-summer-school-2026
uvx pygount --format=summary .                    # your repository: languages, files, code and comment lines
git log --oneline | wc -l                         # and how many commits record the work
```

To compare with the case study on the slides, an operational AI forecasting pipeline written by a coding agent:

```bash
git clone --depth 1 https://github.com/icpac-igad/ea-aifs.git /tmp/ea-aifs
uvx pygount --format=summary /tmp/ea-aifs         # about 228 files and 20,000 lines of Python code (October 2026)
```

The workshop examples themselves are 8 Python files and 467 lines of code. The slides use `cloc` for the same
count. Without sudo, cloc is a single Perl script: download `cloc-2.10.pl` from
<https://github.com/AlDanial/cloc/releases> and run `perl cloc-2.10.pl .`

## Exercises

| Stage | Clock (min) | Example for inspiration | What you ask the agent to build in your repository |
|---|---|---|---|
| E0 Setup and orientation | 15–25 | `GITHUB_SETUP.md`, `CLAUDE.md` | Your own repository and token; a 5-bullet summary of the examples; a commit of `NOTES.md` (your name and home town) |
| E1 Load: a 2 PB virtual store | 25–35 | `01_open_virtual_store.py` | Read one field for another date, variable (`t2m`, `msl`, ...) or box; explain what was *not* downloaded |
| E2 Inspect: a realized store | 35–50 | `02_read_realized.py` | The ensemble rainfall plume at your town; dimensions, channels and latitude order |
| E3 Explore: pan vs pencil chunks | 50–70 | `03_pan_vs_pencil.py` | Predict, then measure, how many chunks a map read and a point-series read touch in each layout |
| E4 Visualise: observed extremes | 70–85 | `04_cmorph_return_periods.py` | Return levels and the 27 annual maxima at your town; does the Gumbel fit match the data? |
| E5 Analyse: heavy-rain days | 85–95 | `05_xclim_heavy_rain.py` | Members with a heavy-rain day at your town, with your own threshold |
| E6 Forecast vs local extremes | 95–110 | `06_forecast_vs_local_extremes.py` | Members above your town's CMORPH 2-year 24 h level, per forecast day |
| E7 Review and publish | 110–115 | `07_review_before_push.py` | Status, diff and log; the pre-push check; then `git push` |
| E8 Stretch (take-home) | after the session | `08_exceedance_probability_map.py` | A map of the chance of exceeding the *local* 2-year level, for another box or start date |

### Prompt cards

- **E0**
  - Ask: *Read CLAUDE.md and ~/python-workshop/exercises/. Tell me in 5 bullets what is here and what you must never do.*
  - Then: *Run git remote -v and gh auth status and explain them, without showing any token. Create NOTES.md with my name and home town, commit it with a detailed message, and push.*
- **E1**
  - Ask: *Run ~/python-workshop/exercises/01_open_virtual_store.py and explain what was and was not downloaded. Then write scripts/e1_<name>.py that reads <variable> for <date>.*
  - Check: is the mean plausible for the region?
- **E2**
  - Ask: *Run ~/python-workshop/exercises/02_read_realized.py. Give me the dimensions, the 38 channels and the latitude order without printing the whole dataset. Then write scripts/e2_<town>_plume.py for <town, lat, lon>.*
  - Check: cumulative curves never go down; the spread grows with lead time.
- **E3**
  - First, fill in the table on the slide with a neighbour.
  - Ask: *Run ~/python-workshop/exercises/03_pan_vs_pencil.py. Which layout is better for a map, and which for a time series? Count the chunks each read touches.*
- **E4**
  - Ask: *Run ~/python-workshop/exercises/04_cmorph_return_periods.py. Is the Gumbel fit good at Nairobi? Which year breaks it? Write scripts/e4_<town>_extremes.py for my town.*
  - Check: latitude **ascends** in this store, unlike E2.
- **E5**
  - Ask: *Run ~/python-workshop/exercises/05_xclim_heavy_rain.py. In plain words, what does wetdays count? Write scripts/e5_<town>_heavy_days.py with a threshold of <N> mm.*
  - Check: daily totals are differences of cumulative `tp`.
- **E6**
  - Ask: *Read ~/python-workshop/exercises/06_forecast_vs_local_extremes.py. Write scripts/e6_<town>_exceedance.py for <my town>: use the CMORPH 2-year 24 h level there as the threshold and plot how many members exceed it on each forecast day. List the assumptions you changed.*
  - Check: is the town inside both domains? Are the units the same (mm in 24 h)?
  - Check: the forecast grid is 0.25° (about 28 km) and CMORPH about 8 km, so the nearest points do not cover the same area.
- **E7**
  - Ask: *Show me git status, the diff and git log. Run ~/python-workshop/exercises/07_review_before_push.py. How can I tell this answer is right? Then push.*
  - Check: your repository is visible on GitHub, with no `out/`, data or keys in it.
- **E8**
  - Ask: *Read ~/python-workshop/exercises/08_exceedance_probability_map.py. Write scripts/e8_<region>_probability.py for <box or start date>.*
  - Check: why are the probabilities low in July? Is the 2-year level of the *annual maximum* a fair threshold for a single forecast day?

## Data

| Dataset | Store (public, read anonymously from `https://data.source.coop`) | Notes |
|---|---|---|
| ECMWF IFS ensemble, virtual | `e4drr-project/forecasts/ecmwf_ifs_ens_aws_s3_icechunk_vd` | References to about 1.9 PB of GRIB; E1 |
| ECMWF IFS ensemble, realized | `e4drr-project/forecasts/ecmwf-ifs-ea-swio-realized-v3/49r1-jja2025` | `tp(time 92, step 65, number 51, lat 321, lon 261)`, 38 channels; latitude descends; `tp` cumulative metres |
| CMORPH extremes 1998–2024 | `e4drr-project/observations/cmorph_rp_icechunk` | Annual maxima and Gumbel return levels, 9 durations; latitude ascends |

Both stores use *pan* chunks, with one whole map per chunk. Maps are cheap to read. A point time series costs one fetch per time step.

## Layout

```
~/python-workshop/ (this repository: examples, read-only)
  exercises/01..08_*.py   solved examples, one per stage; they run as they are
  CLAUDE.md               agent rules (copy into your repository)
  .claude/settings.json   safety rails: no force-push, reset --hard, env, tokens; examples cannot be edited
  pyproject.toml, uv.lock Python environment (copy into your repository); environment.yml for conda
  GITHUB_SETUP.md         your own repository and token, step by step
  workshop-prompts.md     every step's prompt in order, written to keep the cost low
  setup-nosudo.sh         installs uv, gh and Claude Code

~/ai-summer-school-2026/ (your repository: origin = github.com/<you>/ai-summer-school-2026)
  scripts/eN_*.py         your own scripts, written by the agent (committed)
  NOTES.md                your notes (committed)
  out/                    figures and caches (never committed)
```

## Links

- Data pipeline and case studies:
  - [CMORPH return periods](https://github.com/icpac-igad/ibf-thresholds-triggers) (branch `xarray-method`, `thresholds/CMORPH`)
  - [AIFS case study](https://github.com/icpac-igad/ea-aifs)
  - [Code for Earth demo 4](https://github.com/icpac-igad/code-for-earth)
- Tools:
  - [Icechunk](https://icechunk.io)
  - [xarray](https://docs.xarray.dev)
  - [xclim](https://xclim.readthedocs.io)
  - [uv](https://docs.astral.sh/uv)
  - [Claude Code](https://docs.claude.com/claude-code)
- Earlier trainings live on other branches of this repository: `fcptw-6`, `sewaa-ws-202407`, `sewaa25`.
