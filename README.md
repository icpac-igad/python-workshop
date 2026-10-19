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

## 1. Download the workshop examples (in your own terminal)

```bash
cd ~
git clone -b 2026-10 --single-branch https://github.com/icpac-igad/python-workshop.git
~/python-workshop/setup-nosudo.sh --skip-env      # installs uv, gh and claude; no sudo
```

Claude Code, Ori and `~/.env` were set up from the welcome email. If not, see the email, or install Ori with
`curl -fsSL https://openrouter.ai/labs/ori/install.sh | bash` once `~/.local/bin` is on your `PATH`.

You never commit or push to `~/python-workshop`.

## 2. Create your own repository (E0)

Follow **[GITHUB_SETUP.md](GITHUB_SETUP.md)**. It covers:
- the basic ideas of git and GitHub;
- creating an empty repository `ai-summer-school-2026` on github.com;
- creating a **fine-grained token** limited to that one repository, and storing it with `gh auth login` in your own terminal;
- cloning your repository, copying in only the agent rules and environment files, and making your first commit and push.

Then start the agent **from your repository**, never from `~/python-workshop`:

```bash
cd ~/ai-summer-school-2026
set -a; source ~/.env; set +a                    # your key and model, set up from the welcome email
ori claude --model deepseek/deepseek-v4-pro --add-dir ~/python-workshop
```

- `ori` is OpenRouter's launcher ([Ori harness](https://openrouter.ai/docs/guides/ori/harness)). It runs Claude Code on
  the chosen OpenRouter model with your workshop key, so you need no Claude subscription.
- `--add-dir ~/python-workshop` lets the agent **read** the examples. The project rules forbid it to edit them.
- In the agent, `/status` must show `deepseek/deepseek-v4-pro`. A cheaper model for short tasks is
  `--model qwen/qwen3-coder-next`.
- Your personal OpenRouter key arrived by email, with the 3 lines for `~/.env`: a private file (`chmod 600`) in your
  home folder, outside every repository.
- **Never paste a key or token into the agent's chat, a script, or a commit.**
- Each OpenRouter key carries a small workshop credit and is switched off after the school. Your GitHub token
  expires on 31 October. Keep prompts short, and use `/clear` between topics.

## 3. How every exercise works: ask, look, check and commit

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

## 4. Exercises

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
