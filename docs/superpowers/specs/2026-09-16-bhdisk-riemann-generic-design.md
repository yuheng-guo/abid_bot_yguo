# Generic riemann abid_bot — design

Date: 2026-09-16
Target: `Illinois-Relativity-Group/abid_bot`, orphan branch `yguo/bhdisk-riemann`

## Goal

One case-agnostic abid_bot that runs on riemann out of the box. A user clones the
branch, drops their own data into `h5data/`, runs `setup.sh`, and renders with
`runSingle` / `runLocal` / `runMulti`. No path editing, no scheduler, no Lmod.

It consolidates the two riemann ports built for `bhdisk_sol_32` and
`bhdisk_sol_05`, promoting everything those two had to hardcode into named
settings.

## Non-goals

- Supporting Anvil or Frontera. Those trees stay as they are on `master`.
- Merging into `master`. The branch is a deliverable, not a feature branch;
  unrelated history is accepted and intended.
- Fixing the broken `abid_bot_bhdisk/bhdisk_riemann` on `master` (see Follow-ups).
- Changing the physics, the plot pipeline, or the xml attribute format.

## Branch strategy

`git checkout --orphan yguo/bhdisk-riemann` — no parent commit, so nothing from
`master` is reachable. The tool sits at the repo root.

Consumers get only the tool:

    git clone -b yguo/bhdisk-riemann --single-branch \
        git@github.com:Illinois-Relativity-Group/abid_bot.git

A plain `git clone` still fetches all branches (176 MB of archive history), but
checking out this branch gives a clean working tree either way.

## Layout

    README.md            quickstart: clone -> h5data -> setup.sh -> run
    RIEMANN.md           what differs from the SLURM trees, and why
    .gitignore
    params               the contract (see below)
    setup.sh
    setup_params.py      derives case physics from the user's data
    change_view.py       swap views without re-running setup
    runSingle.sh         a few frames, by editing foldernum/ranknum
    runLocal.sh          same, kept as the name the README already uses
    runMulti.sh          many frames, $maxParallel at a time
    runMisc.sh           zoom / fly-over / fly-around paths
    bin/                 unchanged pipeline + scheduler/multirun_template_riemann
    h5data/              exactly what bhdisk_anvil ships — cube_edges.3d,
                         cube_edges_old.3d, line.3d, makebox.py, make_line.py,
                         box.3d — plus the optional link_h5data.sh helper

## The params contract

**`params` keeps `bhdisk_anvil`'s field order, names and comments verbatim.** It
is a file people read top to bottom and already know; re-organising it into
tiers would be a gratuitous familiarity break. The fields the group README tells
people to edit — `root`, `it`, `dt`, `M`, `rho_pseudoXML`, `rho_isoXML`,
`view1XML` — stay exactly where they are, with the same names.

Two additions, both non-disruptive:

- A short **`### EDIT THESE ###`** header block at the top listing those same
  fields, so a newcomer does not have to scan 200 lines to find them. It
  restates the README, it does not move anything.
- The **new knobs** (`cutNormal`, `showTimeLabel`, `transparentBG`) are added
  inline next to the settings they relate to, in the same comment style as
  their neighbours.

The riemann machine settings — VisIt 3.3.3 on `$PATH` at
`/data/shared/visit/bin`, and `maxParallel=16` for a 160-core shared box —
replace the `module load` lines that sat in the same place in the Anvil file.
Nobody needs to edit them.

`h5src` is **optional and unset by default** (see `h5data` below).

## Changes to `setup_params.py`

**Derive `offset`.** It currently derives `it`, `dt`, `firstTime`, `maxdensity`
and `M`, but not `offset`. `offset` is `first_iteration / it`, and it is what
makes the t/M label correct when a user's data does not start at iteration 0.
Left at 0, every frame is silently mislabelled — sol_05 starts at iteration
2051584, so its first frame would have read `t/M = 0` instead of `7443`.
`setmovie.py` names each frame `time_<state*dt/M>.txt` with
`state = frame_index + offset`, and `runModule.py` reads the label straight out
of that filename, so the error propagates to every image.

**Drop the `sultan` dependency.** The script currently runs
`pip install sultan` at import. A shared tool must not install packages or
require network access. Replace with stdlib `subprocess`.

