#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH -t 00:15:00
#SBATCH -J probe_opac_dbg
#SBATCH -o /anvil/scratch/x-yguo11/bhdisk_sol_05/probe_opacity_dbg.out

. ${MODULESHOME}/init/bash
module load gcc/11.2.0
module load openmpi/4.0.6
module load visit/3.1.4

ROOT=/anvil/scratch/x-yguo11/bhdisk_sol_05
A=$ROOT/bin/bw_many_folder_scripts/atts
RUNPY=$ROOT/bin/bw_many_folder_scripts/run.py
DD=3d_data_26_04_09_080010
TMP=$ROOT/_opacity_probe; mkdir -p "$TMP"

echo "which visit: $(which visit)"
echo "===== FULL RAW OUTPUT, V1 ctalpha render ====="
visit -cli -nowin -forceversion 3.1.4 -s $RUNPY \
  0 1 0 0 0 0 0 0 blue 1 0 0 0 \
  $ROOT/h5data/$DD $ROOT/xml/$DD $TMP/DBG_ 0 27 1 \
  $A/modifiedVec.xml $A/bsq2r.xml $A/g00_pseudo.xml $A/g00_iso.xml \
  0.000461833107670726 $A/NSNS_pseudo_disk_ctalpha.xml $A/bhdisk_iso_21_shells.xml 1 \
  $A/Vec_spin_superzoomin_dimensionless.xml $A/Vec_fewer.xml \
  $A/bsq2r_pseudo_test.xml $A/bsq2r_iso_test.xml 0 0 notused 2>&1
echo "===== EXIT CODE: $? ====="
echo "===== PNGs ====="
ls -la "$TMP"/DBG_*.png 2>/dev/null || echo "no DBG png"
