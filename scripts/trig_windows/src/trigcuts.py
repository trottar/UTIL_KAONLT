#! /usr/bin/python

#
# Description: Script to dynamically set new trigger windows and update the param file with these values
# ================================================================
# Time-stamp: "2022-10-04 14:14:19 trottar"
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
import matplotlib.pyplot as plt
import sys, math, os, subprocess

################################################################################################################################################
'''
User Inputs
'''

RunType = sys.argv[1]
ROOTPrefix = sys.argv[2]
runNum = sys.argv[3]
MaxEvent=sys.argv[4]

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
'''
Grab prescale values and tracking efficiencies from report file
'''

# Open report file to grab prescale values
report = UTILPATH+"/REPORT_OUTPUT/Analysis/%s/%s_%s_%s.report" % (RunType,ROOTPrefix,runNum,MaxEvent)
f = open(report)
psList = ['SW_Ps1_factor','SW_Ps2_factor','SW_Ps3_factor','SW_Ps4_factor','SW_Ps5_factor','SW_Ps6_factor']
   
# Prescale input value (psValue) to its actual DAQ understanding (psActual)
psActual = [-1,1,2,3,5,9,17,33,65,129,257,513,1025,2049,4097,8193,16385,32769]
psValue = [-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

# Search root file for prescale values, then save as variables
for line in f:
    data = line.split(':')
    for i, obj in enumerate(psList) :
        if (psList[i] in data[0]) : 
            if (i == 0) :  
                ps1_tmp = data[1].strip()
            if (i == 1) : 
                ps2_tmp = data[1].strip()
            if (i == 2) :
                ps3_tmp = data[1].strip()
            if (i == 3) :
                ps4_tmp = data[1].strip()
            if (i == 4) :
                ps5_tmp = data[1].strip()
                if (i == 5) :
                ps6_tmp = data[1].strip()                
try:
    ps1=int(ps1_tmp)
except NameError:
    ps1=-1
try:
    ps2=int(ps2_tmp)
except NameError:
    ps2=-1
try:
    ps3=int(ps3_tmp)
except NameError:
    ps3=-1
try:
    ps4=int(ps4_tmp)
except NameError:
    ps4=-1
try:
    ps5=int(ps5_tmp)
except NameError:
    ps5=-1
try:
    ps6=int(ps6_tmp)
except NameError:
    ps6=-1

# Convert the prescale input values to their actual DAQ values
for i,index in enumerate(psActual):
    #psValue
    if (index == ps1) :
        if(index == -1):
            PS1 = 0
        else:
            PS1 = psActual[i]
    if (index == ps2) :
        if(index == -1):
            PS2 = 0
        else:
            PS2 = psActual[i]            
    if (index == ps3) :
        if(index == -1):
            PS3 = 0
        else:
            PS3 = psActual[i]
    if (index == ps4) :
        if(index == -1):
            PS4 = 0
        else:
            PS4 = psActual[i]            
    if (index == ps5) :
        if(index == -1):
            PS5 = 0
        else:
            PS5 = psActual[i]
    if (index == ps6) :
        if(index == -1):
            PS6 = 0
        else:
            PS6 = psActual[i]            
f.close()

################################################################################################################################################
'''
Define prescale variables
'''

print("\nPre-scale values...\nPS1:{0}, PS2:{1}, PS3:{2}, PS4:{3}, PS5:{4}, PS6:{5}\n".format(PS1,PS2,PS3,PS4,PS5,PS6))

# Save only the used prescale triggers to the PS_used list
PS_list = [["PS1",PS1],["PS2",PS2],["PS3",PS3],["PS4",PS4],["PS5",PS5],["PS6",PS6]]
PS_used = []
for val in PS_list:
    if val[1] != 0:
        PS_used.append(val)

# Check if COIN trigger is used by seeing it was saved in the PS_used list
if len(PS_used) > 2:
    PS_names = [PS_used[0][0],PS_used[1][0],PS_used[2][0]]
    SHMS_PS = PS_used[0][1]
    HMS_PS = PS_used[1][1]
    COIN_PS = PS_used[2][1]
else:
    PS_names = [PS_used[0][0],PS_used[1][0]]
    SHMS_PS = PS_used[0][1]
    HMS_PS = PS_used[1][1]

################################################################################################################################################

print("Running as %s on %s, hallc_replay_lt path assumed as %s" % (USER, HOST, REPLAYPATH))

out_f = UTILPATH+"/scripts/trig_windows/OUTPUTS/trig_data.csv"

################################################################################################################################################
'''
Define and set up cuts
'''

cut_f = '/DB/CUTS/run_type/lumi.cuts'

cuts = ["c_nozero_edtm","c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")]
# Check if COIN trigger is used
if len(PS_used) > 2:
    cuts = ["c_nozero_edtm","c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS",""),"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")]

lt=Root(os.path.realpath(__file__),"Lumi",ROOTPrefix,runNum,MaxEvent,cut_f,cuts)

proc_root = lt.setup_ana()
c = proc_root[0] # Cut object
tree = proc_root[1] # Dictionary of branches
strDict = proc_root[2] # Dictionary of cuts as strings

