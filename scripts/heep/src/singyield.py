#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-13 07:41:43 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

# 15/01/21 - Stephen Kay, University of Regina
# 21/06/21 - Edited By - Muhammad Junaid, University of Regina, Canada

# Python version of the kaon analysis script. Now utilises uproot to select event of each type and writes them to a root file
# Intention is to apply PID/selection cutting here and plot in a separate script
# Python should allow for easier reading of databases storing timing offsets e.t.c.
# 27/04/21 - Updated to use new hcana variables, old determinations removed

###################################################################################################################################################

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

##################################################################################################################################################

# Check the number of arguments provided to the script
if len(sys.argv)-1!=4:
    print("!!!!! ERROR !!!!!\n Expected 4 arguments\n Usage is with - ROOTfilePrefix RunNumber MaxEvents spec \n!!!!! ERROR !!!!!")
    sys.exit(1)

##################################################################################################################################################

# Input params - run number and max number of events
ROOTPrefix = sys.argv[1]
runNum = sys.argv[2]
MaxEvent = sys.argv[3]
spec = sys.argv[4]

spec = spec.upper()

################################################################################################################################################
'''
ltsep package import
'''

# Import package for cuts
import ltsep as lt 

###############################################################################################################################################

# Defining path for cut file  
if spec == "HMS":
    f_cut = '/DB/CUTS/run_type/hSing_prod.cuts'
if spec == "SHMS":
    f_cut = '/DB/CUTS/run_type/pSing_prod.cuts'

# defining Cuts
if spec == "HMS":
    cuts = ["sing_ee_cut_all_noRF"]
if spec == "SHMS":
    cuts = ["sing_ee_cut_all_noRF"]

proc_root = lt.Root(os.path.realpath(__file__),"HeePSing_%s" % spec,ROOTPrefix,runNum,MaxEvent,f_cut,cuts).setup_ana()
c = proc_root[0] # Cut object
b = proc_root[1] # Dictionary of branches
p = proc_root[2] # Dictionary of pathing variables
OUTPATH = proc_root[3] # Get pathing for OUTPATH

#################################################################################################################################################################

def sing():

    if spec == "HMS":
        # Define the array of arrays containing the relevant HMS and SHMS info                              
        
        NoCut_SING = [b["H_gtr_beta"],b["H_gtr_xp"],b["H_gtr_yp"],b["H_gtr_dp"],b["H_gtr_p"],b["H_hod_goodscinhit"],b["H_hod_goodstarttime"],b["H_cal_etotnorm"],b["H_cal_etottracknorm"],b["H_cer_npeSum"],b["H_RF_Dist"], b['H_W']]
        
        Uncut_SING = [(b["H_gtr_beta"],b["H_gtr_xp"],b["H_gtr_yp"],b["H_gtr_dp"],b["H_gtr_p"],b["H_hod_goodscinhit"],b["H_hod_goodstarttime"],b["H_cal_etotnorm"],b["H_cal_etottracknorm"],b["H_cer_npeSum"],b["H_RF_Dist"], b['H_W']) for (b["H_gtr_beta"],b["H_gtr_xp"],b["H_gtr_yp"],b["H_gtr_dp"],b["H_gtr_p"],b["H_hod_goodscinhit"],b["H_hod_goodstarttime"],b["H_cal_etotnorm"],b["H_cal_etottracknorm"],b["H_cer_npeSum"],b["H_RF_Dist"], b['H_W']) in zip(*NoCut_SING)]
        
        # Create array of arrays of pions after cuts, all events
        
        Cut_SING_tmp = NoCut_SING
        Cut_SING_all_tmp = []
        
        for arr in Cut_SING_tmp:
            Cut_SING_all_tmp.append(c.add_cut(arr, "sing_ee_cut_all_noRF"))
            
        Cut_SING_all = [(b["H_gtr_beta"],b["H_gtr_xp"],b["H_gtr_yp"],b["H_gtr_dp"],b["H_gtr_p"],b["H_hod_goodscinhit"],b["H_hod_goodstarttime"],b["H_cal_etotnorm"],b["H_cal_etottracknorm"],b["H_cer_npeSum"],b["H_RF_Dist"], b['H_W']) for (b["H_gtr_beta"],b["H_gtr_xp"],b["H_gtr_yp"],b["H_gtr_dp"],b["H_gtr_p"],b["H_hod_goodscinhit"],b["H_hod_goodstarttime"],b["H_cal_etotnorm"],b["H_cal_etottracknorm"],b["H_cer_npeSum"],b["H_RF_Dist"], b['H_W']) in zip(*Cut_SING_all_tmp)]
        
        SING = {
            "Uncut_Events" : Uncut_SING,
            "Cut_Events_All" : Cut_SING_all,
        }

    if spec == "SHMS":
        # Define the array of arrays containing the relevant HMS and SHMS info                              
        
        NoCut_SING = [b["pmiss_z"], b["pmiss_y"], b["pmiss_x"], b["W"], b["MMpi"], b["pmiss"], b["emiss"], b["P_gtr_beta"], b["P_gtr_xp"], b["P_gtr_yp"], b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["P_RF_Dist"]]
        
        Uncut_SING = [(b["pmiss_z"], b["pmiss_y"], b["pmiss_x"], b["W"], b["MMpi"], b["pmiss"], b["emiss"], b["P_gtr_beta"], b["P_gtr_xp"], b["P_gtr_yp"], b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["P_RF_Dist"]) for (b["pmiss_z"], b["pmiss_y"], b["pmiss_x"], b["W"], b["MMpi"], b["pmiss"], b["emiss"], b["P_gtr_beta"], b["P_gtr_xp"], b["P_gtr_yp"], b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["P_RF_Dist"]) in zip(*NoCut_SING)]
        
        # Create array of arrays of pions after cuts, all events
        
        Cut_SING_tmp = NoCut_SING
        Cut_SING_all_tmp = []
        
        for arr in Cut_SING_tmp:
            Cut_SING_all_tmp.append(c.add_cut(arr, "sing_ee_cut_all_noRF"))
            
        Cut_SING_all = [(b["pmiss_z"], b["pmiss_y"], b["pmiss_x"], b["W"], b["MMpi"], b["pmiss"], b["emiss"], b["P_gtr_beta"], b["P_gtr_xp"], b["P_gtr_yp"], b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["P_RF_Dist"]) for (b["pmiss_z"], b["pmiss_y"], b["pmiss_x"], b["W"], b["MMpi"], b["pmiss"], b["emiss"], b["P_gtr_beta"], b["P_gtr_xp"], b["P_gtr_yp"], b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["P_RF_Dist"]) in zip(*Cut_SING_all_tmp)]
        
        SING = {
            "Uncut_Events" : Uncut_SING,
            "Cut_Events_All" : Cut_SING_all,
        }
                
    return SING
        
