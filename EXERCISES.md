# Exercises E0-E8: the prompts from the slides

*African Summer School on Artificial Intelligence for Weather and Climate Modelling 2026 · Day 2, 20 October 2026*

These are the prompts shown on the session slides, one exercise after another, with what to look for and what to
check before you commit. Copy a prompt into the agent, replace the `<...>` parts with your own town, name or
question, and read the answer before you accept it.

- Start the agent from **your own repository** (README step 7):

  ```bash
  cd ~/ai-summer-school-2026
  set -a; source ~/.env; set +a
  ori claude --model qwen/qwen3-coder-next --add-dir ~/python-workshop
  ```

- Type `/clear` before every new exercise, and add *"in 3 lines"* or *"only the numbers"* to keep the answers
  short. Shorter, budget-tested versions of the same prompts are in [workshop-prompts.md](workshop-prompts.md).
- The examples in `~/python-workshop/exercises/` are inspiration only: the agent reads and runs them, but writes
  **your** scripts in `scripts/` of your repository.
- Never paste a key or token into the agent's chat.

| | Exercise | Example script |
|---|---|---|
| E0 | Your repository, a token, and orientation | (setup) |
| E1 | Load: open a 2 PB virtual store | `01_open_virtual_store.py` |
| E2 | Inspect: a realized store and the rainfall plume | `02_read_realized.py` |
| E3 | Explore: pan vs pencil chunks | `03_pan_vs_pencil.py` |
| E4 | Visualise observed extremes (CMORPH 1998-2024) | `04_cmorph_return_periods.py` |
| E5 | Count heavy-rain days with xclim | `05_xclim_heavy_rain.py` |
| E6 | Compare the forecast with local observed extremes | `06_forecast_vs_local_extremes.py` |
| E7 | Review and publish | `07_review_before_push.py` |
| E8 | Stretch (take-home): exceedance probability map | `08_exceedance_probability_map.py` |

---

## E0 · A repository and a token on GitHub (10 min)

**In the browser** (step by step in [GITHUB_SETUP.md](GITHUB_SETUP.md)):

1. *Settings → Emails*: keep the email address private; copy the noreply address.
2. *New repository*: `ai-summer-school-2026`, empty (no README).
3. *Settings → Developer settings → Fine-grained tokens*:
   - Only select repositories: `ai-summer-school-2026`
   - Contents: Read and write; everything else: No access
   - Expires 31 October 2026

The token is pasted once, at a hidden prompt in your own terminal. Never into the agent's chat, a script or a commit.

**In the terminal** (outside the agent):

```bash
cd ~
git clone -b 2026-10 https://github.com/icpac-igad/python-workshop.git
~/python-workshop/setup-nosudo.sh --skip-env       # uv, gh, claude
gh auth login       # "Paste an authentication token" (hidden)
gh auth setup-git
git clone https://github.com/<you>/ai-summer-school-2026.git && cd ai-summer-school-2026
cp ~/python-workshop/{CLAUDE.md,pyproject.toml,uv.lock,.gitignore} .
mkdir -p .claude && cp ~/python-workshop/.claude/settings.json .claude/
uv sync --extra virtual
git add -A && git commit -m "Start my workshop repository" && git push -u origin main
set -a; source ~/.env; set +a                      # key and model, from the email
ori claude --model qwen/qwen3-coder-next --add-dir ~/python-workshop
```

Only the rules and environment files are copied, not the examples. The first push proves the token works.

### E0 · Orientation

> Read CLAUDE.md and the examples in ~/python-workshop/exercises/. Tell me in 5 bullets what is there and what you
> must never do. Then explain git remote -v and gh auth status, without showing any token.

**Check**
- The bullets mention both data stores.
- Code runs with `uv run`.
- `origin` is your own repository.
- No secrets, ever.

**Commit**
- `NOTES.md` with your name and home town (with its latitude and longitude).
- A detailed message, then push.

---

