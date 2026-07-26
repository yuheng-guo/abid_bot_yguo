#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 00:40:00
#SBATCH -J probe_opacity
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/probe_opacity.out

# Test the never-used lever: opacityType="ColorTable" (per-shell alpha from the .ct alpha ramp).
# Same data/view/rank as runLocal.sh folder 120 rank 0, NOCUT, refPlot=0 (NO reflect doubling).
# Only rho_pseudoXML changes between renders:
#   V1 = NSNS_pseudo_disk_ctalpha.xml  -> bhdisk_opaque.ct  (alpha 0.55 outer -> 0.80 core, increasing)
#   V2 = NSNS_pseudo_disk_layered.xml  -> bhdisk_layered.ct (alpha 0.65 outer -> 0.30 core, decreasing)
# Frames save with transparent bg, so BLEED-THROUGH = transparent (white) pixels in the envelope.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
A=$ROOT/bin/bw_many_folder_scripts/atts
RUNPY=$ROOT/bin/bw_many_folder_scripts/run.py
DD=3d_data_26_04_09_080010          # folder 120 (PPI lump)
RANK=0
TOT=27
TMP=$ROOT/_opacity_probe; mkdir -p "$TMP"

# render <label> <rho_pseudoXML> <outprefix>
render() {
  local label=$1 pseudo=$2 pref=$3
  echo "==================== $label   ($(basename $pseudo))   $(date +%H:%M:%S) ===================="
  visit -cli -nowin -forceversion 3.1.4 -s $RUNPY \
    0 1 0 0 0 0 0 0 blue 1 0 0 0 \
    $ROOT/h5data/$DD $ROOT/xml/$DD $TMP/$pref $RANK $TOT 1 \
    $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
    0.000461833107670726 $pseudo $A/bhdisk_iso_21_shells.xml 1 \
    $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
    $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused 2>&1 | \
    grep -E "exited abnormally|could not be generated|Saved |Rendering window|t/M ="
  local png=$(ls -S "$TMP/${pref}"*.png 2>/dev/null | head -1)
  [ -n "$png" ] && echo ">>> $label PNG: $(stat -c%s "$png") bytes -> $png" || echo ">>> $label PNG: NONE"
  echo
}

render "V1_ctalpha_opaque"  $A/NSNS_pseudo_disk_ctalpha.xml   V1_ctalpha_
render "V2_layered"         $A/NSNS_pseudo_disk_layered.xml    V2_layered_

echo "=== SUMMARY ==="
ls -la "$TMP"/*.png 2>/dev/null | awk '{print $5"  "$NF}'
