#! /usr/bin/python

#
# Description: Script for plotting trigger windows
# ================================================================
# Time-stamp: "2022-10-28 14:01:24 trottar"
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
psList = ['KLT_Ps1_factor','KLT_Ps2_factor','KLT_Ps3_factor','KLT_Ps4_factor','KLT_Ps5_factor','KLT_Ps6_factor']
    
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

PS_list = [["PS1",PS1],["PS2",PS2],["PS3",PS3],["PS4",PS4],["PS5",PS5],["PS6",PS6]]
PS_names = []
for val in PS_list:
    if val[0] == "PS1" or val[0] == "PS2":        
        if val[1] != 0:
            SHMS_PS = val[1]
            PS_names.append(val[0])    
    if val[0] == "PS3" or val[0] == "PS4":        
        if val[1] != 0:
            HMS_PS = val[1] 
            PS_names.append(val[0])
    if val[0] == "PS5" or val[0] == "PS6":        
        if val[1] != 0:
            COIN_PS = val[1]
            PS_names.append(val[0])

try:
    SHMS_PS
except NameError:
    SHMS_PS = None

try:
    HMS_PS
except NameError:
    HMS_PS = None

try:
    COIN_PS
except NameError:
    COIN_PS = None

################################################################################################################################################
'''
Define and set up cuts
'''

cut_f = '/DB/CUTS/run_type/lumi.cuts'

cuts = ["c_nozero_edtm"]

for ps in PS_names:
    if ps == "PS1" or ps == "PS2":
        cuts+=["c_nozero_ptrigSHMS%s" % ps.replace("PS",""),"c_ptrigSHMS%s" % ps.replace("PS","")]        
    if ps == "PS3" or ps == "PS4":
        cuts+=["c_nozero_ptrigHMS%s" % ps.replace("PS",""),"c_ptrigHMS%s" % ps.replace("PS","")]
    if ps == "PS5" or ps == "PS6":
        cuts+=["c_nozero_ptrigCOIN%s" % ps.replace("PS",""),"c_ptrigCOIN%s" % ps.replace("PS","")]    

lt=Root(os.path.realpath(__file__),"Lumi",ROOTPrefix,runNum,MaxEvent,cut_f,cuts)

proc_root = lt.setup_ana()
c = proc_root[0] # Cut object
tree = proc_root[1] # Dictionary of branches
strDict = proc_root[2] # Dictionary of cuts as strings

for key,val in strDict.items():
    if key == "c_curr":
        global thres_curr, report_current
        # e.g. Grabbing threshold current (ie 2.5) from something like this [' {"H_bcm_bcm1_AvgCurrent" : (abs(H_bcm_bcm1_AvgCurrent-55) < 2.5)}']
        thres_curr = float(val[0].split(":")[1].split("<")[1].split(")")[0].strip())
        # e.g. Grabbing set current for run (ie 55) from something like this [' {"H_bcm_bcm1_AvgCurrent" : (abs(H_bcm_bcm1_AvgCurrent-55) < 2.5)}']
        report_current = float(val[0].split(":")[1].split("<")[0].split(")")[0].split("-")[1].strip())

################################################################################################################################################

for ps in PS_names:
    if ps == "PS1" or ps == "PS2":
        T_coin_pTRIG_SHMS_ROC1_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC1_tdcTimeRaw" % ps.replace("PS","")]
        T_coin_pTRIG_SHMS_ROC2_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC2_tdcTimeRaw" % ps.replace("PS","")]
        T_coin_pTRIG_SHMS_ROC1_tdcTime = tree["T_coin_pTRIG%s_ROC1_tdcTime" % ps.replace("PS","")]
        T_coin_pTRIG_SHMS_ROC2_tdcTime = tree["T_coin_pTRIG%s_ROC2_tdcTime" % ps.replace("PS","")]
        
    if ps == "PS3" or ps == "PS4":
        T_coin_pTRIG_HMS_ROC1_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC1_tdcTimeRaw" % ps.replace("PS","")]
        T_coin_pTRIG_HMS_ROC2_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC2_tdcTimeRaw" % ps.replace("PS","")]
        T_coin_pTRIG_HMS_ROC1_tdcTime = tree["T_coin_pTRIG%s_ROC1_tdcTime" % ps.replace("PS","")]
        T_coin_pTRIG_HMS_ROC2_tdcTime = tree["T_coin_pTRIG%s_ROC2_tdcTime" % ps.replace("PS","")]
        
    if ps == "PS5" or ps == "PS6":
        T_coin_pTRIG_COIN_ROC1_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC1_tdcTimeRaw" % ps.replace("PS","")]
        T_coin_pTRIG_COIN_ROC2_tdcTimeRaw = tree["T_coin_pTRIG%s_ROC2_tdcTimeRaw" % ps.replace("PS","")]
        T_coin_pTRIG_COIN_ROC1_tdcTime = tree["T_coin_pTRIG%s_ROC1_tdcTime" % ps.replace("PS","")]
        T_coin_pTRIG_COIN_ROC2_tdcTime = tree["T_coin_pTRIG%s_ROC2_tdcTime" % ps.replace("PS","")]

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
    ax.hist(c.add_cut(H_bcm_bcm1_AvgCurrent,"c_curr"),bins=c.setbin(c.add_cut(H_bcm_bcm1_AvgCurrent,"c_curr"),10),label='cut',histtype='step', alpha=0.5, stacked=True, fill=True)
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
