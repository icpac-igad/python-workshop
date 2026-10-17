"""Exercise 6: compare the ensemble forecast at one town with that town's observed extremes.

Threshold = the CMORPH 2-year, 24 h rainfall level at the town (exercise 4). For each forecast day we count how
many of the 51 members exceed it (daily totals from exercise 5). Change TOWN, LAT, LON to your own town.

Run:  uv run python exercises/06_forecast_vs_local_extremes.py
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
TOWN, LAT, LON = "Nairobi", -1.29, 36.82
TIME_INDEX = 45                          # forecast start 2025-07-16
RETURN_PERIOD = 2                        # years: a level reached about every other year
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

# 1. Is the town inside both domains? Nearest-point selection never fails, so check it ourselves.
for name, la, lo in [("CMORPH", obs.lat, obs.lon), ("forecast", fc.latitude, fc.longitude)]:
    inside = float(la.min()) <= LAT <= float(la.max()) and float(lo.min()) <= LON <= float(lo.max())
    assert inside, f"{TOWN} ({LAT}, {LON}) is outside the {name} domain"

# 2. Threshold from 27 years of observations (CMORPH latitude ASCENDS). 9 small fetches, one per duration chunk.
thr = (obs["return_period_precip"].sel(duration="24hr", return_period=RETURN_PERIOD)
       .sel(lat=LAT, lon=LON, method="nearest").compute())
thr_mm = float(thr)
assert np.isfinite(thr_mm), "threshold is NaN: is the town over the sea or outside CMORPH?"
print(f"{TOWN}: CMORPH {RETURN_PERIOD}-year 24 h level = {thr_mm:.1f} mm "
      f"(grid point {float(thr.lat):.2f}, {float(thr.lon):.2f})")

# 3. Forecast daily totals. Select the date and whole-day lead times FIRST: 11 fetches instead of 65.
init = pd.Timestamp(fc.time.values[TIME_INDEX])
lead_h = (pd.to_timedelta(fc.step.values) / pd.Timedelta("1h")).astype(int)
day_idx = [i for i, h in enumerate(lead_h) if h % 24 == 0]                  # 0, 24, ..., 240 h
cum = (fc["tp"].isel(time=TIME_INDEX, step=day_idx).sel(latitude=LAT, longitude=LON, method="nearest")
       .compute() * 1000.0)                                                 # cumulative m -> mm
assert np.isfinite(cum.values).all(), f"NaN for {init:%Y-%m-%d}: that date was never written"
daily = cum.diff("step").transpose("number", "step")                        # mm in the 24 h ending at the step
days = lead_h[day_idx][1:] // 24
valid = [init + pd.Timedelta(days=int(d)) for d in days]
print(f"forecast grid point {float(cum.latitude):.2f}, {float(cum.longitude):.2f}, init {init:%Y-%m-%d}")

# 4. How many members exceed the observed 2-year level on each day?
n_members = daily.sizes["number"]
exceed = (daily > thr_mm).sum("number").values
for d, v, e, wettest in zip(days, valid, exceed, daily.max("number").values):
    print(f"  day {d:2d} ({v:%d %b}): {e:2d} of {n_members} members above {thr_mm:.0f} mm, wettest member {wettest:.1f} mm")

fig, axes = plt.subplots(1, 2, figsize=(14, 4.6))
ax = axes[0]
for m in range(n_members):
    ax.plot(days, daily.isel(number=m), color="steelblue", alpha=0.2, lw=0.8)
ax.plot(days, daily.mean("number"), color="black", lw=2, label="ensemble mean")
ax.axhline(thr_mm, color="crimson", ls="--", lw=1.5, label=f"CMORPH {RETURN_PERIOD}-year 24 h level")
ax.set(title=f"{TOWN}: daily rainfall, 51 members", xlabel="forecast day", ylabel="mm in 24 h")
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1]
ax.bar(days, exceed, color="crimson")
ax.set(title=f"Members above the local {RETURN_PERIOD}-year level", xlabel="forecast day",
       ylabel=f"members (of {n_members})", ylim=(0, n_members))
ax.set_xticks(days, [f"{d}\n{v:%d %b}" for d, v in zip(days, valid)], fontsize=8)
ax.grid(axis="y", alpha=0.3)
fig.suptitle(f"ECMWF IFS ensemble from {init:%Y-%m-%d} vs CMORPH 1998-2024 extremes at {TOWN}")
fig.tight_layout()
png = out / f"06_{TOWN.lower()}_exceedance.png"
fig.savefig(png, dpi=120)
print("saved", png)