**Do not overwrite a value the user has set.** Write a derived value only when
the field still holds the shipped placeholder. Otherwise keep the user's value
and print a warning when the two differ by more than 1%. Prevents the case where
a hand-entered ADM mass is silently replaced by `bhns.mon` cols 12+13 — on
sol_05 those disagree by 2.1%, which moves the last frame from t/M 9693 to 9492.

## New knobs (promoted from hardcoded values)

The two cases differ only in values that are currently literals inside
`runModule.py`:

| setting | sol_32 | sol_05 | new params name | ships as |
|---|---|---|---|---|
| cut plane normal | `(0,-1,0)` | `(0,0,1)` | `cutNormal` | `(0,-1,0)` |
| t/M caption | on | off | `showTimeLabel` | `1` |
| transparent PNG background | off | on | `transparentBG` | `0` |

Each reads from the environment in `runModule.py`, exported by `params`.
**Defaults are the sol_32 column**, because that matches the upstream Anvil
code, so a user porting from `bhdisk_anvil` sees no behaviour change.

**`cutPlot` ships as `1` in every run script.** Cut is the normal mode of
operation, and the uncut path is the fragile one: `runModule.py` only calls
`reflect()` when `cutPlot` is set, because in nocut mode the reflection doubles
the full 21-shell isosurface and overflows the VisIt engine. The sol_05 branch
already ships `cutPlot=1` in both `runLocal.sh` and `runMulti.sh`; sol_32 used
`cutPlot=0` only for its second, uncut campaign. Shipping `1` makes the default
path the one that is known to render.

## Fixes carried in from the two ports

These are riemann-correctness fixes, not preferences. All are already proven on
both cases.

- **`-forceversion 3.3.3`** everywhere (was 3.1.4).
- **No `module load`** anywhere. riemann has no Lmod.
- **`sbatch` -> `xargs -P $maxParallel`** in `runMulti.sh`, `runMisc.sh`,
  `bin/filmBundled.sh`, plus `bin/scheduler/multirun_template_riemann`.
- **`PlotBox()` reads `$root`** instead of a hardcoded `/anvil/scratch/...` path.
- **`PlotBH()` no longer calls `AddOperator("Delaunay")`.** VisIt 3.3.3 ships
  the Delaunay operator disabled and `visit -cli` has no API to enable it; the
  call raises `Invalid operator plugin name`. The horizon renders correctly
  without it.
- **`colorByMagnitude` added to the spin-vector atts.** 3.3.3 renamed the 3.1.4
  `colorByMag` field and defaults the new one to `true`, which overrides
  `vectorColor` and renders the arrow blue instead of the configured colour.
  Note: VisIt's attribute parser rejects XML comments — a single comment blanks
  the whole file to defaults.
- **`clean_h5folders.sh` quarantines on "no `*.h5`"**, not on "no files".
  Restart folders often hold only `CCTK_Proc1.out`, which passes a file-count
  test, consumes a folder index and renders nothing.
- **`rmdupes.py` must not follow symlinks.** It uses `shutil.move`, which
  resolves a symlinked data folder and physically relocates the files out of the
  user's data tree — it moved 106 GB out of `h5_extracted` on sol_05. With the
  symlink-farm layout this silently de-centralises the dataset. Fix: rename the
  link, never the target.

## Run scripts

riemann has no scheduler, so `runSingle` and `runLocal` are mechanically
identical — both run `visit -cli` inline. Both names are kept, and **both keep
the `foldernum=()` / `ranknum=()` array form people already use.** The only
change to `runSingle.sh` relative to `bhdisk_frontera`'s is that the `sbatch`
line becomes a direct `visit -cli` call.

- `runSingle.sh` — edit `foldernum` / `ranknum`, same as Frontera and Anvil.
  Optionally accepts `<folder> <rank>` as an override for convenience; with no
  arguments it behaves exactly as before.
- `runLocal.sh` — identical form; kept because the group README already
  documents it as the way to run on local machines like riemann.
- `runMulti.sh` — `firstFolder`/`lastFolder`, `xargs -P $maxParallel`.
- `runMisc.sh` — camera-path variants, ported the same way.

All keep the `params<N>` / `xml<N>` set mechanism (`. runMulti.sh 2` reads
`params2` and writes `xml2/`), which is how two campaigns with different views
run concurrently.

