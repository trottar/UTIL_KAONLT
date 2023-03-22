#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-03-22 13:20:31 trottar"
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

    "fADCdeadtime" : run_type_dir+"fADCdeadtime.cuts",
    "coin_heep" : run_type_dir+"coin_heep.cuts",
    "hSing_optics" : run_type_dir+"hSing_optics.cuts",
    "hSing_prod" : run_type_dir+"hSing_prod.cuts",
    "pSing_optics" : run_type_dir+"pSing_optics.cuts",
    "pSing_prod" : run_type_dir+"pSing_prod.cuts",
    "coinpeak" : run_type_dir+"coinpeak.cuts",
    "coin_prod" : run_type_dir+"coin_prod.cuts",
    "lumi" : run_type_dir+"lumi.cuts",
    "pid_eff" : run_type_dir+"pid_eff.cuts",
    "simc_coin_heep" : run_type_dir+"simc_coin_heep.cuts",
    "simc_sing_heep" : run_type_dir+"simc_sing_heep.cuts",

}

for key, val in runTypeDict.items():
    print("{} -> {}".format(key,val))

def readcuts(cut):

    with open(runTypeDict[cut], "r") as f:
        print(f)
        
while True:    
    user_inp =  input('Please enter a run type cut (type exit to end)...')

    if user_inp[0:3] == "exit":
        break
