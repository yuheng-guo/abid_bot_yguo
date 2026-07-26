#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 01:00:00
#SBATCH -J probe_nocutfix
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/probe_nocut_fix.out

# Isolate WHY the nocut density-iso crashes the engine, using an instrumented COPY
# of the pipeline (bin/bw_nocut_test). All renders: nocut (cutPlot=0), folder090 state10, 64G.
#   1 asis        BHTEST=''        21-shell  -> reproduce crash (control)
#   2 noreflect   BHTEST=noreflect 21-shell  -> is reflect() the culprit?
#   3 fewershells BHTEST=''        5-shell   -> is it geometry complexity (21 shells)?
#   4 boxbound    BHTEST=boxbound  21-shell  -> does a spatial bound fix it (like clip does)?
# good PNG >100K (density) | blank <20K (engine crashed, logrho dropped). Output -> temp.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
TESTDIR=$ROOT/bin/bw_nocut_test
A=$TESTDIR/atts
RUNPY=$TESTDIR/run.py
export PYTHONPATH=$TESTDIR:$PYTHONPATH
TMP=$ROOT/_nocut_fix_tmp; mkdir -p "$TMP"
DD=3d_data_26_03_21_154340

# render <label> <BHTEST> <isoxml> <pref>
render() {
  local label=$1 bht=$2 isox=$3 pref=$4
  echo "==================== $label  (BHTEST='$bht', iso=$isox)  $(date +%H:%M:%S) ===================="
  BHTEST="$bht" visit -cli -nowin -forceversion 3.1.4 -s $RUNPY \
    0 1 0 0 0 0 1 0 blue 1 0 0 0 \
    $ROOT/h5data/$DD $ROOT/xml/$DD $TMP/$pref 10 24 1 \
    $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
    0.000461833107670726 $A/NSNS_pseudo_disk.xml $A/$isox 1 \
    $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
    $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused 2>&1 | \
    grep -E "exited abnormally|could not be generated|Reflect set|Box set|Saved |t/M ="
  local png=$(ls -S "$TMP/${pref}"*.png 2>/dev/null | head -1)
  if [ -n "$png" ]; then
    local sz=$(stat -c%s "$png")
    echo ">>> $label: $sz bytes -> $([ "$sz" -gt 100000 ] && echo 'GOOD (density present)' || echo 'BLANK (engine crashed)')"
  else echo ">>> $label: NO PNG"; fi
  echo
}

render "1_asis"        ""         bhdisk_iso_21_shells.xml N1_asis_
render "2_noreflect"   noreflect  bhdisk_iso_21_shells.xml N2_noreflect_
render "3_fewershells" ""         bhdisk_iso_5_shells.xml  N3_fewer_
render "4_boxbound"    boxbound   bhdisk_iso_21_shells.xml N4_box_

echo "=== SUMMARY ==="
for p in N1_asis N2_noreflect N3_fewer N4_box; do
  f=$(ls -S "$TMP/${p}"*.png 2>/dev/null | head -1)
  [ -n "$f" ] && printf "%-14s %8s bytes  %s\n" "$p" "$(stat -c%s "$f")" "$f"
done
