"""Exercise 4: explore 27 years of observed rainfall extremes (CMORPH, 1998-2024) for East Africa.

The store holds annual maxima and Gumbel return-period depths that were computed from a pencil-chunked
copy of 236,688 CMORPH files (all 27 years at each grid point in one chunk). This store itself is
pan-chunked (one map per chunk), so maps are cheap and a 27-year point series costs 27 fetches.

Run:  uv run python exercises/04_cmorph_return_periods.py
"""
import os
import pathlib
import time

# Stray AWS_* variables silently redirect the open; the store is public, so drop them first.
for k in [k for k in os.environ if k.startswith("AWS_")]:
    os.environ.pop(k)

import icechunk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

ENDPOINT = "https://data.source.coop"
BUCKET = "e4drr-project"
PREFIX = "observations/cmorph_rp_icechunk"
DURATION = "24hr"
RETURN_PERIOD = 10                       # years
LAT, LON = -1.29, 36.82                  # Nairobi
out = pathlib.Path("out")
out.mkdir(exist_ok=True)

storage = icechunk.s3_storage(
    bucket=BUCKET, prefix=PREFIX, endpoint_url=ENDPOINT, region="us-east-1",
    anonymous=True, from_env=False, force_path_style=True)
repo = icechunk.Repository.open(storage, config=icechunk.RepositoryConfig.default())
ds = xr.open_zarr(repo.readonly_session("main").store, zarr_format=3, consolidated=False, chunks={})

print("dims:", dict(ds.sizes))
print("variables:", list(ds.data_vars))
print("durations:", ds.duration.values.tolist(), "| return periods:", ds.return_period.values.tolist())
print(f"latitude runs {float(ds.lat[0]):.1f} -> {float(ds.lat[-1]):.1f} (ASCENDING here, unlike the forecast store)")
for v in ds.data_vars:
    print(f"  {v}: chunks {ds[v].encoding['chunks']}")

# Map read: one duration -> one chunk.
t0 = time.time()
rp_map = ds["return_period_precip"].sel(duration=DURATION, return_period=RETURN_PERIOD).compute()
print(f"map read ({DURATION}, {RETURN_PERIOD}-yr): {time.time() - t0:.1f}s, 1 chunk")

# Point series read: one duration, every year -> one chunk per year.
t0 = time.time()
amax = ds["annual_maxima"].sel(duration=DURATION).sel(lat=LAT, lon=LON, method="nearest").compute()
rp_point = ds["return_period_precip"].sel(duration=DURATION).sel(lat=LAT, lon=LON, method="nearest").compute()
print(f"series read (27 annual maxima at Nairobi): {time.time() - t0:.1f}s, {ds.sizes['year']} chunks")

vals = amax.values
assert np.isfinite(vals).all(), "NaN in annual maxima: check the point is inside the domain"
print(f"Nairobi {DURATION} annual max: median {np.median(vals):.0f} mm, wettest {vals.max():.0f} mm "
      f"in {int(amax.year[vals.argmax()])}")
print("return levels (mm):", dict(zip(rp_point.return_period.values.tolist(), np.round(rp_point.values, 1).tolist())))

# Sanity check: the empirical exceedance of the 27 maxima should sit near the fitted Gumbel curve.
sorted_vals = np.sort(vals)[::-1]
empirical_T = (len(vals) + 1) / np.arange(1, len(vals) + 1)        # Weibull plotting position

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), gridspec_kw=dict(width_ratios=[1, 1.15, 1]))
ax = axes[0]
pm = ax.pcolormesh(rp_map.lon, rp_map.lat, rp_map, cmap="YlGnBu", shading="auto",
                   vmax=float(rp_map.quantile(0.99)))
fig.colorbar(pm, ax=ax, label="mm")
ax.plot(LON, LAT, "r^", ms=8, label="Nairobi")
ax.set(title=f"{RETURN_PERIOD}-year {DURATION} rainfall (Gumbel)", xlabel="lon", ylabel="lat")
ax.set_aspect("equal")
ax.legend(loc="lower left")

ax = axes[1]
ax.bar(amax.year, vals, color="steelblue")
for T, c in [(2, "grey"), (10, "darkorange"), (50, "crimson")]:
    ax.axhline(float(rp_point.sel(return_period=T)), color=c, ls="--", lw=1.5, label=f"{T}-yr level")
ax.set(title=f"Nairobi: annual max {DURATION} rainfall, 1998-2024", xlabel="year", ylabel="mm")
ax.legend()
ax.grid(axis="y", alpha=0.3)

ax = axes[2]
ax.semilogx(rp_point.return_period, rp_point, "o-", color="crimson", label="Gumbel fit")
ax.semilogx(empirical_T, sorted_vals, "k.", label="observed annual maxima")
ax.set(title="Does the fit match the data?", xlabel="return period (years)", ylabel=f"{DURATION} rainfall (mm)")
ax.legend()
ax.grid(alpha=0.3, which="both")
fig.suptitle("CMORPH 1998-2024, East Africa: observed rainfall extremes")
fig.tight_layout()
fig.savefig(out / "04_cmorph_return_periods.png", dpi=120)
print("saved", out / "04_cmorph_return_periods.png")
