"""Exercise 8 (stretch): map the probability that daily rainfall exceeds the LOCAL observed 2-year level.

Exercise 6 did this at one town. Here every forecast grid point gets its own threshold: the CMORPH 2-year,
24 h level at the nearest CMORPH pixel. Probability = share of the 51 members above it, for each forecast day.
Both stores are pan-chunked, so maps are cheap: 1 fetch for the threshold map, 1 per forecast day.

Run:  uv run python exercises/08_exceedance_probability_map.py
"""
import os
import pathlib

# Stray AWS_* variables silently redirect the open; the store is public, so drop them first.
for k in [k for k in os.environ if k.startswith("AWS_")]:
    os.environ.pop(k)

import icechunk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

ENDPOINT = "https://data.source.coop"
BUCKET = "e4drr-project"
FORECAST = "forecasts/ecmwf-ifs-ea-swio-realized-v3/49r1-jja2025"
CMORPH = "observations/cmorph_rp_icechunk"
TIME_INDEX = 45                          # forecast start 2025-07-16
RETURN_PERIOD = 2
DAYS = [1, 2, 3, 4, 5]                   # forecast days to map
BOX = dict(latitude=slice(15, -5), longitude=slice(30, 45))   # Ethiopia + Kenya; forecast latitude DESCENDS
out = pathlib.Path("out")
out.mkdir(exist_ok=True)


def open_store(prefix):
    storage = icechunk.s3_storage(
        bucket=BUCKET, prefix=prefix, endpoint_url=ENDPOINT, region="us-east-1",
        anonymous=True, from_env=False, force_path_style=True)
    repo = icechunk.Repository.open(storage, config=icechunk.RepositoryConfig.default())
    return xr.open_zarr(repo.readonly_session("main").store, zarr_format=3, consolidated=False,
                        chunks={}, decode_timedelta=True)


obs = open_store(CMORPH)
fc = open_store(FORECAST)

# 1. Forecast: select date, the needed whole-day lead times and the box BEFORE computing.
init = pd.Timestamp(fc.time.values[TIME_INDEX])
steps = [np.timedelta64(24 * d, "h") for d in [DAYS[0] - 1, *DAYS]]
cum = fc["tp"].isel(time=TIME_INDEX).sel(step=steps, **BOX).compute() * 1000.0     # cumulative mm
assert np.isfinite(cum.values).all(), f"NaN for {init:%Y-%m-%d}: that date was never written"
daily = cum.diff("step")                                                             # mm per 24 h
print(f"forecast box {dict(daily.sizes)}, init {init:%Y-%m-%d}")

# 2. Threshold map: one CMORPH chunk, then the nearest CMORPH pixel for each forecast grid point.
#    CMORPH is ~8 km and its latitude ASCENDS; nearest-point matching is a teaching shortcut, not a regrid.
rp = obs["return_period_precip"].sel(duration="24hr", return_period=RETURN_PERIOD).compute()
thr = rp.sel(lat=daily.latitude, lon=daily.longitude, method="nearest").drop_vars(["lat", "lon"])
print(f"threshold map: {RETURN_PERIOD}-year 24 h level, {float(thr.min()):.0f} to {float(thr.max()):.0f} mm, "
      f"{int(np.isnan(thr).sum())} grid points without CMORPH data")

# 3. Probability = share of members above the local threshold (NaN where there is no threshold).
prob = (daily > thr).mean("number").where(np.isfinite(thr))
for d, p in zip(DAYS, prob):
    print(f"  day {d} ({init + pd.Timedelta(days=d):%d %b}): max probability {float(p.max()):.0%}, "
          f"{int((p >= 0.5).sum())} grid points at 50% or more")

vmax = max(0.1, float(prob.max()))         # small probabilities stay visible
fig, axes = plt.subplots(1, len(DAYS), figsize=(3.4 * len(DAYS), 4.6), sharey=True)
for ax, d, p in zip(axes, DAYS, prob):
    pm = ax.pcolormesh(p.longitude, p.latitude, p, cmap="Reds", vmin=0, vmax=vmax, shading="auto")
    ax.set(title=f"day {d} ({init + pd.Timedelta(days=d):%d %b})", xlabel="lon")
    ax.set_aspect("equal")
axes[0].set_ylabel("lat")
fig.colorbar(pm, ax=axes, shrink=0.8, label=f"share of 51 members above the local {RETURN_PERIOD}-year 24 h level")
fig.suptitle(f"ECMWF IFS ensemble from {init:%Y-%m-%d}: chance of exceeding the CMORPH {RETURN_PERIOD}-year level")
fig.savefig(out / "08_exceedance_probability.png", dpi=120, bbox_inches="tight")
print("saved", out / "08_exceedance_probability.png")