##################################################################################################################################################################

def main():
    SING_Data = sing()

    # This is just the list of branches we use from the initial root file for each dict
    # I don't like re-defining this here as it's very prone to errors if you included (or removed something) earlier but didn't modify it here
    # Should base the branches to include based on some list and just repeat the list here (or call it again directly below)

    if spec == "HMS":
        SING_Data_Header = ["H_gtr_beta","H_gtr_xp","H_gtr_yp","H_gtr_dp", "H_gtr_p","H_hod_goodscinhit","H_hod_goodstarttime","H_cal_etotnorm","H_cal_etottracknorm","H_cer_npeSum","H_RF_Dist","H_W"]
    if spec == "SHMS":
        SING_Data_Header = ["pmiss_z","pmiss_y","pmiss_x", "W","MMpi","pmiss","emiss","P_gtr_beta","P_gtr_xp","P_gtr_yp","P_gtr_p","P_gtr_dp","P_hod_goodscinhit","P_hod_goodstarttime","P_cal_etotnorm","P_cal_etottracknorm","P_aero_npeSum","P_aero_xAtAero","P_aero_yAtAero","P_hgcer_npeSum","P_hgcer_xAtCer","P_hgcer_yAtCer","P_RF_Dist"]
        
    # Need to create a dict for all the branches we grab                                                
    data = {}
    data.update(SING_Data)
    data_keys = list(data.keys()) # Create a list of all the keys in all dicts added above, each is an array of data                                                                                       

    for i in range (0, len(data_keys)):
        if("Events" in data_keys[i]):
            DFHeader=list(SING_Data_Header)
        else:
            continue
            # Uncomment the line below if you want .csv file output, WARNING the files can be very large and take a long time to process!                                                                      
            #pd.DataFrame(data.get(data_keys[i])).to_csv("%s/%s_%s.csv" % (OUTPATH, data_keys[i], runNum), header=DFHeader, index=False) # Convert array to panda dataframe and write to csv with correct header                                                                                                      
        if (i == 0):
            pd.DataFrame(data.get(data_keys[i]), columns = DFHeader, index = None).to_root("%s/%s_%s_%s_An\
alysed_Data.root" % (OUTPATH, runNum, MaxEvent, spec), key ="%s" % data_keys[i])
        elif (i != 0):
            pd.DataFrame(data.get(data_keys[i]), columns = DFHeader, index = None).to_root("%s/%s_%s_%s_An\
alysed_Data.root" % (OUTPATH, runNum, MaxEvent, spec), key ="%s" % data_keys[i], mode ='a')

if __name__ == '__main__':
    main()
print ("Processing Complete")
