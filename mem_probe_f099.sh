#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 00:30:00
#SBATCH -J mem_probe_f099
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/mem_probe_f099.out

# Measure TRUE peak render memory for the heavy folder-099 frame that OOMs at 20G.
# Renders ONE frame under a 64G cap (won't be OOM-killed), samples RSS, prints peak.
# Output PNG redirected to a throwaway temp dir so movies/ is untouched.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

TMPOUT=/anvil/scratch/x-yguo11/bhdisk_sol_05/_mem_probe_tmp
mkdir -p "$TMPOUT"

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
RUNPY=$ROOT/bin/bw_many_folder_scripts/run.py
ATTS=$ROOT/bin/bw_many_folder_scripts/atts
DATADIR=$ROOT/h5data/3d_data_26_03_27_013218
XMLDIR=$ROOT/xml/3d_data_26_03_27_013218
TOSAVE=$TMPOUT/probe_099_008_

# ---- background RSS sampler (process-tree, summed) ----
PEAK=0
(
  while true; do
    rss=$(ps -u "$USER" -o rss=,comm= 2>/dev/null | grep -iE 'visit|engine|mdserver|vcl|cli|python' | awk '{s+=$1} END{print s+0}')
    echo "$rss"
    sleep 2
  done
) > "$TMPOUT/rss_samples.txt" &
SAMPLER=$!

echo "=== render start $(date) ==="
visit -cli -nowin -forceversion 3.1.4 -s $RUNPY 0 1 0 0 0 0 1 1 blue 1 0 0 0 \
  $DATADIR $XMLDIR $TOSAVE 8 23 1 \
  $ATTS/modifiedVec.xml $ATTS/bsq2r.xml $ATTS/g00_pseudo.xml $ATTS/g00_iso.xml \
  0.000461833107670726 $ATTS/NSNS_pseudo_disk.xml $ATTS/bhdisk_iso_21_shells.xml 1 \
  $ATTS/Vec_spin_superzoomin_dimensionless.xml $ATTS/Vec_fewer.xml \
  $ATTS/bsq2r_pseudo_test.xml $ATTS/bsq2r_iso_test.xml 0 0 notused
echo "=== render end $(date) ==="

kill $SAMPLER 2>/dev/null

# peak from ps samples (KB -> GB)
PEAK_KB=$(sort -n "$TMPOUT/rss_samples.txt" | tail -1)
echo "PEAK process-tree RSS (ps sampler): ${PEAK_KB} KB = $(awk "BEGIN{printf \"%.2f\", ${PEAK_KB:-0}/1048576}") GB"

# authoritative cgroup peak, if exposed
for f in /sys/fs/cgroup/memory/slurm/uid_${UID}/job_${SLURM_JOB_ID}/memory.max_usage_in_bytes \
         /sys/fs/cgroup/memory.peak; do
  if [ -r "$f" ]; then
    v=$(cat "$f")
    echo "cgroup peak ($f): $v bytes = $(awk "BEGIN{printf \"%.2f\", $v/1073741824}") GB"
  fi
done

echo "=== rendered PNG (size tells us if it succeeded / non-blank) ==="
ls -la "$TMPOUT"/probe_099_008_* 2>/dev/null
