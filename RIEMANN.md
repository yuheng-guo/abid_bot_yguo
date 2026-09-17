# Running this abid_bot on riemann

This branch was written for Anvil (SLURM + Lmod). riemann has neither: there is
no batch scheduler, no compute nodes, and no `module` command, so images are
rendered directly on the login machine. These are the changes that were made.

## Environment

| Anvil | riemann |
|---|---|
| `module load visit/3.1.4` | VisIt **3.3.3** at `/data/shared/visit/bin` (on `$PATH` via `params`) |
| `module load python` / `bwpy` | system `python3` (3.12, with numpy + h5py) |
| `module load hdf5/1.10.7` | system `h5ls` / `h5dump` |
| `sbatch` + `multirun_template_anvil` | run locally, `$maxParallel` at a time, via `bin/scheduler/multirun_template_riemann` |

`maxParallel` is set in `params` (default 16). riemann has 160 cores but is
shared, so don't raise it much.

## Files changed

- `params` — `root`, `export root`, `h5src`, `maxParallel`, VisIt on `$PATH`,
  no `module load`. The original is kept as `params.anvil.bak`.
- `setup.sh`, `bin/bw_many_folder_scripts/cray.sh`,
  `bin/bw_many_folder_scripts/SetMovie.sh` — `module load` removed.
- `runLocal.sh`, `orunLocal.sh`, `runMulti.sh`, `bin/filmBundled.sh` —
  `-forceversion 3.1.4` -> `3.3.3`; `sbatch` replaced with local execution.
- `bin/bw_many_folder_scripts/cray.sh` — `examplefilename` is now
  `rho_b.file_0.h5`. Most data folders are rho_b-only, so `Bx.file_0.h5` does
  not exist in them. (`movieSeq_v2_arg.bash` actually picks the first `*.h5` it
  finds, so this is cosmetic, but it was misleading.)
- `bin/bw_many_folder_scripts/runModule.py`
  - `PlotBox()` no longer hardcodes `/anvil/scratch/x-yguo11/...`; it reads
    `$root` from the environment.
  - `PlotBH()` no longer calls `AddOperator("Delaunay")`. **VisIt 3.3.3 ships
    the Delaunay operator disabled** ("Skipping disabled operator plugin
    Delaunay version 1.0" in the viewer log) and `visit -cli` has no API to
    enable it -- the call raises `Invalid operator plugin name`. The horizon
    renders correctly without it. This matches the other working riemann
    install, `/data/wiwang3/abid_bot_disk_bhdisk_B3`.
- `runLocal.sh`, `orunLocal.sh` — each run now writes to its own
  `movies/<DATE>_<jobName>/` subdirectory, the same way `runMulti.sh` and
  `bin/filmBundled.sh` already did, so repeat runs no longer overwrite each
  other. (Uncomment the line below it to go back to a bare `<jobName>`.)
- `bin/link_h5data.sh` — new, see below.

## Data layout

The multi-TB simulation output is too big to copy into the abid_bot tree, so it
stays where it is and is symlinked in -- the same convention the other abid_bot
installs on riemann use. `params` points at it:

    h5src="/data/yuhengguo/bhdisk_sol_05/hdf5/h5_extracted"

`bin/link_h5data.sh` does three things:

1. moves any `sol32_may_hdf5/` folders up into `$h5src` (a sol_32-only
   rescue step; inert here),
2. renames every raw `YY_MM_DD_HHMMSS` folder to `3d_data_YY_MM_DD_HHMMSS`,
3. symlinks those into `h5data/`, together with the diagnostics files and
   `horizon/` from `$h5src/data` (bhns.xon, bhns.mon, bhns_BHspin.mon,
   bhns-particles.mon, ...).

It is safe to re-run.

## Usage

    . params
    . bin/link_h5data.sh     # only needed when the data on disk changes
    . setup.sh               # builds xml/, bhdata/, cm.txt, spin vtks
    . runLocal.sh            # one frame  (edit foldernum / ranknum first)
    . runMulti.sh            # many frames, $maxParallel at a time

Note `setup.sh` moves empty `3d_data_*` folders into `h5data/bad_data/`, and
`rmdupes.py` moves duplicated time ranges there too, so the folder count after
setup is lower than the number of links.
