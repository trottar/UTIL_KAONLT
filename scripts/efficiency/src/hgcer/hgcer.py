#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-15 17:56:48 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

# Oct 11, 2020 Vijay Kumar, University of Regina

# A short python demo script demonstrating opening up a root file, using uproot to grab some info and then save it as a new rootfile
# This time, we also define and apply some cuts to our SHMS events

# Import relevant packages
import uproot as up
import numpy as np
import root_numpy as rnp
import pandas as pd
import root_pandas as rpd
import ROOT
import scipy
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import sys, math, os, subprocess

# Check the number of arguments provided to the script
if len(sys.argv)-1!=2:
    print("!!!!! ERROR !!!!!\n Expected 3 arguments\n Usage is with - ROOTfilePrefix RunNumber MaxEvents \n!!!!! ERROR !!!!!")
    sys.exit(1)

# Input params - run number and max number of events
#ROOTPrefix = sys.argv[1]
ROOTPrefix = "Kaon_coin_replay_production"
runNum = sys.argv[1]
MaxEvent = sys.argv[2]

# Import package for cuts
import ltsep as lt 

##############################################################################################################################################
'''
Define and set up cuts
'''

fout = '/DB/CUTS/run_type/pid_eff.cuts'

# defining Cuts
cuts = ["p_picut_eff","p_picut_eff_no_hgcer","p_picut_eff_no_aero","p_picut_eff_no_cal","p_ecut_eff_no_hgcer","p_ecut_eff","p_kcut_eff","p_kcut_eff_no_hgcer","p_pcut_eff","p_pcut_eff_no_hgcer","p_cut_eff_no_cal_hgcer","p_cut_eff_no_hgcer_aero_cal"]

proc_root = lt.Root(os.path.realpath(__file__),"KaonLT_hgcer",ROOTPrefix,runNum,MaxEvent,fout,cuts).setup_ana()
c = proc_root[0] # Cut object
b = proc_root[1] # Dictionary of branches
p = proc_root[2] # Dictionary of pathing variables
OUTPATH = proc_root[3] # Get pathing for OUTPATH

# Add this to all files for more dynamic pathing
USER =  p["USER"] # Grab user info for file finding
HOST = p["HOST"]
REPLAYPATH = p["REPLAYPATH"]
UTILPATH = p["UTILPATH"]
ANATYPE=p["ANATYPE"]

print("Running as %s on %s, hallc_replay_lt path assumed as %s" % (USER, HOST, REPLAYPATH))
# Construct the name of the rootfile based upon the info we provided
rootName = "%s/%s_%s_%s.root" % (OUTPATH, ROOTPrefix, runNum, MaxEvent)

