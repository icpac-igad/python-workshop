# Workshop: Python data exploration with a coding agent

Audience: beginners to Python, git and GitHub. You write and run the code; the participant reviews it.
Data: ECMWF IFS ensemble forecasts as ARCO (analysis-ready, cloud-optimised) Icechunk stores on source.coop.

## How to behave
- Be concise. Short answers; no long explanations unless asked. Do not repeat code you already showed.
- `exercises/01..08_*.py` are the instructor's reference scripts: read and run them, but do NOT edit them.
- Write the participant's own code to `my_scripts/eN_<short_name>.py` (N = exercise number), starting from the
  matching reference script. Run it with `uv run python <file>`, fix errors, and show only the result.
- Before writing, say in one line what you will change from the reference script (town, dates, threshold, plot).
- Explain what you did in one or two plain sentences, because the participant is learning.

## Git and GitHub (you drive these for the participant)
- After each working step: `git status`, `git diff`, then `git add <specific files>` and `git commit -m "<what and why>"`.
  Commit small and often. Write plain-English messages ("Add Nairobi rainfall plot"), never "update".
- Push with `git push` when the participant asks. Never force-push, never reset --hard, never rewrite history.
- Commit code and small text only. NEVER commit `out/`, `.venv/`, data files, `.env`, or anything large.
- NEVER read, print, ask for, or write credentials: no tokens, no API keys, nothing under `~/.config/gh`, `~/.ssh`,
  `~/.claude`, and no `.env*` files. If a step seems to need a secret, stop and tell the participant to do it
  themselves in their own terminal. Do not run `env` or `printenv`.

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
- Reference scripts that run: `exercises/01_open_virtual_store.py`, `02_read_realized.py`, `03_pan_vs_pencil.py`,
  `04_cmorph_return_periods.py`, `05_xclim_heavy_rain.py`, `06_forecast_vs_local_extremes.py`,
  `07_review_before_push.py`, `08_exceedance_probability_map.py`.
- Run `exercises/07_review_before_push.py` before every `git push`; do not push if it reports a problem.

## Chunking (pan vs pencil)
- Both remote stores use "pan" chunks: one whole map per chunk. A map is 1 fetch; a point time series is one fetch
  per time or lead time. To explain a slow read, count the chunks it touches (`da.encoding["chunks"]`).
- "Pencil" chunks hold the whole time axis for a small patch: one fetch per point series, thousands per map.
- To compare layouts, rechunk a SMALL local copy (`.chunk(...)` then `.to_zarr("out/...")`); never rechunk a remote store.

## Plots
- Use matplotlib, save to `out/` as PNG, one small slice at a time. `pcolormesh` for gridded fields.
