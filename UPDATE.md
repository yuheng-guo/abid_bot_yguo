# Updating the visualization code from upstream

This is a **flattened** clone. In the GitHub repo the tool lives nested at
`abid_bot_bhdisk/bhdisk_anvil/`; here it has been moved to the root of this
folder. Because the local layout differs from the remote, pull upstream
changes with git's **subtree** merge strategy instead of a plain `git pull`:

    git pull -X subtree=abid_bot_bhdisk/bhdisk_anvil origin master

That shifts upstream's `abid_bot_bhdisk/bhdisk_anvil/` subfolder onto this flat
root automatically. (A plain `git pull` would try to recreate the nested dirs.)

Your local data/output files are ignored via `.git/info/exclude`, so they
won't interfere with merges.