Every run writes to its own `movies/<DATE>_<jobName>/` so repeat runs do not
overwrite each other.

`visit -cli` drops to an interactive prompt on an uncaught script exception and
hangs forever; the scripts redirect `< /dev/null` so a failure exits.

## `h5data`

**The existing structure is preserved exactly.** It is what people are used to
setting up, and `setup.sh`, `cray.sh`, `setmovie.py`, `setup_bh.sh` and
`setup_spinvtk_dimensionless.py` all read it directly. Nothing about it changes:

    h5data/3d_data_YY_MM_DD_HHMMSS/rho_b.file_*.h5
    h5data/bhns.xon, bhns.mon, bhns_BHspin.mon, BH_diagnostics.ah1.gp
    h5data/horizon/all_horizon/h.t*.ah1.gp   (+ BH_diagnostics.ah1.gp)

The user populates it themselves, by symlink or copy, exactly as the group
README already describes. The branch ships only the geometry files Anvil ships.

`BH_diagnostics.ah1.gp` is needed in both places:
`setup_spinvtk_dimensionless.py` reads it from `horizon/all_horizon/`, other
steps read the top-level copy. This is undocumented today and is a common way
for the spin vector to come out empty — the README gains a line about it.

### Optional helper

`h5data/link_h5data.sh` is an **optional convenience**, sitting alongside
`makebox.py` and `make_line.py`, for the case where the raw output is too large
to live inside the tree. Given `h5src=<path>` in `params` it renames
`YY_MM_DD_HHMMSS` to `3d_data_YY_MM_DD_HHMMSS` and symlinks the folders,
diagnostics and `horizon/` into `h5data/` — producing exactly the layout above.

It is not part of the documented workflow and `h5src` is unset by default.
Someone who has never heard of it sets up `h5data/` the way they always have.
Generalised from the sol_32 version; the sol_32-only `sol32_may_hdf5` rescue
block is removed.

One caveat the README must carry: if `h5data/3d_data_*` are symlinks, the
`rmdupes.py` fix listed above is what stops `setup.sh` relocating the real data
out of the source tree.

## `.gitignore`

    xml*/  movies/  log/  bhdata/  h5data/3d_data_*  h5data/bad_data/
    cm.txt  visitlog.py  xml_log.txt  __pycache__/  *.pyc  *.tar.gz

No generated file ships. Committed logs are what put 113 MB of `xml_log.txt`
into `master`'s history across three trees.

## Attaching the two case trees

Both keep their `abid_bot_yguo` branch and their local case params. Each gains
the group branch as a second remote:

    git remote add group git@github.com:Illinois-Relativity-Group/abid_bot.git
    git fetch group yguo/bhdisk-riemann

Generic fixes then flow in by cherry-pick. Case-specific values
(`root`, `h5src`, `M`, `maxdensity`, `offset`, view choices) stay local and
uncommitted, as they are today. Nothing in the running campaigns is disturbed.

## Verification

The branch is not done until, on riemann:

1. A clean clone of the branch into an empty directory renders one frame from
   the sol_32 data using only documented steps.
2. The same clone renders one frame from the sol_05 data, by editing `params`
   only — proving case-independence.
3. `setup_params.py` recovers `it=512`, `dt=0.1097556941`, and `offset=4007`
   for sol_05 and `offset=0` for a run starting at iteration 0.
4. Both renders match the corresponding image already produced by the existing
   case trees.

## Risks

- **Orphan branch cannot be merged to `master`.** Accepted explicitly.
- **`master`'s `abid_bot_bhdisk/bhdisk_riemann` stays broken**, so anyone
  cloning `master` still finds a SLURM tree labelled riemann. See Follow-ups.
- **`runSingle.sh` is new to this tree** — ported from `bhdisk_frontera`, the
  only tree that has one. It needs testing, not just transcription.
- **VisIt 3.3.3 vs 3.1.4 attribute drift.** `colorByMag` was one instance; the
  other twelve `atts/*.xml` files still carry the old field name and may show
  the same symptom on other plots.

## Follow-ups (out of scope)

- Fix or delete `abid_bot_bhdisk/bhdisk_riemann` on `master`.
- Audit the remaining `atts/*.xml` for 3.1.4 field names.
- History rewrite to drop the committed `xml_log.txt` blobs from `master`.