## E1 · Load: open a 2 PB virtual store (10 min)

> Run example 01_open_virtual_store.py and explain what was and was not downloaded. Then write my own
> scripts/e1_`<name>`.py that reads `<variable>` for `<date>`.

**Look for**
- The store opens in about 2.5 s.
- 12 groups: 0p4, 49r1 and 50r1, each for four forecast cycles.
- One `t2m` field of shape (321, 261).

The virtual store holds references to about 1.9 PB of GRIB files; the references themselves are about 76 GB.

### E1 · Check and commit

- The mean is about 22 °C. Is that plausible for the region?
- Only references and one field were fetched, not 2 PB.
- Reference time plus lead time gives valid time.

> Show the diff, then commit with a title and a body: why, the result and how we checked it. Push.

---

## E2 · Inspect: a realized store (15 min)

> Run example 02_read_realized.py. Give me the dimensions, the 38 channels and the latitude order without printing
> the whole dataset. Then write scripts/e2_`<town>`_plume.py for my town.

Tip: ask for **daily lead times only (0 to 240 h)** in your own script. Reading all 65 lead times at one point is
slow (E3 explains why).

**Look for**
- `time 92, step 65, number 51, latitude 321, longitude 261`
- 38 channels: `tp`, `t2m`, `msl`, winds, humidity and more.
- A plot in `out/` (the example writes `out/02_nairobi_tp.png`).

### E2 · What the plume shows (debrief)

The "plume" is the 51-member rainfall plot: one line per ensemble member, at your town.

- Latitude descends: 40 → -40.
- `tp` is cumulative, so the curves never go down.
- The spread grows with lead time.
- The control run (black) is one member, not the truth.
- Start date 2025-07-16 is in the dry season, so a few mm is plausible.

Why was the point read slow? That is E3. Commit and push the work.

---

## E3 · Explore: pan vs pencil chunks (20 min)

Both remote stores in this session use **pan** chunks: one chunk holds one whole map. A pencil chunk is a column:
every time, a tiny patch. The layout decides how many chunks a read must fetch.

### E3 · Predict first (no agent)

How many chunks does each read touch? Discuss with a neighbour and complete the table. The box covers Ethiopia
and Kenya: 81 × 61 grid points, 11 daily lead times, 51 members.

| Read | Pan (1, 51, 81, 61) | Pencil (11, 51, 1, 1) |
|---|---|---|
| One map, one lead time | ? | ? |
| Nairobi, every lead time | ? | ? |

### E3 · Compare the two layouts

> Run example 03_pan_vs_pencil.py. Which layout is better for a map, and which for a time series? Count the chunks
> each read touches.

**What the script does**
1. Pulls the box once (about 35 s) and caches it in `out/03_box.nc`.
2. Saves it twice: once in pan chunks, once in pencil chunks.
3. Times a map read and a time-series read on each.

### E3 · Debrief: same data, very different costs

Fill in your table first, then compare. (Measured on a local disk, best of 3, 13 October 2026; from the cloud
each fetch takes about 0.7 to 3 s, so the gap grows.)

<details><summary>Show the answer</summary>

| Layout | Map read | Nairobi series read |
|---|---|---|
| Pan (1, 51, 81, 61) | **1 chunk**, about 6 ms | 11 chunks, about 16 ms |
| Pencil (11, 51, 1, 1) | 4,941 chunks, about 6.6 s | **1 chunk**, about 5 ms |

Neither layout wins everywhere: choose it for the question you ask most often.
</details>

**Pencils at scale (how the E4 data was made):** 236,688 CMORPH NetCDF files on AWS S3 → an East Africa store in
pan chunks (48, 120, 110), 372 GB → rechunked to pencils (473376, 5, 5) in 7.9 min with 20 workers → a 27-year
series at one point reads in 0.5 s → return periods for every pixel. Whole pipeline: about $6 of cloud compute.

---

## E4 · Visualise observed extremes (15 min)