################################################################################################################################################

T_coin_pTRIG_SHMS_ROC1_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC1_tdcTimeRaw" % PS_names[0].replace("PS","")]
T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC2_tdcTimeRaw" % PS_names[0].replace("PS","")]
T_coin_pTRIG_SHMS_ROC1_tdcTime = tree["T_coin_pTRIG%s_ROC1_tdcTime" % PS_names[0].replace("PS","")]
T_coin_pTRIG_SHMS_ROC2_tdcTime = tree["T_coin_pTRIG%s_ROC2_tdcTime" % PS_names[0].replace("PS","")]

T_coin_pTRIG_HMS_ROC1_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC1_tdcTimeRaw" % PS_names[1].replace("PS","")]
T_coin_pTRIG_HMS_ROC2_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC2_tdcTimeRaw" % PS_names[1].replace("PS","")]
T_coin_pTRIG_HMS_ROC1_tdcTime = tree["T_coin_pTRIG%s_ROC1_tdcTime" % PS_names[1].replace("PS","")]
T_coin_pTRIG_HMS_ROC2_tdcTime = tree["T_coin_pTRIG%s_ROC2_tdcTime" % PS_names[1].replace("PS","")]

# Check if COIN trigger is used
if len(PS_used) > 2:
    T_coin_pTRIG_COIN_ROC1_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC1_tdcTimeRaw" % PS_names[2].replace("PS","")]
    T_coin_pTRIG_COIN_ROC2_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC2_tdcTimeRaw" % PS_names[2].replace("PS","")]
    T_coin_pTRIG_COIN_ROC1_tdcTime = tree["T_coin_pTRIG%s_ROC1_tdcTime" % PS_names[2].replace("PS","")]
    T_coin_pTRIG_COIN_ROC2_tdcTime = tree["T_coin_pTRIG%s_ROC2_tdcTime" % PS_names[2].replace("PS","")]

T_coin_pEDTM_tdcTimeRaw = tree["T_coin_pEDTM_tdcTimeRaw"]
T_coin_pEDTM_tdcTime = tree["T_coin_pEDTM_tdcTime"]

################################################################################################################################################
'''
Grabs the misc param file so it can be updated with trigger windows
'''

# Read in the Misc_Parameters.csv cut parameter file which has the trigger window information
inp_f = UTILPATH+'/DB/PARAM/Misc_Parameters.csv'
try:
    trig_data = pd.read_csv(inp_f)
    print(trig_data.keys())
except IOError:
    print("Error: %s does not appear to exist." % inp_f)
    sys.exit(0)

################################################################################################################################################

