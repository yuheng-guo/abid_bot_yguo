#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 01:00:00
#SBATCH -J mem_probe_j114
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/mem_probe_job114.out

# Replay job114's 10-frame sequence (folder 099) under a 64G cap, reading the
# cgroup memory high-water mark after EACH frame. Tells us whether peak RSS
# accumulates across serially-rendered frames (accumulation OOM) or stays flat
# (=> the 20G batch crash is I/O/contention, not memory).
# Output PNGs go to a throwaway temp dir; movies/ is untouched. No rerun/cancel.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

TMPOUT=/anvil/scratch/x-yguo11/bhdisk_sol_05/_mem_probe_tmp/job114
mkdir -p "$TMPOUT"

JOBFILE=/anvil/scratch/x-yguo11/bhdisk_sol_05/log/260602_1109_bhdisk_sol05_cut_51-100/job/job114.sh
CG=/sys/fs/cgroup/memory/slurm/uid_${UID}/job_${SLURM_JOB_ID}/memory.max_usage_in_bytes

gb() { awk "BEGIN{printf \"%.2f\", $1/1073741824}"; }

i=0
while IFS= read -r line; do
  i=$((i+1))
  # redirect this frame's save path into the temp dir
  newline=$(echo "$line" | sed "s#/movies/260602_1109_bhdisk_sol05_cut_51-100/#/_mem_probe_tmp/job114/#g")
  echo "=== frame $i  $(date +%H:%M:%S) ==="
  eval "$newline" > "$TMPOUT/frame_${i}.log" 2>&1
  if [ -r "$CG" ]; then
    v=$(cat "$CG")
    echo "    cgroup high-water after frame $i: $v bytes = $(gb $v) GB"
  fi
  # did this frame's PNG come out non-blank? (blank density PNGs are tiny)
  png=$(ls -S "$TMPOUT"/*_$(printf "%03d" $((i+7)))_*0000.png 2>/dev/null | head -1)
  [ -n "$png" ] && echo "    PNG: $(ls -la "$png" | awk '{print $5" bytes  "$NF}')"
  # surface any engine crash in this frame
  grep -qE "exited abnormally|could not be generated" "$TMPOUT/frame_${i}.log" && echo "    *** ENGINE CRASH in frame $i ***"
done < "$JOBFILE"

echo
echo "=== FINAL cgroup high-water ==="
[ -r "$CG" ] && { v=$(cat "$CG"); echo "$v bytes = $(gb $v) GB"; }
echo "=== PNG sizes (blank density ~ a few KB; good ~ 1 MB) ==="
ls -la "$TMPOUT"/*.png 2>/dev/null | awk '{print $5"  "$NF}'
