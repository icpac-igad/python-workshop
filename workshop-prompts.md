# Workshop prompts: one step after another, on a small budget

*African Summer School on Artificial Intelligence for Weather and Climate Modelling 2026 · Day 2, 20 October 2026*

Your OpenRouter key carries a **small workshop credit**. The steps below fit inside it with plenty to spare, *if*
you follow the six habits. Steps marked **(no agent)** cost nothing: you type them in your own terminal.

Replace `<town>`, `<lat>`, `<lon>` with your own (the examples use Kisumu, -0.09, 34.77).

## The six habits that keep the cost low

1. **One exercise, one conversation.** Type `/clear` before every new step. Every message re-sends the whole
   conversation, so a long chat gets more expensive with every turn.
2. **Name the file.** "Read `~/python-workshop/exercises/04_...py`" is cheap. "Look around the repository" makes the
   agent open everything.
3. **Ask for short answers.** End with "in 3 lines" or "only the numbers".
4. **Never let the agent read notebooks or images.** A run notebook or a PNG holds large encoded outputs. Look at
   the plot yourself and describe it in one sentence. (The project rules forbid both.)
5. **Run the example before asking about it.** The output answers most questions for free.
6. **Do git yourself when you can.** `git status`, `git log`, `git switch`, `git revert` and `git tag` cost nothing in
   your own terminal. Use the agent for the parts that need thought: the code and the commit message.

In the agent, `/status` shows the model (it must be `qwen/qwen3-coder-next`).

---

## Step 0 · Environment (no agent)

From the welcome email: JupyterHub account, Claude Code, Ori and `~/.env`. Then:

```bash
cd ~
git clone -b 2026-10 --single-branch https://github.com/icpac-igad/python-workshop.git
~/python-workshop/setup-nosudo.sh --skip-env          # uv and gh, no sudo
```

Then follow [GITHUB_SETUP.md](GITHUB_SETUP.md): your empty repository `ai-summer-school-2026`, a fine-grained token,
`gh auth login`, clone, copy the rules and environment files, `uv sync --extra virtual`, first commit and push.

Start the agent **from your own repository**:

```bash
cd ~/ai-summer-school-2026
set -a; source ~/.env; set +a
ori claude --model qwen/qwen3-coder-next --add-dir ~/python-workshop
```

## Step 1 · E0 Orientation

> Read CLAUDE.md. List the files in ~/python-workshop/exercises with the first docstring line of each. Then, in 5
> bullets: what is here, and what you must never do.

Check: the agent names the read-only rule and the secret rules. `/clear`

## Step 2 · E0 First commit by the agent

> Create NOTES.md with my name `<name>` and home town `<town>` (`<lat>`, `<lon>`). Show the diff, commit with a
> detailed message (title, Why, Result, Checked), and push.

Check: open your repository on GitHub and read the message. `/clear`

## Step 3 · E1 Load a 2 PB virtual store

> Run ~/python-workshop/exercises/01_open_virtual_store.py. In 3 lines: what was downloaded, what was not, and why.

Check: the mean value is plausible for the region. `/clear`

## Step 4 · E2 Inspect: the rainfall plume at your town

> Read ~/python-workshop/exercises/02_read_realized.py. Write scripts/e2_`<town>`_plume.py for `<town>` (`<lat>`,
> `<lon>`), with `# %%` cell markers, reading only daily lead times (0 to 240 h). Run it. In 3 lines: the dimensions, the latitude order, and the largest
> 10-day total. Then commit with a detailed message.

Check: the cumulative curves never go down, and the spread grows with lead time. Look at `out/` yourself. `/clear`

## Step 5 · E3 Explore: pan vs pencil chunks

First fill in the table on the slide with a neighbour (no agent). Then:

> Run ~/python-workshop/exercises/03_pan_vs_pencil.py. In 3 lines: how many chunks a map read and a point series
> touch in each layout, and which layout suits which read.

`/clear`

## Step 6 · E4 Visualise: observed extremes

> Read ~/python-workshop/exercises/04_cmorph_return_periods.py. Write scripts/e4_`<town>`_extremes.py for `<town>`,
> with `# %%` cell markers. Run it. Give only the 2-, 10- and 50-year 24 h levels and the wettest year. Commit with
> a detailed message.

Check: latitude **ascends** in this store, unlike E2. `/clear`

## Step 7 · E5 Analyse: heavy-rain days