# Define a function to return a dictionary of the events we want
# Arrays we generate in our dict should all be of the same length (in terms of # elements in the array) to keep things simple
def SHMS_events(): 

    NoCut_Events_SHMS = [b["CTime_eKCoinTime_ROC1"], b["CTime_ePiCoinTime_ROC1"], b["CTime_epCoinTime_ROC1"], b["H_cal_etotnorm"], b["P_gtr_beta"], b["P_gtr_xp"], b["P_gtr_yp"], b["P_gtr_p"], b["P_gtr_dp"], b["P_cal_etotnorm"], b["P_aero_npeSum"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"],  b["P_aero_xAtCer"], b["P_aero_yAtCer"], b["P_cal_fly_earray"], b["P_cal_pr_eplane"], b["P_gtr_x"], b["P_gtr_y"], b["emiss"], b["pmiss"]]
    SHMS_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*NoCut_Events_SHMS)]

    # Create (currently empty) arrays of our SHMS events for Cut1 and Cut2, we also have a temp array of our uncut data
    Cut_Events_SHMS_tmp = NoCut_Events_SHMS
    Pion_Cut_wHGC_Events = []
    Pion_Cut_noHGC_Events = []
    Positron_Cut_wHGC_Events = []
    Positron_Cut_noHGC_Events = []
    Pion_Aero_Cut_noAero_Events = []
    Pion_Cal_Cut_noCal_Events = []
    Kaon_Cut_wHGC_Events = []
    Kaon_Cut_noHGC_Events = []
    P_Cut_wHGC_Events = []
    P_Cut_noHGC_Events = []
    P_Cut_no_Cal_HGC_Events = []
    P_Cut_no_Cal_HGC_Aero_Events = []

    #Apply our cuts to the data and save our new arrays
    for arr in   Cut_Events_SHMS_tmp:
        Pion_Cut_wHGC_Events.append(c.add_cut(arr, "p_picut_eff"))
        Pion_Cut_noHGC_Events.append(c.add_cut(arr, "p_picut_eff_no_hgcer"))
        Positron_Cut_wHGC_Events.append(c.add_cut(arr, "p_ecut_eff"))
        Positron_Cut_noHGC_Events.append(c.add_cut(arr, "p_ecut_eff_no_hgcer"))
        Pion_Aero_Cut_noAero_Events.append(c.add_cut(arr, "p_picut_eff_no_aero"))
        Pion_Cal_Cut_noCal_Events.append(c.add_cut(arr, "p_picut_eff_no_cal"))
        Kaon_Cut_wHGC_Events.append(c.add_cut(arr, "p_kcut_eff"))
        Kaon_Cut_noHGC_Events.append(c.add_cut(arr, "p_kcut_eff_no_hgcer"))
        P_Cut_wHGC_Events.append(c.add_cut(arr, "p_pcut_eff"))
        P_Cut_noHGC_Events.append(c.add_cut(arr, "p_pcut_eff_no_hgcer"))
        P_Cut_no_Cal_HGC_Events.append(c.add_cut(arr, "p_cut_eff_no_cal_hgcer"))
        P_Cut_no_Cal_HGC_Aero_Events.append(c.add_cut(arr, "p_cut_eff_no_hgcer_aero_cal"))

        
        # Again, strictly force this to be an array and NOT a list
    Pion_Cut_wHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Pion_Cut_wHGC_Events)]
    Pion_Cut_noHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Pion_Cut_noHGC_Events)]
    Positron_Cut_wHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Positron_Cut_wHGC_Events)]
    Positron_Cut_noHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Positron_Cut_noHGC_Events)]
    Pion_Aero_Cut_noAero_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Pion_Aero_Cut_noAero_Events)]
    Pion_Cal_Cut_noCal_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Pion_Cal_Cut_noCal_Events)]
    Kaon_Cut_wHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Kaon_Cut_wHGC_Events)]
    Kaon_Cut_noHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*Kaon_Cut_noHGC_Events)]
    P_Cut_wHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*P_Cut_wHGC_Events)]
    P_Cut_noHGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*P_Cut_noHGC_Events)]
    P_Cut_no_Cal_HGC_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*P_Cut_no_Cal_HGC_Events)]
    P_Cut_no_Cal_HGC_Aero_Events_Info = [(CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) for (CTeK, CTePi, CTeP, HCal, PBeta, Pxp, Pyp, PP, PDel, Ptot, Paernpe, Phgnpe, Pxat, Pyat, Paeroxat, Paeroyat, Pfly, Ppr, Pxtr, Pytr, Pemiss, Ppmiss) in zip(*P_Cut_no_Cal_HGC_Aero_Events)]
    SHMS_Events = {
        "SHMS_Events": SHMS_Events_Info,
        "SHMS_Pions": Pion_Cut_wHGC_Events_Info,
        "SHMS_Positrons_Without_HGC_Cuts": Positron_Cut_noHGC_Events_Info,
        "SHMS_Positrons": Positron_Cut_wHGC_Events_Info,
        "SHMS_Pions_Without_HGC_Cuts": Pion_Cut_noHGC_Events_Info,
        "SHMS_Pions_Aero_Without_Aero_Cuts": Pion_Aero_Cut_noAero_Events_Info,
        "SHMS_Pions_Cal_Without_Cal_Cuts": Pion_Cal_Cut_noCal_Events_Info,
        "SHMS_Kaons": Kaon_Cut_wHGC_Events_Info,
        "SHMS_Kaons_Without_HGC_Cuts": Kaon_Cut_noHGC_Events_Info,
        "SHMS_Protons": P_Cut_wHGC_Events_Info,
        "SHMS_Protons_Without_HGC_Cuts": P_Cut_noHGC_Events_Info,
        "SHMS_cut_no_Cal_HGC": P_Cut_no_Cal_HGC_Events_Info,
        "SHMS_cut_no_Cal_HGC_Aero": P_Cut_no_Cal_HGC_Aero_Events_Info,
    }

    return SHMS_Events

def main():
    # Run our functions and get a dict from each
    SHMS_Events_Data = SHMS_events()
    
    # This is just the list of branches we use from the initial root file for each dict
    # They're the "headers" of the data frame we create - i.e. they're going to be the branches in our new root file
    # Note - I don't like re-defining this here as it's very prone to errors if you included (or removed something) earlier but didn't modify it here
    SHMS_Data_Header = ["CTime_eKCoinTime_ROC1","CTime_ePiCoinTime_ROC1","CTime_epCoinTime_ROC1","H_cal_etotnorm", "P_gtr_beta","P_gtr_xp","P_gtr_yp","P_gtr_p","P_gtr_dp","P_cal_etotnorm", "P_aero_npeSum", "P_hgcer_npeSum", "P_hgcer_xAtCer", "P_hgcer_yAtCer", "P_aero_xAtCer", "P_aero_yAtCer","P_cal_fly_earray", "P_cal_pr_eplane", "P_gtr_x", "P_gtr_y", "emiss", "pmiss"]
    data = {} # Create an empty dictionary

    d = SHMS_Events_Data  

    #for d in (All_Events_Data): # Convert individual dictionaries into a "dict of dicts"
    data.update(d) # For every dictionary we give above, add its keys to the new dict
    data_keys = list(data.keys()) # Create a list of all the keys in all dicts added above, each is an array of data

    for i in range (0, len(data_keys)):
        # Set the headers for our data frame
        if("SHMS_" in data_keys[i]):
            DFHeader=list(SHMS_Data_Header)
        else:
            continue
 
        if (i == 0): # For the first case, start writing to file
            pd.DataFrame(data.get(data_keys[i]), columns = DFHeader, index = None).to_root("%s/%s_%s_efficiency.root" % (OUTPATH, runNum, MaxEvent), key ="%s" % data_keys[i])
        elif (i != 0): # For any but the first case, append it to our file
            pd.DataFrame(data.get(data_keys[i]), columns = DFHeader, index = None).to_root("%s/%s_%s_efficiency.root" % (OUTPATH, runNum, MaxEvent), key ="%s" % data_keys[i], mode ='a') 
                    
if __name__ == '__main__':
    main()