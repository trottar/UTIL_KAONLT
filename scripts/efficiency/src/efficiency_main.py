#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-03 18:13:50 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import os

import sys, os, time

################################################################################################################################################
'''
User Inputs
'''
ROOTPrefix = sys.argv[1]
runNum = sys.argv[2]
MaxEvent=sys.argv[3]

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

# Add this to all files for more dynamic pathing
USER =  lt.SetPath(os.path.realpath(__file__)).getPath("USER") # Grab user info for file finding
HOST = lt.SetPath(os.path.realpath(__file__)).getPath("HOST")
REPLAYPATH = lt.SetPath(os.path.realpath(__file__)).getPath("REPLAYPATH")
UTILPATH = lt.SetPath(os.path.realpath(__file__)).getPath("UTILPATH")
ANATYPE=lt.SetPath(os.path.realpath(__file__)).getPath("ANATYPE")

################################################################################################################################################

print("Running as %s on %s, hallc_replay_lt path assumed as %s" % (USER, HOST, REPLAYPATH))

timestmp = time.strftime("%Y_%m_%d")

# Output for luminosity table
out_f = UTILPATH+"/scripts/efficiency/OUTPUTS/%s_efficiency_data_%s.csv"  % (ROOTPrefix.replace("replay_",""),timestmp)

################################################################################################################################################
'''
Check that root/output paths and files exist for use
'''

# Construct the name of the rootfile based upon the info we provided
OUTPATH = UTILPATH+"/OUTPUT/Analysis/%sLT" % ANATYPE        # Output folder location
lt.SetPath(os.path.realpath(__file__)).checkDir(OUTPATH)
print("Output path checks out, outputting to %s" % (OUTPATH))

################################################################################################################################################

import efficiency_report
import efficiency_standard_kin

reportDict = efficiency_report.dictionary(UTILPATH,ROOTPrefix,runNum,MaxEvent)
standardDict = efficiency_standard_kin.dictionary(REPLAYPATH,runNum)

################################################################################################################################################

data = {}
for d in (reportDict, standardDict): 
    data.update(d)

eff_data = {i : data[i] for i in sorted(data.keys())}

# Convert merged dictionary to a pandas dataframe then sort it
table  = pd.DataFrame([eff_data], columns=eff_data.keys())
table = table.reindex(sorted(table.columns), axis=1)

file_exists = os.path.isfile(out_f)

# Updates csv file with efficiency values for later analysis (see plot_yield.py)
if file_exists:
    try:
        out_data = pd.read_csv(out_f)
    except IOError:
        print("Error: %s does not appear to exist." % out_f)
    # Checks if run number is alread in csv and replaces it if it is there
    run_index = out_data.index[out_data["Run_Number"] == int(runNum)].tolist()
    out_data.drop(run_index, inplace=True)
    out_data = out_data.append(table,ignore_index=True)
    print("Output efficiency values\n",out_data)
    out_data.to_csv(out_f, index = False, header=True, mode='w+',)
else:
    table.to_csv(out_f, index = False, header=True, mode='a',)            
