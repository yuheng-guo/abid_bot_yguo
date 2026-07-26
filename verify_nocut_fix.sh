#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=32G
#SBATCH --export=ALL
#SBATCH -t 00:30:00
#SBATCH -J verify_nocut
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/verify_nocut_fix.out

# Verify the reflect fix using the REAL pipeline + the EXACT production nocut command
# (folder 090, frame 010) that came from params/runMulti. Real run.py (now fixed),
# real 21-shell atts, cutPlot=0. Output -> temp so movies/ is untouched.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
B=$ROOT/bin/bw_many_folder_scripts
A=$B/atts
TMP=$ROOT/_verify_tmp; mkdir -p "$TMP"

echo "=== render start $(date) ==="
visit -cli -nowin -forceversion 3.1.4 -s $B/run.py \
  0 1 0 0 0 0 1 0 blue 1 0 0 0 \
  $ROOT/h5data/3d_data_26_03_21_154340 $ROOT/xml/3d_data_26_03_21_154340 \
  $TMP/verify_nocut_090_010_ 10 24 1 \
  $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
  0.000461833107670726 $A/NSNS_pseudo_disk.xml $A/bhdisk_iso_21_shells.xml 1 \
  $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
  $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused 2>&1 | \
  grep -E "exited abnormally|could not be generated|Reflect set|Saved |t/M ="
echo "=== render end $(date) ==="

png=$(ls -S "$TMP"/verify_nocut_090_010_*.png 2>/dev/null | head -1)
if [ -n "$png" ]; then
  sz=$(stat -c%s "$png")
  echo ">>> RESULT: $sz bytes -> $([ "$sz" -gt 100000 ] && echo 'GOOD (density present)' || echo 'BLANK (still crashing)')"
  echo "$png"
else echo ">>> RESULT: NO PNG produced"; fi