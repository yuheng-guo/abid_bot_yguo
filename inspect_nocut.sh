#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=32G
#SBATCH --export=ALL
#SBATCH -t 00:40:00
#SBATCH -J inspect_nocut
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/inspect_nocut/inspect_nocut.out

# Render a few uncut frames of folder 090 (real pipeline, fixed reflect) into a
# PERSISTENT folder for the user to inspect. cutPlot=0, 21-shell, exact params settings.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
B=$ROOT/bin/bw_many_folder_scripts
A=$B/atts
OUT=$ROOT/inspect_nocut; mkdir -p "$OUT"
DD=3d_data_26_03_21_154340

for rank in 0 11 23; do
  echo "=== rank $rank  $(date +%H:%M:%S) ==="
  visit -cli -nowin -forceversion 3.1.4 -s $B/run.py \
    0 1 0 0 0 0 1 0 blue 1 0 0 0 \
    $ROOT/h5data/$DD $ROOT/xml/$DD $OUT/nocut_090_$(printf "%03d" $rank)_ $rank 24 1 \
    $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
    0.000461833107670726 $A/NSNS_pseudo_disk.xml $A/bhdisk_iso_21_shells.xml 1 \
    $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
    $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused 2>&1 | \
    grep -E "exited abnormally|could not be generated|Saved |t/M ="
done

echo "=== PNGs for inspection ==="
ls -la "$OUT"/*.png | awk '{print $5" bytes  "$NF}'
