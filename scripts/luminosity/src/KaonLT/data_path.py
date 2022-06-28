#! /usr/bin/python
#
# Description: Grabs lumi data from corresponding csv depending on run setting. Then plots the yields and creates a comprehensive table.
# Variables calculated: current, rate_HMS, rate_SHMS, sent_edtm_PS, uncern_HMS_evts_scaler, uncern_SHMS_evts_scaler, uncern_HMS_evts_notrack, uncern_SHMS_evts_notrack, uncern_HMS_evts_track, uncern_SHMS_evts_track
# ================================================================
# Time-stamp: "2022-06-27 06:18:14 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#


def get_file(inp_name,SCRIPTPATH):
    '''
    Grab proper lumi data file
    '''

    # Depending on input, the corresponding data setting csv data will be grabbed
    if "10p6" in inp_name:
        if "l1" in inp_name:
            if "LH2" in inp_name.upper():
                target = "LH2"
                inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/LH2/lumi_data_lh2_l1_10p6.csv"
                out_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/LH2/yield_data_lh2_l1_10p6.csv"
                print("\nGrabbing input...\n%s" % str(inp_f))
            if "C" in inp_name.upper():
                target = "carbon"
                inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/Carbon0p5/lumi_data_c_l1_10p6.csv"
                out_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/Carbon0p5/yield_data_c_l1_10p6.csv"
                print("\nGrabbing input...\n%s" % str(inp_f))
        elif "l2" in inp_name:
            if "LH2" in inp_name.upper():
                target = "LH2"
                inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/LH2/lumi_data_lh2_l2_10p6.csv"
                out_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/LH2/yield_data_lh2_l2_10p6.csv"
            if "C" in inp_name.upper():
                target = "carbon"
                inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/Carbon0p5/lumi_data_c_l2_10p6.csv"
                out_f = SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/Carbon0p5/yield_data_c_l2_10p6.csv"
                print("\nGrabbing input...\n%s" % str(inp_f))

    elif "6p2" in inp_name:
        if "LH2" in inp_name.upper():
            target = "LH2"
            inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/LH2/lumi_data_lh2_l1_6p2.csv"
            out_f = SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/LH2/yield_data_lh2_l1_6p2.csv"
            print("\nGrabbing input...\n%s" % str(inp_f))
        if "C" in inp_name.upper():
            target = "carbon"
            inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/Carbon0p5/lumi_data_c_l1_6p2.csv"
            out_f = SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/Carbon0p5/yield_data_c_l1_6p2.csv"
            print("\nGrabbing input...\n%s" % str(inp_f))

    elif "8p2" in inp_name:
        if "LH2" in inp_name.upper():
            target = "LH2"
            inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/LH2/lumi_data_lh2_l1_8p2.csv"
            out_f = SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/LH2/yield_data_lh2_l1_8p2.csv"
            print("\nGrabbing input...\n%s" % str(inp_f))
        if "C" in inp_name.upper():
            target = "carbon"
            inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/Carbon0p5/lumi_data_c_l1_8p2.csv"
            out_f = SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/Carbon0p5/yield_data_c_l1_8p2.csv"
            print("\nGrabbing input...\n%s" % str(inp_f))

    else:
        target = "carbon"
        inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/lumi_data.csv"
        out_f = SCRIPTPATH+"/luminosity/OUTPUTS/yield_data.csv"
        print("\nError: Invalid input...\nGrabbing default input...\n%s" % str(inp_f))

    return [target,inp_f,out_f]
