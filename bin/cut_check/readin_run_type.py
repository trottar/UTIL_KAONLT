#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-03-22 13:12:57 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import os, sys

################################################################################################################################################
'''
User Inputs
'''

#ROOTPrefix = sys.argv[1]

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
USER=lt.USER # Grab user info for file finding
HOST=lt.HOST
REPLAYPATH=lt.REPLAYPATH
UTILPATH=lt.UTILPATH
SCRIPTPATH=lt.SCRIPTPATH
ANATYPE=lt.ANATYPE

################################################################################################################################################

run_type_dir = UTILPATH+"/DB/CUTS/run_type/"

runTypeDict = {

    "fADCdeadtime" : "fADCdeadtime.cuts",
    "coin_heep" : "coin_heep.cuts",
    "hSing_optics" : "hSing_optics.cuts",
    "hSing_prod" : "hSing_prod.cuts",
    "pSing_optics" : "pSing_optics.cuts",
    "pSing_prod" : "pSing_prod.cuts",
    "coinpeak" : "coinpeak.cuts",
    "coin_prod" : "coin_prod.cuts",
    "lumi" : "lumi.cuts",
    "pid_eff" : "pid_eff.cuts",
    "simc_coin_heep" : "simc_coin_heep.cuts",
    "simc_sing_heep" : "simc_sing_heep.cuts",

}

for key, val in runTypeDict:
    print(val)
user_inp =  input('Please enter a run type cut...')