> Run example 04_cmorph_return_periods.py. Is the Gumbel fit good at Nairobi? Which year breaks it? Then write
> scripts/e4_`<town>`_extremes.py for my town.

**Look for**
- Dimensions: `duration 9, year 27, lat 550, lon 474`
- A map of the 10-year, 24 h rainfall.
- The 27 annual maxima at Nairobi, with the fitted return levels.

Latitude **ascends** in this store, unlike E2. Before running: will the map or the 27-year series be faster to read?

### E4 · Does the fit match the data? (debrief)

- Nairobi, 24 h: median annual maximum 79 mm; 2-year level 88.5 mm; 10-year level 167 mm.
- 1998 (El Niño): **285 mm**, above the fitted 100-year level of 266 mm.
- Discuss: are 27 years enough for a 100-year level? Is satellite rainfall comparable to a rain gauge?

Commit.

---

## E5 · Count heavy-rain days with xclim (10 min)

> Run example 05_xclim_heavy_rain.py. In plain words, what does wetdays count? Then write
> scripts/e5_`<town>`_heavy_days.py with my own threshold.

**Look for**
- How many of the 51 members have a day of at least 10 mm at Nairobi.
- The wettest day: ensemble mean and wettest member.

**Check and commit**
- Daily totals are differences of cumulative `tp`.
- July is the dry season at Nairobi, so low counts are expected.
- 10 mm is a teaching value, not an operational threshold.

---

## E6 · Compare the forecast with local observed extremes (15 min)

> Read example 06_forecast_vs_local_extremes.py. Write scripts/e6_`<town>`_exceedance.py for `<my town>`: use the
> CMORPH 2-year 24 h level there as the threshold, and plot how many members exceed it on each forecast day.

**Look for**
- A new plot in `out/`.
- A list of the assumptions the agent changed.

Example run, 2025-07-16 start: Nairobi 2-year level 88.5 mm, Kisumu 86.9 mm; 0 of 51 members exceed either on
days 1-10 (dry season).

### E6 · Check and commit

- The forecast grid is 0.25° (about 28 km); CMORPH is about 8 km. The nearest grid points do not cover the same area.
- Does the selected location lie within both domains?
- Is the threshold in the same units and accumulation period as the forecast (mm in 24 h)?

> Commit with a title and a body: why, the result, how we checked it and which example inspired it.

---

## E7 · Review and publish (5 min)

> Show me git status, the diff and git log. Run example 07_review_before_push.py. How can I tell this answer is
> right? Then push.

Example history:

```
$ git log --oneline
Add exceedance plot for Kisumu against the CMORPH 2-year level
Explore CMORPH return periods at Nairobi
Compare pan and pencil chunk read times
Read the realized store and plot the Nairobi plume
Open the virtual ECMWF store and read one t2m field
Add my notes
```

**Check**
- Values finite, units plausible.
- No `out/`, data or keys in any commit.
- Pushed to your own repository.
- The repository is visible on GitHub.

This repository is where the group project starts on Day 3.

---

## E8 · Stretch: where could the forecast exceed local extremes? (take-home)

> Read example 08_exceedance_probability_map.py. Write scripts/e8_`<region>`_probability.py for `<my box or start
> date>`.

**What it does**
- Each forecast grid point gets its own threshold: the CMORPH 2-year 24 h level at the nearest pixel.
- Probability = share of the 51 members above it, for forecast days 1-5.
- Pan chunks keep it cheap: 1 fetch for the threshold map, 1 per forecast day.

From 2025-07-16 over Ethiopia and Kenya the highest probability is 6 %. Is the 2-year level of the *annual
maximum* a fair threshold for a single forecast day?

---

## More to try

After E7, [workshop-prompts.md](workshop-prompts.md) has further tasks that cost almost nothing: explore a script
as a notebook with jupytext, a branch for a "what if", undo with `git revert`, tag your result, and measure your
work with `uvx pygount`.
