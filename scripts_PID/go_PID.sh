#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2020-01-08 11:53:13 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

runNum=$1
# numEvts=$2
numEvts=-1

root -l "run_detectEfficiency.C+($runNum,$numEvts)"
