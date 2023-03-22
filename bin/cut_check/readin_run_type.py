#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-03-22 14:00:53 trottar"
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
general_dir = UTILPATH+"/DB/CUTS/general/"

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

# Matches run type cuts with the general cuts (e.g pid, track, etc.)
generalDict = {
    "pid" : general_dir+"pid.cuts",
    "track" : general_dir+"track.cuts",
    "accept" : general_dir+"accept.cuts",
    "coin_time" : general_dir+"coin_time.cuts",
    "current" : general_dir+"current.cuts",
    "misc" : general_dir+"misc.cuts",
}

for key, val in runTypeDict.items():
    print("{} -> {}".format(key,val))

def readcutname(cut):

    file_content = []
    with open(runTypeDict[cut], "r") as f:
        for line in f:
            if "#" not in line:
                file_content.append(line)
        
    print(" ".join(file_content))

    return file_content

def grabcut(cuts):

    cuts = cuts.split("=")
    cut_name = cuts[0]
    cut_lst = cuts[1].split("+")

    file_content = []
    for cut in cut_lst:
        for key, val in generalDict.items():
            if key in cut:
                cut_key = cut.strip().split(".")[0]
                cut_val = cut.strip().split(".")[1]
                with open(generalDict[cut_key], "r") as f:
                    for line in f:
                        if "#" not in line:
                            if cut_val in line:
                                file_content.append(line.split("=")[1])

    out_cuts = cut_name+" = "+",".join(file_content).replace("\n","")

    print(out_cuts)
    
    return out_cuts
        
user_inp =  input('\n\nPlease enter a run type cut (type exit to end)...')
while True:    

    cut_lst = readcutname(user_inp)

    user_inp =  input('\n\nPlease enter a run type cut (type exit to end)...')

    if user_inp[0:3] == "bye" or user_inp[0:4] == "exit":
        break

    for cut in cut_lst:
        grabcut(cut)