def setWindows(runNum):
    '''
    Set the trigger windows by...

    1) Finding the number of events per bin
    2) Based off the threshold for the number of events, the min and max windows are set.  
    '''

    def getBinEdges(branch,cut,numbins,window):
        # Calculate the geometric mean
        def geo_mean(inp):
            l_inp = np.log(inp[inp != 0])
            return np.exp(l_inp.mean())
        # finds the number of events per bin (the zero events are cut out beforehand)
        counts, bins = np.histogram(c.add_cut(branch,cut),bins=numbins)
        # Set the threshold for the number of events an order of magnitude more than the geometric mean
        #thres_count = geo_mean(counts)*10
        # Get maximum number of counts
        thres_count = max(counts)
        # Finding the bins that are above the set threshold for the number of events
        #binVals = [b for c,b in zip(counts,bins) if c > thres_count]
        # Get bin with peak value
        peak = [bins[i] for i,val in enumerate(counts) if thres_count == val][0]
        # Define window around peak
        binVals = [val for i,val in enumerate(bins) if peak-window < val < peak+window]
        # Set min and max windows
        minBin = min(binVals)
        maxBin = max(binVals)
        return [minBin, maxBin]

    numbins = 200
    window = 300
    # Get windows for {SPEC}_ROC1_tdcTimeRaw and pEDTM_tdcTimeRaw
    c_T_coin_pTRIG_HMS_ROC1_tdcTimeRaw = getBinEdges(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),numbins,window)
    c_T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw = getBinEdges(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS",""),numbins,window)
    # Check if COIN trigger is used
    if len(PS_used) > 2:
        c_T_coin_pTRIG_HMS_ROC1_tdcTimeRaw = getBinEdges(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),numbins,window)
        c_T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw = getBinEdges(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS",""),numbins,window)
        c_T_coin_pTRIG_COIN_ROC1_tdcTimeRaw = getBinEdges(T_coin_pTRIG_COIN_ROC1_tdcTimeRaw,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS",""),numbins,window)
    c_T_coin_pEDTM_tdcTimeRaw = getBinEdges(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm",numbins,window)

    window = 50
    # This will need to run twice as it will need (or at least I'd prefer) to have the time raw window cut on time.
    # In theory just using time raw > 0 cut should suffice
    # Get windows for {SPEC}_ROC1_tdcTime and pEDTM_tdcTime
    c_T_coin_pTRIG_HMS_ROC1_tdcTime = getBinEdges(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),numbins,window)
    c_T_coin_pTRIG_SHMS_ROC2_tdcTime = getBinEdges(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS",""),numbins,window)
    # Check if COIN trigger is used
    if len(PS_used) > 2:
        c_T_coin_pTRIG_COIN_ROC1_tdcTime = getBinEdges(T_coin_pTRIG_COIN_ROC1_tdcTime,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS",""),numbins,window)
    c_T_coin_pEDTM_tdcTime = getBinEdges(T_coin_pEDTM_tdcTime,"c_nozero_edtm",numbins,window)

    # Create a dictionary that contains the information that will be uploaded to Misc_Parameters.csv for a particular run
    new_row = {'Run_Start' : "{:.0f}".format(float(runNum)), 'Run_End' : "{:.0f}".format(float(runNum)), 'noedtm' : 0.0, 'edtmLow' : "{:.0f}".format(float(c_T_coin_pEDTM_tdcTimeRaw[0])), 
               'edtmHigh' : "{:.0f}".format(float(c_T_coin_pEDTM_tdcTimeRaw[1])),'ptrigHMSLow' : "{:.0f}".format(float(c_T_coin_pTRIG_HMS_ROC1_tdcTimeRaw[0])), 
               'ptrigHMSHigh' : "{:.0f}".format(float(c_T_coin_pTRIG_HMS_ROC1_tdcTimeRaw[1])),'ptrigSHMSLow' : "{:.0f}".format(float(c_T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw[0])), 
               'ptrigSHMSHigh' : "{:.0f}".format(float(c_T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw[1])),'ptrigCOINLow' : 0.0, 'ptrigCOINHigh' : 10000.0, 'goodstarttime' : 1.0, 'goodscinhit' : 1.0}
    # Check if COIN trigger is used
    if len(PS_used) > 2:
        # Create a dictionary that contains the information that will be uploaded to Misc_Parameters.csv for a particular run
        new_row =  {'Run_Start' : "{:.0f}".format(float(runNum)), 'Run_End' : "{:.0f}".format(float(runNum)), 'noedtm' : 0.0, 'edtmLow' : "{:.0f}".format(float(c_T_coin_pEDTM_tdcTimeRaw[0])), 
                    'edtmHigh' : "{:.0f}".format(float(c_T_coin_pEDTM_tdcTimeRaw[1])),'ptrigHMSLow' : "{:.0f}".format(float(c_T_coin_pTRIG_HMS_ROC1_tdcTimeRaw[0])), 
                    'ptrigHMSHigh' : "{:.0f}".format(float(c_T_coin_pTRIG_HMS_ROC1_tdcTimeRaw[1])),'ptrigSHMSLow' : "{:.0f}".format(float(c_T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw[0])), 
                    'ptrigSHMSHigh' : "{:.0f}".format(float(c_T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw[1])),'ptrigCOINLow' : "{:.0f}".format(float(c_T_coin_pTRIG_COIN_ROC1_tdcTimeRaw[0])), 
                    'ptrigCOINHigh' : "{:.0f}".format(float(c_T_coin_pTRIG_COIN_ROC1_tdcTimeRaw[1])),'goodstarttime' : 1.0, 'goodscinhit' : 1.0}

    return new_row

################################################################################################################################################

def reconParam(runNum):
    '''
    Reconstruct /DB/PARAM/Misc_Parameters.csv with new window values
    '''
    # Get new windows and set up row to be added to Misc_Parameters.csv
    new_row = setWindows(runNum)

    global trig_data
    print("\nRemoving...\n",trig_data[(trig_data["Run_Start"] <= int(runNum)) & (trig_data["Run_End"] >= int(runNum))],"\n") 

    # Checking if run number is in a row already
    run_row = trig_data[(trig_data["Run_Start"] <= int(runNum)) & (trig_data["Run_End"] >= int(runNum))]

    # Removing row with this run number argument
    run_index = trig_data.index[(trig_data["Run_Start"] <= int(runNum)) & (trig_data["Run_End"] >= int(runNum))].tolist()
    trig_data.drop(run_index, inplace=True)

    # Setting an open window row that will be added to the end of Misc_Parameters.csv. This ensures that the script will run in the future without errors. 
    # This row will not overwrite the windows that are set above
    open_row = {'Run_Start' : 0, 'Run_End' : 99999, 'noedtm' : 0.0, 'edtmLow' : 0.0, 'edtmHigh' : 10000.0, 'ptrigHMSLow' : 0.0, 'ptrigHMSHigh' : 10000.0, 
                'ptrigSHMSLow' : 0.0, 'ptrigSHMSHigh' : 10000.0, 'ptrigCOINLow' : 0.0, 'ptrigCOINHigh' : 10000.0, 'goodstarttime' : 1.0, 'goodscinhit' : 1.0}

    # Add in newly formed rows to dataframe
    trig_data = trig_data.append(new_row,ignore_index=True)
    trig_data = trig_data.append(open_row,ignore_index=True)

    # Update csv with new version of dataframe
    trig_data.to_csv(inp_f, index=False, header=True, mode='w+',)

    print("\n\nNew version of Misc_Parameters.csv...\n",trig_data)
    return trig_data      

################################################################################################################################################

def main():

    reconParam(runNum)

if __name__ == '__main__': main()
