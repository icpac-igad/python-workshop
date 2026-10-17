# Hands-on Python data exploration with a coding agent

**ACMAD summer school 2026 · Day 2 · 20 October 2026 · branch `2026-10`**

In this session you load, inspect, explore and visualise real weather and climate data from the cloud:
- ECMWF ensemble forecasts (51 members, East Africa)
- 27 years of CMORPH satellite rainfall extremes (1998–2024)

You do not type Python in this session. Instead you direct a coding agent, [Claude Code](https://docs.claude.com/claude-code), in plain language:
1. You read what it writes.
2. You run it.
3. You check the result against physics.
4. Git keeps the record.

The numbered scripts in `exercises/` are **working starting points**. For each exercise, you ask the agent to read the matching script and write **your own** version in `my_scripts/`, adapted to your town, date or question.

## 1. Get the repository

```bash
git clone -b 2026-10 --single-branch https://github.com/icpac-igad/python-workshop.git acmad2026-python
cd acmad2026-python
```

## 2. Set up (E0, in your own terminal, not inside the agent)

```bash
./setup-nosudo.sh                   # installs uv, gh, claude and the Python environment; no sudo
./setup-github.sh <github-username> # browser login, then creates github.com/<you>/acmad2026-python
./claude-workshop.sh                # asks for your OpenRouter key (hidden input) and starts Claude Code
```

- The GitHub login opens a browser page. You never paste a token anywhere.
- Your personal OpenRouter key arrived by email. Type it only at the hidden prompt of `claude-workshop.sh`.
  **Never paste a key into the agent's chat, a script, or a commit.** Each key has a spending cap and will be switched off after the school.
- After `setup-github.sh`, your repository has two remotes:
  - `origin` is your own repository, where you push.
  - `upstream` is this workshop repository. `git pull upstream 2026-10` fetches instructor updates.
- Prefer conda? Run `mamba env create -f environment.yml`. Then run scripts with `python` instead of `uv run python`.

## 3. How every exercise works: ask, look, check and commit

1. **Ask**: give the agent an instruction in plain language, naming the reference script.
2. **Look**: read the output and the figure in `out/` yourself.
3. **Check and commit**: are the values finite, the units right, the sizes plausible? Then ask the agent to commit,
   with a message that says *why*.

The general prompt pattern:

> *Read `exercises/0N_....py` and run it. Then write `my_scripts/eN_<short_name>.py` that does the same for
> \<my change\>. Run it, show me the result, and tell me what you changed. Then commit.*

The agent follows the project rules in [`CLAUDE.md`](CLAUDE.md):
- Run code with `uv run` only.
- Select small slices before computing.
- Never touch secrets.
- Never commit `out/` or data.
- Never edit the reference scripts.

## 4. Exercises

| Stage | Clock (min) | Reference script | What you ask the agent to build |
|---|---|---|---|
| E0 Setup and orientation | 15–25 | `CLAUDE.md`, `exercises/` | A 5-bullet summary of this repository; a first commit of `NOTES.md` (your name and home town) |
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
  - Ask: *Read CLAUDE.md and exercises/. Tell me in 5 bullets what is here and what you must never do.*
  - Then: *Create NOTES.md with my name and home town, and commit it.*
- **E1**
  - Ask: *Run exercises/01_open_virtual_store.py and explain what was and was not downloaded. Then write my_scripts/e1_<name>.py that reads <variable> for <date>.*
  - Check: is the mean plausible for the region?
- **E2**
  - Ask: *Run exercises/02_read_realized.py. Give me the dimensions, the 38 channels and the latitude order without printing the whole dataset. Then write my_scripts/e2_<town>_plume.py for <town, lat, lon>.*
  - Check: cumulative curves never go down; the spread grows with lead time.
- **E3**
  - First, fill in the table on the slide with a neighbour.
  - Ask: *Run exercises/03_pan_vs_pencil.py. Which layout is better for a map, and which for a time series? Count the chunks each read touches.*
- **E4**
  - Ask: *Run exercises/04_cmorph_return_periods.py. Is the Gumbel fit good at Nairobi? Which year breaks it? Write my_scripts/e4_<town>_extremes.py for my town.*
  - Check: latitude **ascends** in this store, unlike E2.
- **E5**
  - Ask: *Run exercises/05_xclim_heavy_rain.py. In plain words, what does wetdays count? Write my_scripts/e5_<town>_heavy_days.py with a threshold of <N> mm.*
  - Check: daily totals are differences of cumulative `tp`.
- **E6**
  - Ask: *Read exercises/06_forecast_vs_local_extremes.py. Write my_scripts/e6_<town>_exceedance.py for <my town>: use the CMORPH 2-year 24 h level there as the threshold and plot how many members exceed it on each forecast day. List the assumptions you changed.*
  - Check: is the town inside both domains? Are the units the same (mm in 24 h)?
  - Check: the forecast grid is 0.25° (about 28 km) and CMORPH about 8 km, so the nearest points do not cover the same area.
- **E7**
  - Ask: *Show me git status, the diff and git log. Run exercises/07_review_before_push.py. How can I tell this answer is right? Then push.*
  - Check: your repository is visible on GitHub, with no `out/`, data or keys in it.
- **E8**
  - Ask: *Read exercises/08_exceedance_probability_map.py. Write my_scripts/e8_<region>_probability.py for <box or start date>.*
  - Check: why are the probabilities low in July? Is the 2-year level of the *annual maximum* a fair threshold for a single forecast day?

## Data

| Dataset | Store (public, read anonymously from `https://data.source.coop`) | Notes |
|---|---|---|
| ECMWF IFS ensemble, virtual | `e4drr-project/forecasts/ecmwf_ifs_ens_aws_s3_icechunk_vd` | References to about 1.9 PB of GRIB; E1 |
| ECMWF IFS ensemble, realized | `e4drr-project/forecasts/ecmwf-ifs-ea-swio-realized-v3/49r1-jja2025` | `tp(time 92, step 65, number 51, lat 321, lon 261)`, 38 channels; latitude descends; `tp` cumulative metres |
| CMORPH extremes 1998–2024 | `e4drr-project/observations/cmorph_rp_icechunk` | Annual maxima and Gumbel return levels, 9 durations; latitude ascends |

Both stores use *pan* chunks, with one whole map per chunk. Maps are cheap to read. A point time series costs one fetch per time step.

## Repository layout

```
CLAUDE.md               rules the coding agent follows (read it once)
exercises/01..08_*.py   reference scripts, one per stage; they run as they are
my_scripts/             your own scripts, written by the agent (committed)
out/                    figures and local caches (never committed)
setup-nosudo.sh         installs uv, gh, Claude Code and the environment
setup-github.sh         GitHub login and your own copy of this repository
claude-workshop.sh      starts Claude Code with your OpenRouter key
pyproject.toml, uv.lock the Python environment (uv); environment.yml for conda
.claude/settings.json   safety rails: no force-push, reset --hard, env, or reading ~/.ssh and .env
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
