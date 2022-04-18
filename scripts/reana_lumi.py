#! /usr/bin/python
#
# Description: Script is used to reanalyze all lumi data or to organize lumi data values into subdirectories
# ================================================================
# Time-stamp: "2021-11-03 06:36:01 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import numpy as np
import pandas as pd
import sys, os, subprocess

################################################################################################################################################
'''
Define a flag to reanalyze lumi data
'''

# Defines a flag for python which will reanalyze all lumi data
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-reana","--reanalyze", help="Reanalyze lumi data",action="store_true")
args = parser.parse_args() 

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

print("@@",os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
USER =  lt.SetPath(os.path.realpath(__file__)).getPath("USER") # Grab user info for file finding
HOST = lt.SetPath(os.path.realpath(__file__)).getPath("HOST")
SCRIPTPATH = lt.SetPath(os.path.realpath(__file__)).getPath("SCRIPTPATH")

################################################################################################################################################
'''
Determine which runs to reanalyze
'''

# Flag to chose which runs to plot (mainly for debugging, keep as "all")
l_flag = "1"

if l_flag == "all":
    # All lumi runs
    lumi_list = [5149,5150,5151,5152,5153,5154,5155,5156,5157,5158,5159,5160,5161,5162,5163,5164,5165,5166,5167,5168,5169,5170,5171,5173,
                 5175,5176,5177,5178,5179,5180,5181,5295,5297,5298,5299,5300,5301,5302,5303,7841,7842,7843,7844,7845,7846,7847,7862,7859,
                 7863,7864,7862,7859,7863,7864,7865,7948,7949,7950,7951,7952,7954,7956,7957,7958,7959,7960,7961,8299,8300,8301,8302,8303]
elif l_flag == "1":
    # One run (change as needed)
    lumi_list = [5154]
else:
    # Any number of runs
    lumi_list = [5154,5155,5156,5157,5158,5298,5299]

################################################################################################################################################
'''
Reanalyze data
'''

# If reanalyze argument is called then all lumi data will be processed again
if args.reanalyze:
    for l in lumi_list:
        os.system("../replay_lumi.sh %s" % l) 

################################################################################################################################################
'''
Move lumi analyzed data from general csv to setting and target specific
'''

# Location of lumi data csv
inp_f = SCRIPTPATH+"/luminosity/OUTPUTS/lumi_data.csv"
try:
    lumi_data = pd.read_csv(inp_f)
except IOError:
    print("Error: %s does not appear to exist." % inp_f)
print(lumi_data.keys())

def convertDFtoCSV(inp_data,out_f):
    '''
    Converts dataframe to csv file for arbitrary df and output location
    '''
    table  = pd.DataFrame(inp_data, columns=inp_data.keys())
    table = table.reindex(sorted(table.columns), axis=1)
    
    table.to_csv(out_f, index = False, header=True, mode='w+',)  

# Redefine lumi data by run number
lh2_l1_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5149) & (lumi_data["run number"] <= 5153)) 
                                 | ((lumi_data["run number"] >= 5159) & (lumi_data["run number"] <= 5166)) 
                                 | ((lumi_data["run number"] >= 5295) & (lumi_data["run number"] <= 5297))])
# Convert to csv from dataframe
convertDFtoCSV(lh2_l1_10p6,SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/LH2/lumi_data_lh2_l1_10p6.csv")
print("\n\nLumi #1 LH2 runs {0} are now in {1}".format(list(lh2_l1_10p6["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/LH2/lumi_data_lh2_l1_10p6.csv"))

c_l1_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5154) & (lumi_data["run number"] <= 5158)) 
                               | ((lumi_data["run number"] >= 5298) & (lumi_data["run number"] <= 5299))])
convertDFtoCSV(c_l1_10p6,SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/Carbon0p5/lumi_data_c_l1_10p6.csv")
print("\n\nLumi #1 Carbon0p5 runs {0} are now in {1}".format(list(c_l1_10p6["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_1/Carbon0p5/lumi_data_c_l1_10p6.csv"))

lh2_l2_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5167) & (lumi_data["run number"] <= 5171)) 
                                 | ((lumi_data["run number"] >= 5302) & (lumi_data["run number"] <= 5303))])
convertDFtoCSV(lh2_l2_10p6,SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/LH2/lumi_data_lh2_l2_10p6.csv")
print("\n\nLumi #2 LH2 runs {0} are now in {1}".format(list(lh2_l2_10p6["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/LH2/lumi_data_lh2_l2_10p6.csv"))

c_l2_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5174) & (lumi_data["run number"] <= 5181)) 
                               | ((lumi_data["run number"] >= 5300) & (lumi_data["run number"] <= 5301))])
convertDFtoCSV(c_l2_10p6,SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/Carbon0p5/lumi_data_c_l2_10p6.csv")
print("\n\nLumi #2 Carbon0p5 runs {0} are now in {1}".format(list(c_l2_10p6["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/10p6/Lumi_2/Carbon0p5/lumi_data_c_l2_10p6.csv"))

lh2_l1_6p2 = dict(lumi_data.loc[((lumi_data["run number"] >= 7843) & (lumi_data["run number"] <= 7845)) 
                                | ((lumi_data["run number"] >= 7862) & (lumi_data["run number"] <= 7863))])
convertDFtoCSV(lh2_l1_6p2,SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/LH2/lumi_data_lh2_l1_6p2.csv")
print("\n\nLumi #1 LH2 runs {0} are now in {1}".format(list(lh2_l1_6p2["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/LH2/lumi_data_lh2_l1_6p2.csv"))

c_l1_6p2 = dict(lumi_data.loc[(lumi_data["run number"] == 7841) | ((lumi_data["run number"] >= 7846) & (lumi_data["run number"] <= 7847)) 
                              | ((lumi_data["run number"] >= 7864) & (lumi_data["run number"] <= 7865))])
convertDFtoCSV(c_l1_6p2,SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/Carbon0p5/lumi_data_c_l1_6p2.csv")
print("\n\nLumi #1 Carbon0p5 runs {0} are now in {1}".format(list(c_l1_6p2["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/6p2/Lumi_1/Carbon0p5/lumi_data_c_l1_6p2.csv"))

lh2_l1_8p2 = dict(lumi_data.loc[((lumi_data["run number"] >= 7953) & (lumi_data["run number"] <= 7960))])
convertDFtoCSV(lh2_l1_8p2,SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/LH2/lumi_data_lh2_l1_8p2.csv")
print("\n\nLumi #1 LH2 runs {0} are now in {1}".format(list(lh2_l1_8p2["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/LH2/lumi_data_lh2_l1_8p2.csv"))

c_l1_8p2 = dict(lumi_data.loc[((lumi_data["run number"] >= 7948) & (lumi_data["run number"] <= 7952))])
convertDFtoCSV(c_l1_8p2,SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/Carbon0p5/lumi_data_c_l1_8p2.csv")
print("\n\nLumi #1 Carbon0p5 runs {0} are now in {1}".format(list(c_l1_8p2["run number"]),SCRIPTPATH+"/luminosity/OUTPUTS/8p2/Lumi_1/Carbon0p5/lumi_data_c_l1_8p2.csv"))
