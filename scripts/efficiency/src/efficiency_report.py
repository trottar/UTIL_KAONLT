#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-05-25 12:09:52 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import uproot as up
import numpy as np
import pandas as pd
import scipy
import scipy.integrate as integrate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys, math, os, subprocess

################################################################################################################################################
'''
User Inputs
'''

runType = sys.argv[1]
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

# Output for luminosity table
out_f = UTILPATH+"/scripts/efficiency/OUTPUTS/efficiency_data.csv"

################################################################################################################################################
'''
Check that root/output paths and files exist for use
'''

# Construct the name of the rootfile based upon the info we provided
OUTPATH = UTILPATH+"/OUTPUT/Analysis/%sLT" % ANATYPE        # Output folder location
lt.SetPath(os.path.realpath(__file__)).checkDir(OUTPATH)
print("Output path checks out, outputting to %s" % (OUTPATH))

################################################################################################################################################
'''
Grab prescale values and tracking efficiencies from report file
'''

# Open report file to grab prescale values and tracking efficiency
report = UTILPATH+"/REPORT_OUTPUT/Analysis/%s/%s_%s_%s.report" % (runType,ROOTPrefix,runNum,MaxEvent)
f = open(report)
psList = ['SW_Ps1_factor','SW_Ps2_factor','SW_Ps3_factor','SW_Ps4_factor','SW_Ps5_factor','SW_Ps6_factor']

effDict = {

    'Run_Number': None,
    'BCM1_Charge': None,
    'BCM1_Beam_Cut_Charge': None,
    'BCM1_Current': None,
    'BCM1_Beam_Cut_Current': None,
    #'beam on time': None,
    #'time of run': None,
    'SHMS_Run_Length': None,
    'HMS_Run_Length': None,
    'Ps1_factor': None,
    'Ps2_factor': None,
    'Ps3_factor': None,
    'Ps4_factor': None,
    'Ps5_factor': None,
    'Ps6_factor': None,
    'Total_SHMS_3/4_Triggers': None,
    '(current_cut)_Total_SHMS_3/4_Triggers': None ,
    'Pre-Scaled_SHMS_3/4_Triggers': None ,
    'Accepted_SHMS_Triggers': None ,
    'Total_HMS_EL-REAL_Triggers': None,
    '(current_cut)_Total_HMS_EL-REAL_Triggers': None ,
    'Pre-Scaled_HMS_EL-REAL_Triggers': None ,
    'Accepted_HMS_Triggers': None ,
    'Total_COIN_Triggers': None,
    '(current_cut)_Total_COIN_Triggers': None ,
    'Pre-Scaled_COIN_Triggers': None ,
    'Accepted_COIN_Triggers': None ,
    'EDTM_Accepted_Triggers': None ,    
    'SHMS_Hodoscope_S1X_Rate': None,
    'HMS_EL-REAL_Trigger_Rate': None,
    'SHMS_Hodoscope_S1X_Rate': None,
    'SHMS_3/4_Trigger_Rate': None,
    'COIN_Trigger_Rate': None,
    #'CPULT': None,
    #'CPULT Error': None,
    'Scaler_EDTM_Live_Time': None,
    'Scaler_EDTM_Live_Time_ERROR': None,
    'Non_Scaler_EDTM_Live_Time': None,
    'Non_Scaler_EDTM_Live_Time_ERROR': None,
    #'eLT': None,
    #'eLT error': None,
    'SHMS_Hodo_3_of_4_EFF': None,
    #'SHMS Hodo efficiencies error': None,
    'SHMS_Hodo_4_of_4_EFF': None,
    #'SHMS Hodo efficiencies error': None,
    'HMS_Hodo_3_of_4_EFF': None,
    #'HMS Hodo efficiencies error': None,
    'HMS_Hodo_4_of_4_EFF': None,
    #'HMS Hodo efficiencies error': None,
    'HMS_Cer_Elec_Eff': None,
    'HMS_Cer_Elec_Eff_ERROR': None,
    'SHMS_Aero_Pion_Eff': None,
    'SHMS_Aero_Pion_Eff_ERROR': None,
    'SHMS_HGC_Pion_Eff': None,
    'SHMS_HGC_Pion_Eff_ERROR': None,
    #'Cointime blocking efficiency': None,
    #'cointime blocking efficiency error': None,
    #'beta tracking efficiency': None,
    #'beta tracking efficiency error': None,
    'HMS_Electron_Singles_TRACK_EFF': None,
    'HMS_Electron_Singles_TRACK_EFF_ERROR': None,
    'SHMS_Pion_Singles_TRACK_EFF': None,
    'SHMS_Pion_Singles_TRACK_EFF_ERROR': None,
    'SHMS_Prot_Singles_TRACK_EFF': None,
    'SHMS_Prot_Singles_TRACK_EFF_ERROR': None,
    'SHMS_Hadron_Singles_TRACK_EFF': None,
    'SHMS_Hadron_Singles_TRACK_EFF_ERROR': None,
    #'coin tracking efficiencies': None,
    #'coin tracking efficiencies error': None,
    'Target_Mass_(amu)': None ,
    #'X positions': None,
    #'x variance': None,
    #'y positions': None,
    #'y variance': None ,
    
}

# Prescale input value (psValue) to its actual DAQ understanding (psActual)
# !!!!!!!!!!! Convert to dictionary
psActual = [-1,1,2,3,5,9,17,33,65,129,257,513,1025,2049,4097,8193,16385,32769]
psValue = [-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

# Search root file for prescale values and tracking efficiency, then save as variables
for line in f:
    data = line.split(':')
    for k,v in effDict:
        if key in data[0]:
            effDict[key] = data[1].split("+-")
print(effDict)


# !!!! Temporary, this will be imported in collection script once other scripts are developed.
eff_data = {i : effDict[i] for i in sorted(effDict.keys())}

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
    run_index = out_data.index[out_data["run number"] == int(runNum)].tolist()
    out_data.drop(run_index, inplace=True)
    out_data = out_data.append(table,ignore_index=True)
    print("Output efficiency values\n",out_data)
    out_data.to_csv(out_f, index = False, header=True, mode='w+',)
else:
    table.to_csv(out_f, index = False, header=True, mode='a',)            
