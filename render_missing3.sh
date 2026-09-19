#!/bin/bash
# Resumable renderer for the set-3 (GW-composite) disk frames.
#
#   ./render_missing3.sh [NPAR]
#
# runMulti3.sh builds 40 job scripts of visit commands but has no skip logic and
# makes a fresh timestamped output dir per launch, so an interrupted run cannot be
# continued. This reads the SAME job scripts, drops every frame whose PNG already
# exists, and runs the remainder NPAR at a time into the SAME movies/ dir.
#
# Why low NPAR: each frame is a fresh `visit -cli` that random-reads a ~150 MB
# HDF5 file. At 40-way the array thrashed (queue depth 42, 0 frames in 12 min)
# once the page cache was evicted by the VTK/OBJ writes. Fewer, more sequential
# readers is strictly faster here.
set -u
cd "$(dirname "$0")"
export PATH=/data/shared/visit/bin:$PATH
export NO_TIME_LABEL=1 TRANSPARENT_BG=1     # set-3 look: no t/M caption, alpha-0 background
NPAR="${1:-10}"
PIDFILE="$(pwd)/.render_missing3.pid"
# Record our process-group id. Managing this run by PID file avoids `pkill -f <pattern>`,
# which repeatedly matched the managing shell's own command line and killed it.
echo $$ > "$PIDFILE"
LOGDIR=$(ls -dt log/*diskgw_meshmatch | head -1)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# one visit command per line, in frame order
cat "$LOGDIR"/job/job*.sh > "$WORK/all.txt"
: > "$WORK/todo.txt"
while IFS= read -r line; do
  [ -z "$line" ] && continue
  pre=$(printf '%s\n' "$line" | tr ' ' '\n' | grep '/movies/' | head -1)
  [ -z "$pre" ] && continue
  compgen -G "${pre}*.png" > /dev/null && continue   # already rendered -> skip
  printf '%s\n' "$line" >> "$WORK/todo.txt"
done < "$WORK/all.txt"

TOT=$(wc -l < "$WORK/all.txt"); TODO=$(wc -l < "$WORK/todo.txt")
echo "$(date '+%H:%M:%S') frames total=$TOT already=$((TOT-TODO)) todo=$TODO  NPAR=$NPAR"
[ "$TODO" -eq 0 ] && { echo "nothing to do"; exit 0; }

xargs -a "$WORK/todo.txt" -d '\n' -P "$NPAR" -I{} bash -c '{} < /dev/null > /dev/null 2>&1' 
echo "$(date '+%H:%M:%S') done; frames now = $(find "$(ls -dt movies/*diskgw_meshmatch|head -1)" -name '*.png' | wc -l)"
