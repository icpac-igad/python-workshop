"""Exercise 1: open the virtual ECMWF store (2 PB of GRIB, only references are stored) and read ONE field.

Needs the optional GRIB codec:  uv sync --extra virtual
Run:  uv run python exercises/01_open_virtual_store.py
"""
import os

# The store is read anonymously, but stray AWS_* variables redirect the virtual-chunk client. Drop them first.
for k in [k for k in os.environ if k.startswith("AWS_")]:
    os.environ.pop(k)

import time

import gribberish.zarr  # noqa: F401  registers the GRIB codec for Zarr v3
import icechunk
import numpy as np
import xarray as xr
import zarr

storage = icechunk.s3_storage(
    bucket="e4drr-project", prefix="forecasts/ecmwf_ifs_ens_aws_s3_icechunk_vd",
    endpoint_url="https://data.source.coop", region="us-east-1",
    anonymous=True, from_env=False, force_path_style=True)
# Without this icechunk refuses to follow a virtual reference into a bucket you have not named.
auth = icechunk.containers_credentials({"s3://ecmwf-forecasts/": icechunk.s3_anonymous_credentials()})
cfg = icechunk.RepositoryConfig.default()
cfg.manifest = icechunk.ManifestConfig(preload=icechunk.ManifestPreloadConfig(max_total_refs=0, max_arrays_to_scan=0))
t0 = time.time()
repo = icechunk.Repository.open(storage, config=cfg, authorize_virtual_chunk_access=auth)
session = repo.readonly_session("main")
print(f"opened in {time.time() - t0:.1f}s (only references were fetched)")

root = zarr.open_group(session.store, mode="r")
for era in sorted(root.group_keys()):
    for run in sorted(root[era].group_keys()):
        g = root[era][run]
        print(f"{era}/{run}: {g['time'].shape[0]} dates, {g['step'].shape[0]} steps")

ds = xr.open_zarr(session.store, group="50r1/00z", consolidated=False, zarr_format=3,
                  decode_timedelta=True, chunks=None)
date = ds.time.values[-1]
field = (ds["t2m"].sel(time=date, number=0, step=np.timedelta64(0, "h"))
         .sel(latitude=slice(40, -40), longitude=slice(15, 80)))      # latitude DESCENDS
arr = np.asarray(field.values, dtype=np.float32)
print(f"t2m {str(date)[:10]} {arr.shape}: mean {np.nanmean(arr) - 273.15:.1f} degC")
