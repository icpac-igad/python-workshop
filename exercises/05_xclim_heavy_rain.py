"""Exercise 5: turn the cumulative forecast into daily rainfall and count heavy-rain days with xclim.

Run:  uv run python exercises/05_xclim_heavy_rain.py
"""
import os

for k in [k for k in os.environ if k.startswith("AWS_")]:
    os.environ.pop(k)

import importlib.util
import pathlib
import sys

import numpy as np
import pandas as pd
import xarray as xr
import xclim

sys.path.insert(0, str(pathlib.Path(__file__).parent))
spec = importlib.util.spec_from_file_location("ex2", pathlib.Path(__file__).parent / "02_read_realized.py")
src = open(spec.origin).read().split("t0 = time.time()")[0]     # reuse open_sub() without re-running the plot
ns = {}
exec(src, ns)

ds = ns["open_sub"]("49r1-jja2025")
TIME_IDX, LAT, LON = 45, ns["LAT"], ns["LON"]
THRESH_MM = 10          # "heavy" daily rainfall for this exercise (a teaching value, not an operational threshold)

init = pd.Timestamp(ds.time.values[TIME_IDX])
lead_h = (pd.to_timedelta(ds.step.values) / pd.Timedelta("1h")).astype(int)
day_idx = [i for i, h in enumerate(lead_h) if h % 24 == 0 and h > 0]     # whole-day lead times only

# Select the steps BEFORE computing: 10 chunks are fetched instead of 65.
# tp is cumulative from forecast start (m): convert to mm, then difference to get 24 h totals.
cum = (ds["tp"].isel(time=TIME_IDX, step=day_idx).sel(latitude=LAT, longitude=LON, method="nearest")
       .compute() * 1000.0).transpose("number", "step")
daily = cum.diff("step", label="upper")
daily = xr.concat([cum.isel(step=slice(0, 1)), daily], dim="step")

valid = init + pd.to_timedelta(lead_h[day_idx], unit="h")
pr = xr.DataArray(daily.values, dims=("number", "time"), coords={"number": daily.number.values, "time": valid},
                  attrs={"units": "mm/day", "standard_name": "precipitation_flux"}, name="pr")

heavy_days = xclim.indices.wetdays(pr, thresh=f"{THRESH_MM} mm/day", freq="YS")    # per member
wettest = xclim.indices.max_1day_precipitation_amount(pr, freq="YS")
n = pr.sizes["number"]
print(f"init {init:%Y-%m-%d}, {n} members, {pr.sizes['time']} days, point {LAT},{LON}")
print(f"members with at least one day >= {THRESH_MM} mm: {int((heavy_days.squeeze() >= 1).sum())} of {n} "
      f"({float((heavy_days.squeeze() >= 1).mean()):.0%})")
print(f"wettest single day, ensemble mean {float(wettest.mean()):.1f} mm, max member {float(wettest.max()):.1f} mm")