> Read ~/python-workshop/exercises/05_xclim_heavy_rain.py. Write scripts/e5_`<town>`_heavy_days.py with a threshold
> of `<N>` mm/day, with `# %%` cell markers. Run it. Give only the number of members with a heavy-rain day. Commit
> with a detailed message.

Check: the daily totals are differences of cumulative `tp`. `/clear`

## Step 8 · E6 Forecast vs local extremes

> Read ~/python-workshop/exercises/06_forecast_vs_local_extremes.py. Write scripts/e6_`<town>`_exceedance.py for
> `<town>`, with `# %%` cell markers. Run it. Give the threshold, the members above it per day, and the assumptions
> you changed, in at most 5 lines. Commit with a detailed message.

Check: is the town inside both domains? Are the units both mm in 24 h? `/clear`

## Step 9 · E7 Review and publish

> Run git status and ~/python-workshop/exercises/07_review_before_push.py. If it reports no problem, push. Answer in
> 3 lines.

Check: your repository on GitHub shows `scripts/`, `NOTES.md` and no `out/`, data or keys. `/clear`

---

## Exploring further, almost free

### Step 10 · Explore a script as a notebook (no agent)

Your scripts have `# %%` cell markers, so jupytext turns them into notebooks without the agent:

```bash
cd ~/ai-summer-school-2026
uv run python -m ipykernel install --user --name ai-school-2026 --display-name "AI school 2026"   # once
uv run jupytext --set-formats ipynb,py:percent scripts/e6_<town>_exceedance.py
```

1. In JupyterLab, open `scripts/e6_<town>_exceedance.ipynb` and pick the kernel **AI school 2026**.
2. Run the cells one by one. Change a value, then run again. Explore by hand.
3. Copy your notebook changes back into the script:
   `uv run jupytext --sync scripts/e6_<town>_exceedance.ipynb`.
4. Look at `git diff`. It shows a readable script diff, not notebook JSON.
5. Commit the `.py`. The `.ipynb` is ignored on purpose: its outputs would bloat your history.

### Step 11 · A branch for a "what if" (no agent, or one small prompt)

```bash
git switch -c try-threshold-10mm
```

> In scripts/e5_`<town>`_heavy_days.py change the threshold to 10 mm/day, run it, and give only the new number.
> Commit with a detailed message.

```bash
git diff main --stat                # what the experiment changed
git switch main                     # back to the original
git merge try-threshold-10mm        # keep it ...   or:   git branch -D try-threshold-10mm   to drop it
```

### Step 12 · Undo a mistake with `git revert` (no agent)

1. Edit a script so that it forgets the `* 1000` (metres to mm). Run it, see the absurd result, and commit it.
2. Then:

```bash
git log --oneline -3
git revert HEAD                     # a new commit that undoes the last one: history keeps both
```

Revert keeps the mistake and its correction in the record, unlike deleting.

### Step 13 · Tag your result (no agent)

```bash
git tag -a e6-<town> -m "E6 result for <town>: threshold and exceedance counts"
git push --tags
```

On GitHub, *Tags* now lists a citable version of your work.

### Step 14 · E8 stretch (take-home, after the session)

> Read ~/python-workshop/exercises/08_exceedance_probability_map.py. Write scripts/e8_`<region>`_probability.py for
> `<box or start date>`, with `# %%` cell markers. Run it. Give only the maximum probability per day. Commit with a
> detailed message.

---

## What it costs

Measured on 20 October 2026 by running the prompts above, each in a fresh conversation, for Kisumu. Figures are a
share of your credit. Where two steps share a row, the cost of the first showed up together with the second.

| Step | `qwen/qwen3-coder-next` | Agent turns |
|---|---|---|
| 1-2 E0 orientation, first commit | about 1% | 3 + 5 |
| 3 E1 virtual store | under 1% | 2 |
| 4 E2 plume | about 3% | 22 (slow data read, about 9 min) |
| 5-6 E3 chunks, E4 extremes | about 4% | 2 + 14 |
| 7 E5 heavy days | about 1% | 9 |
| 8 E6 exceedance | about 2% | 7 |
| 9 E7 review and push, 14 E8 stretch | about 1% | 5 + 6 |
| **Whole workshop (steps 1-9 and 14)** | **about 12%** | |

With `deepseek/deepseek-v4-pro`, steps 1-4 alone used about 80% of the credit, mostly because its requests are
spread over many providers and so are rarely cached. Use Qwen3 Coder Next unless the instructor says otherwise.
