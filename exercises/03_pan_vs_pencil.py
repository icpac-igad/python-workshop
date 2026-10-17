"""Exercise 3: pan chunks vs pencil chunks. Same numbers, two layouts, very different read costs.

A "pan" chunk is a whole map for one time (good for maps). A "pencil" chunk is the whole time axis for
a tiny patch of grid (good for time series). We pull one small box from the remote store once, save it
locally in both layouts, then time a map read and a point-series read on each.

Run:  uv run python exercises/03_pan_vs_pencil.py
"""
import os
import pathlib
import shutil
import time

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
BASE = "forecasts/ecmwf-ifs-ea-swio-realized-v3"
SUB = "49r1-jja2025"
TIME_INDEX = 45                          # one forecast start date (2025-07-16)
BOX = dict(latitude=slice(15, -5), longitude=slice(30, 45))   # Ethiopia + Kenya; latitude DESCENDS
LAT, LON = -1.29, 36.82                  # Nairobi
MAP_STEP_H = 72                          # map of rain in the 24 h ending at +72 h
out = pathlib.Path("out")
out.mkdir(exist_ok=True)


def open_sub(sub):
    storage = icechunk.s3_storage(
        bucket=BUCKET, prefix=f"{BASE}/{sub}", endpoint_url=ENDPOINT, region="us-east-1",
        anonymous=True, from_env=False, force_path_style=True)
    repo = icechunk.Repository.open(storage, config=icechunk.RepositoryConfig.default())
    return xr.open_zarr(repo.readonly_session("main").store, zarr_format=3, consolidated=False,
                        chunks={}, decode_timedelta=True)


# 1. Remote store: what does one chunk hold?
ds = open_sub(SUB)
print("remote chunk shape for tp:", ds["tp"].encoding["chunks"], "(time, step, number, lat, lon)")
print("  -> one chunk = one whole map, all 51 members, for ONE date and ONE lead time: a 'pan' chunk")

# 2. Pull one box for one start date. Every lead time is a separate remote chunk, so select only the
#    daily lead times (0, 24, ..., 240 h = 11 fetches instead of 65). Cached so a rerun skips the download.
cache = out / "03_box.nc"
if cache.exists():
    tp = xr.open_dataarray(cache).load()
    print(f"using cached box {cache}")
else:
    daily = ds.step[(ds.step % np.timedelta64(24, "h")) == np.timedelta64(0, "h")]
    t0 = time.time()
    tp = (ds["tp"].isel(time=TIME_INDEX).sel(step=daily, **BOX) * 1000.0).compute()   # m -> mm, cumulative
    tp = tp.drop_vars("time").rename("tp")
    tp.attrs = {"units": "mm", "long_name": "cumulative total precipitation"}
    print(f"pulled box {dict(tp.sizes)} in {time.time() - t0:.1f}s ({daily.size} remote chunk fetches)")
    tp.to_netcdf(cache)

# 3. Save the same numbers twice, in two chunk layouts.
ny, nx = tp.sizes["latitude"], tp.sizes["longitude"]
layouts = {
    "pan":    {"step": 1, "number": 51, "latitude": ny, "longitude": nx},   # whole map per lead time
    "pencil": {"step": -1, "number": 51, "latitude": 1, "longitude": 1},    # whole time axis per grid point
}
for name, chunks in layouts.items():
    path = out / f"03_{name}.zarr"
    shutil.rmtree(path, ignore_errors=True)
    tp.chunk(chunks).to_dataset().to_zarr(path, mode="w", zarr_format=3, consolidated=False)


def n_chunks(name):
    c = xr.open_zarr(out / f"03_{name}.zarr", consolidated=False)["tp"].encoding["chunks"]
    return c, int(np.prod([-(-s // k) for s, k in zip(tp.shape, c)]))


def timed(fn, repeat=3):
    best = np.inf
    for _ in range(repeat):
        t = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t)
    return best


steps_h = (pd.to_timedelta(tp.step.values) / pd.Timedelta("1h")).astype(int)
results = []
for name in layouts:
    da = xr.open_zarr(out / f"03_{name}.zarr", consolidated=False)["tp"]
    shape, total = n_chunks(name)
    read_map = lambda: da.isel(step=int(np.where(steps_h == MAP_STEP_H)[0][0])).values
    read_series = lambda: da.sel(latitude=LAT, longitude=LON, method="nearest").values
    # chunks touched: a map needs every chunk that covers one step; a series every chunk on one point
    touched_map = total // -(-tp.sizes["step"] // shape[0])
    touched_series = -(-tp.sizes["step"] // shape[0])
    results.append(dict(layout=name, chunk_shape=shape, chunks_total=total,
                        map_chunks=touched_map, map_ms=1000 * timed(read_map),
                        series_chunks=touched_series, series_ms=1000 * timed(read_series)))

res = pd.DataFrame(results).set_index("layout")
print("\n", res.to_string(float_format=lambda v: f"{v:.1f}"))

# 4. Plot: the two reads we raced, and the race itself.
i72, i48 = (int(np.where(steps_h == h)[0][0]) for h in (MAP_STEP_H, MAP_STEP_H - 24))
daily_map = (tp.isel(step=i72) - tp.isel(step=i48)).mean("number")
point = tp.sel(latitude=LAT, longitude=LON, method="nearest")
point_daily = point.diff("step")

fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), gridspec_kw=dict(width_ratios=[1.05, 1.3, 1]))
ax = axes[0]
pm = ax.pcolormesh(daily_map.longitude, daily_map.latitude, daily_map, cmap="Blues", shading="auto")
fig.colorbar(pm, ax=ax, label="mm in 24 h (ensemble mean)")
ax.plot(LON, LAT, "r^", ms=8, label="Nairobi")
ax.set(title=f"MAP read: one lead time ({MAP_STEP_H - 24}-{MAP_STEP_H} h)", xlabel="lon", ylabel="lat")
ax.set_aspect("equal")
ax.legend(loc="lower left")

ax = axes[1]
for m in range(point.sizes["number"]):
    ax.plot(steps_h[1:], point_daily.isel(number=m), color="steelblue", alpha=0.18, lw=0.8)
ax.plot(steps_h[1:], point_daily.mean("number"), color="crimson", lw=2, label="ensemble mean")
ax.set(title="SERIES read: every lead time at Nairobi", xlabel="lead time (h)",
       ylabel="mm in the 24 h ending at lead time")
ax.grid(alpha=0.3)
ax.legend()

ax = axes[2]
x = np.arange(2)
w = 0.38
for j, (col, lab) in enumerate([("map_ms", "map read"), ("series_ms", "series read")]):
    bars = ax.bar(x + (j - 0.5) * w, res[col], w, label=lab)
    for b, nc in zip(bars, res[col.replace("_ms", "_chunks")]):
        ax.annotate(f"{nc} chunk{'s' if nc > 1 else ''}", (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom", fontsize=8)
ax.set_xticks(x, [f"{n}\n{s}" for n, s in zip(res.index, res.chunk_shape)], fontsize=8)
ax.set_yscale("log")
ax.set(ylabel="read time, local disk (ms, log scale)", title="Same data, two layouts")
ax.legend()
fig.suptitle(f"ECMWF IFS ensemble, init {str(ds.time.values[TIME_INDEX])[:10]}: pan vs pencil chunks")
fig.tight_layout()
fig.savefig(out / "03_pan_vs_pencil.png", dpi=120)
print("saved", out / "03_pan_vs_pencil.png")
