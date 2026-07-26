# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **`abid_bot`** (remote: `Illinois-Relativity-Group/abid_bot`), a **VisIt-driven movie/visualization
pipeline** for GRMHD black-hole accretion-disk simulations (Einstein Toolkit / IllinoisGRMHD output). It
turns per-timestep HDF5 field data (`rho_b`, `P`, `vx/vy/vz`, `Bx/By/Bz`, metric, `smallb2`) plus
apparent-horizon and diagnostic ASCII files into rendered frames (volume / isosurface / vector / spin-vector
plots) and stitches them into movies. It runs on **Purdue Anvil** (SLURM) using **VisIt 3.1.4** in
`-cli -nowin` batch mode.

This is **not a buildable software project** — there is no compiler, package manager, or test suite. "Running"
means generating per-frame attribute files and invoking VisIt. Do not invent build/lint/test commands.

This checkout is a **flattened clone**: upstream nests the tool at `abid_bot_bhdisk/bhdisk_anvil/`, but here it
lives at the repo root. **Pull upstream changes with the subtree strategy**, not a plain `git pull` (see
`UPDATE.md`):

```bash
git pull -X subtree=abid_bot_bhdisk/bhdisk_anvil origin master
```

Local data/output (`h5data/`, `xml*/`, `movies/`, `log/`, `bhdata/`, all `.h5/.gp/.mon/.png/...`) is git-ignored
via `.git/info/exclude`, so it never interferes with merges.

## The core workflow

Everything is driven by one config file and a small set of orchestrator shell scripts. Three steps:

1. **Edit `params`** — the single source of truth, sourced by every script. It defines `root`, the output
   cadence `it` (iteration stride in the HDF5 data, e.g. 512), `dt`, `M` (ADM mass), `firstTime`/`offset`,
   `maxdensity` (density normalization for `logrho`), feature toggles (`fields`, `particleSeeds`,
   `spin_dimless`, `particleTracer`, `g00`, `updateGWdata`), and the **paths to the VisIt attribute XML
   templates** in `bin/bw_many_folder_scripts/atts/` (views, volume, pseudocolor/iso, vectors, spin vector).
   Multiple configs coexist as `params`, `params2`, … — scripts take an optional suffix arg `$1` and source
   `params$1`, falling back to `params`. `params` echoes a summary and auto-detects whether a BH/binary/merger
   horizon exists.

2. **Run `setup.sh [N]`** — preprocesses one config's data into a per-frame attribute tree under `xml[N]/`.
   It calls (in `bin/`): `clean_h5folders.sh` + `make_h5folders.sh` (organize `h5data/3d_data_*`),
   `setup_bh.sh` (horizon `.gp` → `.3d`), `setup_seeds.sh` (field-line seeds, if `fields`/`particleTracer`),
   `setup_cm.sh` (centers of mass), `setup_frames.sh`, and `setup_spinvtk_dimensionless.py` /
   `setup_spinvtk_dimension.py` (spin-vector `.vtk` from `bhns_BHspin.mon`). `setup_frames.sh` in turn runs
   `cray.sh` (→ `movieSeq_v2_arg.bash`, builds `overlap.txt`/`gap.txt`/`duplicate.txt` to deduplicate
   overlapping iterations across restart segments), `rmdupes.py`, then `SetMovie.sh` → **`setmovie.py`**, which
   generates the per-frame files `view_*.xml`, `volume_*.xml`, `time_*.txt` (camera/volume attributes
   interpolated between the template XMLs via cubic spline).

3. **Render** with one of the three run scripts (each loads `visit/3.1.4`, sources `params$1`, sets plot
   toggles, and invokes VisIt):
   - **`runLocal.sh [N]`** — runs VisIt **directly in the foreground** (one invocation per frame) for an
     explicitly listed `foldernum`/`ranknum`. Use for single/test frames. Run detached:
     `. runLocal.sh >& output &`, watch with `tail -f output`.
   - **`runMulti.sh [N]`** — the production batch path. Bundles `framesPerRun` frames into job scripts under
     `log/<date>_<jobName>/job/`, prepends the SLURM header from `bin/scheduler/multirun_template_anvil`, and
     **`sbatch`es** each. Controlled by `all`/`firstFolder`/`lastFolder` and `foldernum`/`ranknum` lists.
   - **`runMisc.sh`** — special **camera motions** (zoom, fly-over, fly-around) via `bin/filmBundled.sh`,
     toggled by `zoom_flag`/`fly_over_flag`/`fly_around_flag`. Each block names a single `h5folder`, a starting
     frame `idx`, `totframes`, and overriding view/volume XMLs.

Output frames (PNG) land in `movies/<date>_<jobName>/`; per-job logs in `log/<date>_<jobName>/{run,job,out}/`.

## Rendering architecture

The actual VisIt rendering lives in **`bin/bw_many_folder_scripts/`**:

- **`run.py`** — the VisIt CLI entry point (`visit -cli -s run.py ...`). It parses a long list of **positional**
  `sys.argv` (plot booleans, directories, XML paths), builds a `VisitPlot`, and calls `SetPlots()` then one of
  `PlotEvolve()` / `PlotZoom()` / `PlotFlyOver()` / `PlotFlyAround()`.
