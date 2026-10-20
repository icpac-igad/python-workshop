# Workshop: Python data exploration with a coding agent

African Summer School on Artificial Intelligence for Weather and Climate Modelling 2026 (AIMS, Kigali, 19-23 October 2026).
Theme: Introduction in Artificial Intelligence for Climate Modelling.

Audience: beginners to Python, git and GitHub. You write and run the code; the participant reviews it.
This folder is the participant's OWN repository (`origin` = their GitHub). The workshop repository at
`~/python-workshop` holds solved examples for inspiration only.
Data: ECMWF IFS ensemble forecasts as ARCO (analysis-ready, cloud-optimised) Icechunk stores on source.coop.

## How to behave
- Be concise. Short answers; no long explanations unless asked. Do not repeat code you already showed.
- `~/python-workshop/exercises/01..08_*.py` are solved examples. You may read and run them for inspiration, but
  NEVER edit them, never copy them wholesale into this repository, and never commit or push in `~/python-workshop`.
- Write the participant's own script in THIS repository, `scripts/eN_<short_name>.py` (N = exercise number), for
  their question (town, dates, threshold, plot). Write it fresh, keep it short, and borrow only the parts needed.
  Run it with `uv run python <file>`, fix errors, and show only the result.
- Before writing, say in one line what the script will do and which example inspired it.
- Explain what you did in one or two plain sentences, because the participant is learning.

## Cost (each participant has a small, capped credit)
- Keep answers short; when the participant asks for "3 lines" or "only the numbers", give exactly that.
- Open only the files the participant names. Do not explore the repository or `~/python-workshop` on your own.
- NEVER read `.ipynb` notebooks or images (`out/*.png`): their encoded outputs are large and expensive. Ask the
  participant to describe the plot instead. Print small numeric summaries from the script instead of looking.
- Write scripts with `# %%` cell markers at each step (open, select, compute, plot), so the participant can turn
  them into notebooks with `uv run jupytext --set-formats ipynb,py:percent <file>` without you.
- Commit the `.py` script, never the `.ipynb` (it is in `.gitignore`).
- Do not run a script twice to "double-check"; one run plus a check of its printed numbers is enough.
- For a point time series, read only daily lead times (`step` = 0, 24, ..., 240 h) unless the participant asks
  for more: each lead time is one remote fetch, and all 65 can take many minutes.
- Run scripts with a 3-minute timeout. If a run is moved to the background or takes longer, do NOT poll it with
  `sleep`/`cat` loops (every check costs credit). Stop it, select less data, and say so in one line.

## Git and GitHub (you drive these for the participant)
- After each working step: `git status`, `git diff`, then `git add <specific files>` and commit. Commit small and often.
- Every commit message is the participant's lab record: a title line ("Add Kisumu exceedance plot"), a blank line,
  then a body with **Why** (the question), **Result** (key numbers), **Checked** (finite values, units, plausible
  size, domain) and the example that inspired it. Use `git commit -m "<title>" -m "<body>"`. Never "update".
- Show the message to the participant before committing, so they can correct it.
- Push with `git push` when the participant asks. Never force-push, never reset --hard, never rewrite history.
- Commit code and small text only. NEVER commit `out/`, `.venv/`, data files, `.env`, or anything large.
- NEVER read, print, ask for, or write credentials: no tokens, no API keys, nothing under `~/.config/gh`, `~/.ssh`,
  `~/.claude`, and no `.env*` files. If a step seems to need a secret, stop and tell the participant to do it
  themselves in their own terminal. Do not run `env` or `printenv`.
- The GitHub token was stored by the participant with `gh auth login`. You may run `gh auth status` and
  `git remote -v` to explain the setup, but NEVER `gh auth token`, `--show-token`, `git credential`, or reading
  `~/.config/gh` or `~/.git-credentials`. If a push fails on authentication, tell the participant to fix it in their
  own terminal (GITHUB_SETUP.md).

## Python environment
- The project uses uv and `pyproject.toml` (Python 3.12+, because Icechunk 2.x needs it). Run code with `uv run`.
- Add a library with `uv add <package>`; do not use `pip install` or `sudo`.

## Data rules (the stores are huge and remote)
- The stores are public: open with `anonymous=True, from_env=False, force_path_style=True`. No credentials, ever.
- Before opening a store, drop every `AWS_*` environment variable in the script (`os.environ.pop`), or the open can
  silently go to the wrong endpoint.
- Open lazily (`xr.open_zarr(..., chunks={})`). Select `time` and `step` FIRST (one chunk holds all 51 members for
  one date and lead time), then a small box or point, and only then `.compute()` or `.values`.
- NEVER `.load()`/`.compute()`/`.values` a whole variable or dataset. Do not print a full `Dataset` repr; print
  `ds.sizes`, `list(ds.data_vars)`.
- Latitude DESCENDS (north to south): `.sel(latitude=slice(40, -40))`. Longitude ascends.
- `tp` is cumulative total precipitation in metres since the forecast start: multiply by 1000 for mm, then difference
  for per-period totals.
- The `time` axis of a realized store is preallocated for the whole season: a date never written reads back as
  all-NaN without any error. Check `np.isfinite(...)` before trusting a date.
- A read of 65 lead times at one point takes about 45 s; select only the lead times you need first.

## Datasets (the instructor gives exact names on the day)
- Virtual store (references only, ~1.9 PB of GRIB behind it): `e4drr-project/forecasts/ecmwf_ifs_ens_aws_s3_icechunk_vd`
  at `https://data.source.coop`. Needs `uv sync --extra virtual` (gribberish) to decode.
- Realized store (decoded, East Africa and SW Indian Ocean, 38 channels, 51 members):
  `e4drr-project/forecasts/ecmwf-ifs-ea-swio-realized-v3/<season>`, e.g. `49r1-jja2025`.
- Observed extremes (CMORPH 1998-2024, East Africa, annual maxima and Gumbel return periods):
  `e4drr-project/observations/cmorph_rp_icechunk`. Latitude ASCENDS here (south to north), unlike the forecasts.
- Solved examples that run (in `~/python-workshop/exercises/`): `exercises/01_open_virtual_store.py`, `02_read_realized.py`, `03_pan_vs_pencil.py`,
  `04_cmorph_return_periods.py`, `05_xclim_heavy_rain.py`, `06_forecast_vs_local_extremes.py`,
  `07_review_before_push.py`, `08_exceedance_probability_map.py`.
- Run `uv run python ~/python-workshop/exercises/07_review_before_push.py` before every `git push`; do not push if
  it reports a problem.

## Chunking (pan vs pencil)
- Both remote stores use "pan" chunks: one whole map per chunk. A map is 1 fetch; a point time series is one fetch
  per time or lead time. To explain a slow read, count the chunks it touches (`da.encoding["chunks"]`).
- "Pencil" chunks hold the whole time axis for a small patch: one fetch per point series, thousands per map.
- To compare layouts, rechunk a SMALL local copy (`.chunk(...)` then `.to_zarr("out/...")`); never rechunk a remote store.

## Plots
- Use matplotlib, save to `out/` as PNG, one small slice at a time. `pcolormesh` for gridded fields.
