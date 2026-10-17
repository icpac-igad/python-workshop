"""Exercise 2: read a realized Icechunk store (anonymous) and plot one ensemble forecast.

Run:  uv run python exercises/02_read_realized.py
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
import pandas as pd
import xarray as xr

ENDPOINT = "https://data.source.coop"
BUCKET = "e4drr-project"
BASE = "forecasts/ecmwf-ifs-ea-swio-realized-v3"
SUB = "49r1-jja2025"                     # one season sub-store
LAT, LON = -1.29, 36.82                  # Nairobi


def open_sub(sub):
    storage = icechunk.s3_storage(
        bucket=BUCKET, prefix=f"{BASE}/{sub}", endpoint_url=ENDPOINT, region="us-east-1",
        anonymous=True, from_env=False, force_path_style=True)
    cfg = icechunk.RepositoryConfig.default()
    cfg.manifest = icechunk.ManifestConfig(
        preload=icechunk.ManifestPreloadConfig(max_total_refs=0, max_arrays_to_scan=0))
    repo = icechunk.Repository.open(storage, config=cfg)
    session = repo.readonly_session("main")
    ds = xr.open_zarr(session.store, zarr_format=3, consolidated=False,
                      chunks={}, decode_timedelta=True)          # lazy: nothing is downloaded yet
    return ds


t0 = time.time()
ds = open_sub(SUB)
print(f"opened {SUB} in {time.time() - t0:.1f}s")
print("dims:", dict(ds.sizes), "| channels:", len(ds.data_vars))

# Select time first (one chunk = all 51 members for one date+step), then the point.
t1 = time.time()
tp = (ds["tp"].isel(time=45).sel(latitude=LAT, longitude=LON, method="nearest").compute()) * 1000.0  # m -> mm
print(f"pulled {tp.shape} (members x steps) in {time.time() - t1:.1f}s")

lead = (pd.to_timedelta(ds.step.values) / pd.Timedelta("1h")).astype(int)
fig, ax = plt.subplots(figsize=(9, 4.5))
for m in range(tp.sizes["number"]):
    ax.plot(lead, tp.isel(number=m), color="steelblue", alpha=0.18, lw=0.8)
ax.plot(lead, tp.isel(number=0), color="black", lw=2, label="control")
ax.plot(lead, tp.mean("number"), color="crimson", lw=2, label="ensemble mean")
ax.set(xlabel="lead time (h)", ylabel="cumulative precipitation (mm)",
       title=f"ECMWF IFS ensemble tp at Nairobi, init {str(ds.time.values[45])[:10]}")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
out = pathlib.Path("out"); out.mkdir(exist_ok=True)
fig.savefig(out / "02_nairobi_tp.png", dpi=120)
print("saved", out / "02_nairobi_tp.png")
