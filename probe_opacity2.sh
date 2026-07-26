#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=128G
#SBATCH --export=ALL
#SBATCH -t 01:10:00
#SBATCH -J probe_opac2
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/probe_opacity2.out

# folder 120 (PPI lump) rank 0, NOCUT, refPlot=0. Constant opacity (ColorTable mode crashes).
# Test whether densifying shells lets a translucent per-shell opacity still occlude the bg.
#   A = ctalpha (ColorTable)      : RECONFIRM the VisIt crash (control)
#   B = const0.30 + 21 shells     : moderate uniform, current shell count (baseline)
#   C = const0.30 + dense35 shells: densify fix
#   D = const0.18 + dense35 shells: densify + low per-shell opacity (max layering)
# Bleed-through = transparent (white) pixels in the envelope. Good frame ~ tens-hundreds KB.

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
A=$ROOT/bin/bw_many_folder_scripts/atts
RUNPY=$ROOT/bin/bw_many_folder_scripts/run.py
DD=3d_data_26_04_09_080010
TMP=$ROOT/_opacity_probe; mkdir -p "$TMP"
LOG=$ROOT/_opacity_probe/logs; mkdir -p "$LOG"

# render <label> <rho_pseudoXML> <rho_isoXML> <prefix>
render() {
  local label=$1 pseudo=$2 iso=$3 pref=$4
  echo "==================== $label   $(date +%H:%M:%S) ===================="
  echo "   pseudo=$(basename $pseudo)  iso=$(basename $iso)"
  visit -cli -nowin -forceversion 3.1.4 -s $RUNPY \
    0 1 0 0 0 0 0 0 blue 1 0 0 0 \
    $ROOT/h5data/$DD $ROOT/xml/$DD $TMP/$pref 0 27 1 \
    $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
    0.000461833107670726 $pseudo $iso 1 \
    $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
    $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused > "$LOG/$label.log" 2>&1
  local ec=$?
  local png=$(ls -S "$TMP/${pref}"*.png 2>/dev/null | head -1)
  local crash=$(grep -cE "out_of_range|exited abnormally|could not be generated|terminate called" "$LOG/$label.log")
  echo "   exit=$ec  crashlines=$crash"
  [ -n "$png" ] && echo ">>> $label PNG: $(stat -c%s "$png") bytes -> $(basename $png)" || echo ">>> $label PNG: NONE (see $LOG/$label.log)"
  echo
}

render "A_ctalpha_COLORTABLE" $A/NSNS_pseudo_disk_ctalpha.xml $A/bhdisk_iso_21_shells.xml A_ctab_
render "B_const030_21shell"   $A/NSNS_pseudo_const030.xml     $A/bhdisk_iso_21_shells.xml B_c030_21_
render "C_const030_dense35"   $A/NSNS_pseudo_const030.xml     $A/bhdisk_iso_dense35.xml   C_c030_d35_
render "D_const018_dense35"   $A/NSNS_pseudo_const018.xml     $A/bhdisk_iso_dense35.xml   D_c018_d35_

echo "=== SUMMARY ==="
ls -la "$TMP"/*.png 2>/dev/null | awk '{print $5"  "$NF}'
