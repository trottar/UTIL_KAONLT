#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2020-01-13 15:02:15 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

runNum=$1
# numEvts=$2
numEvts=-1

spec=hms
detec=cer
root -b -q -l "run_detectEfficiency.C+($runNum,$numEvts,$spec,$detec)"
