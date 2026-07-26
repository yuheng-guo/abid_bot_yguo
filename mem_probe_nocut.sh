#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 00:40:00
#SBATCH -J mem_probe_nocut
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/mem_probe_nocut.out

# Reproduce the NOCUT frame 090_010 that crashed at 18GB under the 32G batch.
# Under a 64G cap (no ceiling pressure) read the EXACT cgroup high-water
# (memory.max_usage_in_bytes catches transient spikes that 30s jobacctgather misses)
# AND check whether the PNG is good (>500K, has density) or blank (<20K).
# Discriminates: H1 nocut needs >32G | H2 node-OOM/contention | H3 non-memory bug.
# Output to throwaway temp dir; movies/ untouched. No cancel/rerun.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

TMPOUT=/anvil/scratch/x-yguo11/bhdisk_sol_05/_mem_probe_tmp/nocut
mkdir -p "$TMPOUT"
ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
A=$ROOT/bin/bw_many_folder_scripts/atts
CG=/sys/fs/cgroup/memory/slurm/uid_${UID}/job_${SLURM_JOB_ID}/memory.max_usage_in_bytes
gb() { awk "BEGIN{printf \"%.2f\", $1/1073741824}"; }

# background process-tree RSS sampler (backup to cgroup reading)
( while true; do
    ps -u "$USER" -o rss= 2>/dev/null | awk '{s+=$1} END{print s+0}'
    sleep 2
  done ) > "$TMPOUT/rss.txt" &
SAMP=$!

echo "=== nocut render start $(date) ==="
# EXACT failing command (argv: ...0 1 0 0 0 0 1 0 blue... => refPlot=1 cutPlot=0 = nocut), save path -> temp
visit -cli -nowin -forceversion 3.1.4 -s $ROOT/bin/bw_many_folder_scripts/run.py \
  0 1 0 0 0 0 1 0 blue 1 0 0 0 \
  $ROOT/h5data/3d_data_26_03_21_154340 $ROOT/xml/3d_data_26_03_21_154340 \
  $TMPOUT/probe_nocut_090_010_ 10 24 1 \
  $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
  0.000461833107670726 $A/NSNS_pseudo_disk.xml $A/bhdisk_iso_21_shells.xml 1 \
  $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
  $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused
echo "=== nocut render end $(date) ==="
kill $SAMP 2>/dev/null

echo
PEAK_KB=$(sort -n "$TMPOUT/rss.txt" | tail -1)
echo "process-tree RSS peak (sampler): ${PEAK_KB:-0} KB = $(gb $(( ${PEAK_KB:-0} * 1024 )))GB"
[ -r "$CG" ] && { v=$(cat "$CG"); echo "cgroup EXACT high-water: $v bytes = $(gb $v) GB"; }
echo
echo "=== resulting PNG (good>500K has density / blank<20K = density dropped) ==="
ls -la "$TMPOUT"/probe_nocut_090_010_*.png 2>/dev/null | awk '{print $5" bytes  "$NF}'
echo
echo "=== did the engine crash even at 64G? ==="
# (this script's own stdout is the slurm out; grep the visit messages above)
