#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-09 04:02:06 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

################################################################################################################################################
'''
'''
import re

def dictionary(UTILPATH,ROOTPrefix,runNum,MaxEvent):

    # Open report file to grab prescale values and tracking efficiency
    report = UTILPATH+"/REPORT_OUTPUT/Analysis/General/%s_%s_%s.report" % (ROOTPrefix,runNum,MaxEvent)

    with open(report) as f:
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
            'BCM_Cut_SHMS_Run_Length': None,
            'BCM_Cut_HMS_Run_Length': None,
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
            'HMS_CPULT': None,
            'HMS_CPULT Error': None,
            'SHMS_CPULT': None,
            'SHMS_CPULT Error': None,
            'COIN_CPULT': None,
            'COIN_CPULT Error': None,
            'Non_Scaler_EDTM_Live_Time': None,
            'Non_Scaler_EDTM_Live_Time_ERROR': None,
            'SHMS_Hodo_3_of_4_EFF': None,
            #'SHMS Hodo efficiencies error': None,
            'SHMS_Hodo_4_of_4_EFF': None,
            #'SHMS Hodo efficiencies error': None,
            'HMS_Hodo_3_of_4_EFF': None,
            #'HMS Hodo efficiencies error': None,
            'HMS_Hodo_4_of_4_EFF': None,
            #'HMS Hodo efficiencies error': None,
            'HMS_Cer_ALL_Elec_Eff': None,
            'HMS_Cer_ALL_Elec_Eff_ERROR': None,
            'HMS_Cer_COIN_Elec_Eff': None,
            'HMS_Cer_COIN_Elec_Eff_ERROR': None,
            'HMS_Cer_SING_Elec_Eff': None,
            'HMS_Cer_SING_Elec_Eff_ERROR': None,
            'SHMS_Aero_Prot_Eff': None,
            'SHMS_Aero_Prot_Eff_ERROR': None,
            'SHMS_Aero_ALL_Pion_Eff': None,
            'SHMS_Aero_ALL_Pion_Eff_ERROR': None,
            'SHMS_Aero_COIN_Pion_Eff': None,
            'SHMS_Aero_COIN_Pion_Eff_ERROR': None,
            'SHMS_Aero_SING_Pion_Eff': None,
            'SHMS_Aero_SING_Pion_Eff_ERROR': None,
            'SHMS_HGC_Prot_Eff': None,
            'SHMS_HGC_Prot_Eff_ERROR': None,
            'SHMS_HGC_Pion_Eff': None,
            'SHMS_HGC_Pion_Eff_ERROR': None,
            "SHMS_Hadron_ALL_TRACK_EFF" : None,
            "SHMS_Hadron_ALL_TRACK_EFF_ERROR" : None,
            "SHMS_Prot_ALL_TRACK_EFF" : None,
            "SHMS_Prot_ALL_TRACK_EFF_ERROR" : None,
            "SHMS_Prot_COIN_TRACK_EFF" : None,
            "SHMS_Prot_COIN_TRACK_EFF_ERROR" : None,
            "SHMS_Prot_SING_TRACK_EFF" : None,
            "SHMS_Prot_SING_TRACK_EFF_ERROR" : None,
            "SHMS_Pion_ALL_TRACK_EFF" : None,
            "SHMS_Pion_ALL_TRACK_EFF_ERROR" : None,
            "SHMS_Pion_COIN_TRACK_EFF" : None,
            "SHMS_Pion_COIN_TRACK_EFF_ERROR" : None,
            "SHMS_Pion_SING_TRACK_EFF" : None,
            "SHMS_Pion_SING_TRACK_EFF_ERROR" : None,
            "HMS_Elec_ALL_TRACK_EFF" : None,
            "HMS_Elec_ALL_TRACK_EFF_ERROR" : None,
            "HMS_Elec_COIN_TRACK_EFF" : None,
            "HMS_Elec_COIN_TRACK_EFF_ERROR" : None,
            "HMS_Elec_SING_TRACK_EFF" : None,
            "HMS_Elec_SING_TRACK_EFF_ERROR" : None,
            'Target_Mass_(amu)': None ,

        }

        # Search for keywords, then save as value in dictionary
        for line in f:
            data = line.split(':')
            for key,val in effDict.items():
                if "ERROR" in key:
                    if key.replace("_ERROR","") in data[0]:                    
                        effDict[key] = float(re.sub("\D","","%s" % data[1].split("+-")[1]))
                if key in data[0]:
                    effDict[key] = float(re.sub("\D","","%s" % data[1].split("+-")[0]))
        #print(effDict)

    return effDict
