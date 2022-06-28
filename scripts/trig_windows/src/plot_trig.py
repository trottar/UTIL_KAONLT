#! /usr/bin/python

#
# Description: Script for plotting trigger windows
# ================================================================
# Time-stamp: "2022-06-28 01:36:04 trottar"
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

RunType = sys.argv[1]
ROOTPrefix = sys.argv[2]
runNum = sys.argv[3]
MaxEvent=sys.argv[4]

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

p=lt.SetPath(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
USER=p.getPath("USER") # Grab user info for file finding
HOST=p.getPath("HOST")
REPLAYPATH=p.getPath("REPLAYPATH")
UTILPATH=p.getPath("UTILPATH")
ANATYPE=p.getPath("ANATYPE")

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
    current_data = line.split(':')
    if ('SW_BCM4A_Beam_Cut_Current' in current_data[0]):
        report_current = current_data[1].split("+-")
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
ps1=int(ps1_tmp)
ps2=int(ps2_tmp)
ps3=int(ps3_tmp)
ps4=int(ps4_tmp)
ps5=int(ps5_tmp)
ps6=int(ps6_tmp)

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
'''
Define and set up cuts
'''

cut_f = '/DB/CUTS/run_type/lumi.cuts'

cuts = ["c_nozero_edtm","c_noedtm","c_edtm","c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),"c_ptrigHMS%s" % PS_names[1].replace("PS",""),"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS",""),"c_ptrigSHMS%s" % PS_names[0].replace("PS",""),"c_curr"]
# Check if COIN trigger is used
if len(PS_used) > 2:
    cuts = ["c_nozero_edtm","c_noedtm","c_edtm","c_nozero_ptrigHMS%s" % PS_names[1].replace("PS",""),"c_ptrigHMS%s" % PS_names[1].replace("PS",""),"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS",""),"c_ptrigSHMS%s" % PS_names[0].replace("PS",""),"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS",""),"c_ptrigCOIN%s" % PS_names[2].replace("PS",""),"c_curr"]

proc_root = lt.Root(os.path.realpath(__file__),"Lumi",ROOTPrefix,runNum,MaxEvent,cut_f,cuts).setup_ana()
c = proc_root[0] # Cut object
tree = proc_root[1] # Dictionary of branches
OUTPATH = proc_root[2] # Get pathing for OUTPATH

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
H_bcm_bcm1_AvgCurrent = tree["H_bcm_bcm1_AvgCurrent"]

################################################################################################################################################

print("Running as %s on %s, hallc_replay_lt path assumed as %s" % (USER, HOST, REPLAYPATH))

################################################################################################################################################

def trig_Plots():
    '''
    Plots of the triggers with and without the window cuts
    '''

    f = plt.figure(figsize=(11.69,8.27))

    # Check if COIN trigger is used
    if len(PS_used) > 2:

        ax = f.add_subplot(241)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_HMS_ROC1_tdcTimeRaw')
        plt.ylabel('Count')
        
        ax = f.add_subplot(242)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw')
        plt.ylabel('Count')

        plt.title("Run %s" % runNum)

        ax = f.add_subplot(243)
        ax.hist(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTimeRaw,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTimeRaw,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTimeRaw,"c_ptrigCOIN%s" % PS_names[2].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTimeRaw,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_COIN_ROC1_tdcTimeRaw')
        plt.ylabel('Count')

        ax = f.add_subplot(244)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm"),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm"),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pEDTM_tdcTimeRaw')
        plt.ylabel('Count')
        
        ax = f.add_subplot(245)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_HMS_ROC1_tdcTime')
        plt.ylabel('Count')

        ax = f.add_subplot(246)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_SHMS_ROC2_tdcTime')
        plt.ylabel('Count')

        ax = f.add_subplot(247)
        ax.hist(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTime,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTime,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTime,"c_ptrigCOIN%s" % PS_names[2].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_COIN_ROC1_tdcTime,"c_nozero_ptrigCOIN%s" % PS_names[2].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_COIN_ROC1_tdcTime')
        plt.ylabel('Count')

        ax = f.add_subplot(248)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTime,"c_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTime,"c_nozero_edtm"),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTime,"c_nozero_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTime,"c_nozero_edtm"),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pEDTM_tdcTime')
        plt.ylabel('Count')

    else:

        ax = f.add_subplot(231)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTimeRaw,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_HMS_ROC1_tdcTimeRaw')
        plt.ylabel('Count')

        ax = f.add_subplot(232)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw')
        plt.ylabel('Count')

        plt.title("Run %s" % runNum)

        ax = f.add_subplot(233)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm"),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTimeRaw,"c_nozero_edtm"),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pEDTM_tdcTimeRaw')
        plt.ylabel('Count')
        
        ax = f.add_subplot(234)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_ptrigHMS%s" % PS_names[1].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_HMS_ROC1_tdcTime,"c_nozero_ptrigHMS%s" % PS_names[1].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_HMS_ROC1_tdcTime')
        plt.ylabel('Count')

        ax = f.add_subplot(235)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_ptrigSHMS%s" % PS_names[0].replace("PS","")),bins=c.setbin(c.add_cut(T_coin_pTRIG_SHMS_ROC2_tdcTime,"c_nozero_ptrigSHMS%s" % PS_names[0].replace("PS","")),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pTRIG_SHMS_ROC2_tdcTime')
        plt.ylabel('Count')

        ax = f.add_subplot(236)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTime,"c_nozero_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTime,"c_nozero_edtm"),200),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        ax.hist(c.add_cut(T_coin_pEDTM_tdcTime,"c_edtm"),bins=c.setbin(c.add_cut(T_coin_pEDTM_tdcTime,"c_nozero_edtm"),200),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
        plt.yscale('log')
        plt.xlabel('T_coin_pEDTM_tdcTime')
        plt.ylabel('Count')

        plt.legend(loc="upper right")
        
    plt.tight_layout()      
    plt.savefig(UTILPATH+'/scripts/trig_windows/OUTPUTS/trig_%s_%s.png' % (ROOTPrefix,runNum))     # Input file location and variables taking)

def currentPlots():
    '''
    Plots of the currents with and without cuts
    '''

    f = plt.figure(figsize=(11.69,8.27))

    ax = f.add_subplot(111)
    ax.hist(c.add_cut(H_bcm_bcm1_AvgCurrent,"c_curr"),bins=c.setbin(H_bcm_bcm1_AvgCurrent,10),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
    ax.hist(H_bcm_bcm1_AvgCurrent,bins=c.setbin(H_bcm_bcm1_AvgCurrent,10),label='no cut',histtype='step', alpha=0.5, stacked=True, fill=True)
    plt.yscale('log')
    plt.xlabel('H_bcm_bcm1_AvgCurrent')
    plt.ylabel('Count')
    plt.title("Run %s, %s" % (runNum,report_current))

    plt.savefig(UTILPATH+'/scripts/trig_windows/OUTPUTS/curr_%s_%s.png' % (ROOTPrefix,runNum))     # Input file location and variables taking)

################################################################################################################################################

def main():

    trig_Plots()
    currentPlots()
    plt.show()

if __name__ == '__main__': main()
