# sol_05 setup

The riemann-ported visualization pipeline, retargeted at sol_05. Git branch
here is **`bhdisk_sol_05_riemann`**, remote
`git@github.com:yuheng-guo/abid_bot_yguo.git`. See `RIEMANN.md` for the riemann
port itself -- everything there applies unchanged -- and `../STRUCTURE.md` for
how this folder is laid out.

This directory is `abid-bot/` because it generates images. Gravitational-wave
generation lives in a separate tree, `../gw-generation/`, on the
Illinois-Relativity-Group repo (branch `yguo/gw-multi-radius`). The two are
named apart on purpose: they share an ancestor but do unrelated work, and for a
while both were called `abid_bot`, which meant the same name referred to the
visualization tree in `bhdisk_sol_32` and the GW tree here.

## What was retargeted

| setting | value |
|---|---|
| `root` | `/data/yuhengguo/bhdisk_sol_05/abid-bot` |
| `h5src` | `/data/yuhengguo/bhdisk_sol_05/hdf5/h5_extracted` |
| `M` (ADM mass) | **`0.0590833070753691`** (sol_32 was `0.0564177477296656`) |
| `maxdensity` | **`0.000461833107670726`** (sol_32 was `0.000223625890017604`) |
| `it`, `dt` | `512`, `0.1097556941` -- same as sol_32, reused deliberately |

Both `params` and `params2` carry these. `params2` differs from `params` only
in `view1XML` (`bhdisk_view_30deg_superzoomin.xml`), as on sol_32.

Job names in the run scripts are now `bhdisk_sol05_*`. Folder/frame ranges are
reset to placeholders -- they can't be set until the data is extracted.

## Carried over from sol_32 verbatim

- All riemann fixes: VisIt 3.3.3 on `$PATH`, no Lmod, `sbatch` -> `xargs -P
  $maxParallel`, `PlotBox()` reading `$root`, `PlotBH()` without the disabled
  Delaunay operator, `bin/scheduler/multirun_template_riemann`.
- The yellow spin-arrow fix: `colorByMagnitude` added to
  `atts/Vec_spin_superzoomin_dimensionless.xml` (3.3.3 renamed the 3.1.4
  `colorByMag` field, and its default is `true`, which overrode `vectorColor`).
- `NO_TIME_LABEL=1` env toggle in `runModule.py` to render without the t/M
  label. Inert unless set.
- `bin/clean_h5folders.sh` quarantining on "no `*.h5`" rather than "no files".
- `bin/link_h5data.sh`, including the empty-target replacement and the
  bad_data release guard.
- `maxParallel=16`, plot toggles, all `atts/` xml.

## NOT done yet -- the tars are still landing

Nothing under `hdf5/` was touched. `hdf5/h5_extracted/` does not exist yet.

All of `it`, `dt`, `M` and `maxdensity` are now set, so `params` does not need
`setup_params.py`. Do **not** run it: it would overwrite `M` and `maxdensity`
with values re-derived from `bhns.mon`, and `root` with `pwd`. The only value
still at its default is `firstTime` (`00000.00000000000`, with `offset=0`),
which is correct if the run starts at iteration 0 -- worth a glance at the
first iteration number in the first `3d_data_*` folder once the data is out.

## Order of operations once the tars are complete

    cd /data/yuhengguo/bhdisk_sol_05/abid-bot
    # 1. extract tars into hdf5/h5_extracted/
    # 2. confirm firstTime/offset against the first iteration number
    . params
    . bin/link_h5data.sh
    . setup.sh                 # and: . setup.sh 2   for the params2/xml2 set
    # 3. set foldernum/ranknum in runLocal.sh, render one frame for review
    . runLocal.sh
    # 4. set firstFolder/lastFolder in runMulti.sh, then
    . runMulti.sh              # campaign 1: zoomin, no cut
    . runMulti2.sh 2           # campaign 2: superzoomin + cut