- **`runModule.py`** (~1350 lines) — defines `class VisitPlot` plus geometry/operator helpers (`box*`, `clip*`,
  `cylinder*`, `iso`, `threshold`, `reflect`), database loaders (`LoadandDefine`, `OpenDatabase ... CarpetHDF5`),
  plot builders (`PlotVol`, `PlotPseudo`, `PlotVelocity`, `PlotB`, `PlotBH`, `PlotTrace`), annotation/save
  setup, and the scalar-expression definitions (e.g. `logrho = log10(rho_b/maxdensity)`,
  `logbsq2r = log10(smallb2/(2*rho_b))`). This is where to change *how* fields are rendered.

⚠️ **The `run.py` argument contract is fragile and positional.** `run.py` reads fixed `sys.argv[i]` indices, and
the run scripts (`runLocal.sh`, `runMulti.sh`, `filmBundled.sh`) + the PBS templates
(`singleRun_anvil_frames.pbs`, `scheduler/multirun_template_anvil`) emit those arguments in matching order.
If you add or reorder a plot option, you must update **all** of: the caller's `visit ... run.py <args>` line,
`run.py`'s `sys.argv` indexing, and `VisitPlot`'s `PlotOpts`/`ArgList` unpacking — or frames render with the
wrong settings silently.

### Key concepts / vocabulary

- **folder** (`foldernum`, **1-indexed**): one `h5data/3d_data_YY_MM_DD_HHMMSS` directory = one simulation
  output/restart segment.
- **rank** (`ranknum`, **0-indexed**): a frame *within* a folder. The number of frames in a folder is
  `totranks = $(ls xml[N]/<folder>/time_* | wc -l)` — i.e. it is **derived from the generated `time_*` files**,
  so `setup.sh` must run before any render. Each rank maps to one `view_<rank>.xml` / `volume_<rank>.xml`.
- **`atts/` XML templates**: hand-authored VisIt attribute files (created by exporting from the VisIt GUI).
  `setmovie.py` interpolates *between* a start and end template to animate the camera/volume across frames.
  `atts_bhd/` is the previous preset set (git-ignored); `change_view.py` bulk-overwrites every generated
  `xml/3d_data_*/view_*.xml` with one chosen template (use to retro-fix an already-generated frame tree).

## Subsystems in `bin/`

- **`grid_code/`** — grid-based field-line seed generation (`seedmaker.py`, `bhcen1.txt`).
- **`gw_code/`** — gravitational-wave overlay: converts `Psi4`/strain data to VTK for 3D/2D GW surface plots
  (`params_gw.py`, `prepare_gw_rho.py`, `gw_rho_merger.py`, `GW_up.py`). Triggered when `updateGWdata=true` in
  `params`.
- **`particle_code/` & `particle_tracer/`** — Lagrangian tracer / particle-seeded field lines
  (`particlePicker.py`, `particlePickerModule.py`).
- **`plotting_tool/`** — auxiliary plotting.
- **`scheduler/multirun_template_anvil`** — the SLURM header (`#SBATCH -p shared -N1 -n1 --mem=32G`) prepended
  to every batched render job. `singleRun_anvil_frames.pbs` is the `wholenode` variant.

## Conventions & gotchas

- **SLURM is for Anvil.** Headers use Anvil partitions (`shared`, `wholenode`) — not TACC `-p normal`. The
  leftover `cd $PBS_O_WORKDIR` in the templates is a PBS-ism that is harmless under SLURM. Heavy renders belong
  in `sbatch` jobs (`runMulti.sh`), not on the login node; `runLocal.sh` foreground is for a handful of test
  frames only.
- **Module loads matter and differ by step:** `module load visit/3.1.4` for rendering, `module load python`
  for setup, `module load hdf5` for `h5ls`/`cray.sh`. VisIt must be pinned with `-forceversion 3.1.4`.
- **Foreign paths.** Scripts originate from other machines (Blue Waters `bw_many_folder_scripts`, TACC paths,
  `local_gw_setups/...frontera`). When adapting copied scripts, rewrite hardcoded absolute paths to this
  `root` (`/anvil/scratch/x-yguo11/bhdisk_sol_05`). The `root=` line in `params` is the anchor everything keys
  off.
- **Plot toggles live in the run scripts, not `params`.** `PlotDensAsIso`, `PlotSpinVec`, `cutPlot`, `bgcolor`,
  etc. are set near the top of `runLocal.sh`/`runMulti.sh`/`runMisc.sh`. `cutPlot=1` (show back half only)
  requires a matching `(0,-x,y)` view.
- This repo follows the broader scratch-workspace conventions in `/anvil/scratch/x-yguo11/CLAUDE.md` (HDF5
  layout, `it=<n>` iteration datasets, "prefer validating over deleting expensive simulation output"). Defer to
  that file for data-inspection guidance; this file covers the visualization pipeline specifically.
