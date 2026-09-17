# Where the generic version lives

This tree is the **bhdisk_sol_05** case: its `params`, `xml*/` and `movies/` are
specific to this simulation and stay here.

The generic riemann abid_bot — the one other people clone — is on the group
repo, fetched here as the `group` remote:

    git@github.com:Illinois-Relativity-Group/abid_bot.git   branch yguo/bhdisk-riemann

    git fetch group yguo/bhdisk-riemann
    git log --oneline group/yguo/bhdisk-riemann

To see what this tree has that the generic branch does not, or vice versa:

    git diff group/yguo/bhdisk-riemann -- bin/ setup.sh setup_params.py

The two are kept in step for **code**, not for params. Fixes that matter to
everyone (the numeric `time_*.txt` and `bh1_cm_*.txt` sorts, the
`rmdupes.py` symlink fix, the `clean_h5folders.sh` guards) are applied in
both places. Case values — `M`, `maxdensity`, `offset`, `dt` — are
deliberately local and are not synced.

`origin` remains your own repo, `abid_bot_yguo`.
