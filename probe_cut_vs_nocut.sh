#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 00:50:00
#SBATCH -J probe_cutvnocut
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/probe_cut_vs_nocut.out

# Isolate the nocut blank-density crash: render the SAME data 3 ways under 64G.
#  A) cut  folder090 state10 (cutPlot=1)  -> does the clip path work on this data?
#  B) nocut folder090 state10 (cutPlot=0) -> reconfirm crash (determinism)
#  C) nocut folder091 state6  (cutPlot=0) -> is the nocut crash consistent across folders?
# good PNG >500K (has density) | blank <20K (logrho dropped). Output -> temp, movies/ untouched.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
A=$ROOT/bin/bw_many_folder_scripts/atts
RUNPY=$ROOT/bin/bw_many_folder_scripts/run.py
TMP=$ROOT/_mem_probe_tmp/cutvnocut; mkdir -p "$TMP"

# render <label> <cutPlotFlag> <dataDirName> <rank> <outprefix>
render() {
  local label=$1 cut=$2 dd=$3 rank=$4 pref=$5
  echo "==================== $label  (cutPlot=$cut, $dd, rank $rank)  $(date +%H:%M:%S) ===================="
  visit -cli -nowin -forceversion 3.1.4 -s $RUNPY \
    0 1 0 0 0 0 1 $cut blue 1 0 0 0 \
    $ROOT/h5data/$dd $ROOT/xml/$dd $TMP/$pref $rank 24 1 \
    $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
    0.000461833107670726 $A/NSNS_pseudo_disk.xml $A/bhdisk_iso_21_shells.xml 1 \
    $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
    $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused 2>&1 | \
    grep -E "exited abnormally|could not be generated|Saved |Rendering window|t/M ="
  local png=$(ls -S "$TMP/${pref}"*.png 2>/dev/null | head -1)
  if [ -n "$png" ]; then
    local sz=$(stat -c%s "$png")
    echo ">>> $label PNG: $sz bytes -> $([ "$sz" -gt 500000 ] && echo 'GOOD (density present)' || echo 'BLANK (density dropped)')"
  else
    echo ">>> $label PNG: NONE produced"
  fi
  echo
}

render "A_CUT_f090_s10"   1 3d_data_26_03_21_154340 10 A_cut_090_010_
render "B_NOCUT_f090_s10" 0 3d_data_26_03_21_154340 10 B_nocut_090_010_
render "C_NOCUT_f091_s6"  0 3d_data_26_03_22_041432 6  C_nocut_091_006_

echo "=== SUMMARY ==="
ls -la "$TMP"/*.png 2>/dev/null | awk '{print $5"  "$NF}'
