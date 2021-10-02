#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-09-30 01:16:58 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import numpy as np
import pandas as pd
import sys, os, subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-reana","--reanalyze", help="Reanalyze lumi data",action="store_true")
args = parser.parse_args() 

l_flag = "all"

if l_flag == "all":
    lumi_list = [5149,5150,5151,5152,5153,5154,5155,5156,5157,5158,5159,5160,5161,5162,5163,5164,5165,5166,5167,5168,5169,5170,5171,5173,
                 5175,5176,5177,5178,5179,5180,5181,5295,5297,5298,5299,5300,5301,5302,5303,7841,7842,7843,7844,7845,7846,7847,7862,7859,
                 7863,7864,7862,7859,7863,7864,7865,7948,7949,7950,7951,7952,7954,7956,7957,7958,7959,7960,7961,8299,8300,8301,8302,8303]
elif l_flag == "1":
    lumi_list = [5154]
else:
    lumi_list = [5154,5155,5156,5157,5158]

if args.reanalyze:
    for l in lumi_list:
        os.system("../replay_lumi.sh %s" % l) 

# Add this to all files for more dynamic pathing
USER = subprocess.getstatusoutput("whoami") # Grab user info for file finding
HOST = subprocess.getstatusoutput("hostname")

if ("farm" in HOST[1]):
    REPLAYPATH = "/group/c-kaonlt/USERS/%s/hallc_replay_lt" % USER[1]
elif ("lark" in HOST[1]):
    REPLAYPATH = "/home/%s/work/JLab/hallc_replay_lt" % USER[1]
elif ("cdaq" in HOST[1]):
    REPLAYPATH = "/home/cdaq/hallc-online/hallc_replay_lt"
elif ("trottar" in HOST[1]):
    REPLAYPATH = "/home/trottar/Analysis/hallc_replay_lt"

inp_f = "%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/lumi_data.csv" % str(REPLAYPATH)
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
    
    file_exists = os.path.isfile(out_f)
    
    table.to_csv(out_f, index = False, header=True, mode='w+',)  

lh2_l1_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5149) & (lumi_data["run number"] <= 5153)) 
                                 | ((lumi_data["run number"] >= 5159) & (lumi_data["run number"] <= 5166)) 
                                 | ((lumi_data["run number"] >= 5295) & (lumi_data["run number"] <= 5297))])
convertDFtoCSV(lh2_l1_10p6,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_1/LH2/lumi_data_lh2_l1_10p6.csv" % str(REPLAYPATH))
print("\n\nLumi #1 LH2 runs {0} are now in {1}".format(list(lh2_l1_10p6["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_1/LH2/lumi_data_lh2_l1_10p6.csv" % str(REPLAYPATH)))

c_l1_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5154) & (lumi_data["run number"] <= 5158)) 
                               | ((lumi_data["run number"] >= 5298) & (lumi_data["run number"] <= 5299))])
convertDFtoCSV(c_l1_10p6,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_1/Carbon0p5/lumi_data_c_l1_10p6.csv" % str(REPLAYPATH))
print("\n\nLumi #1 Carbon0p5 runs {0} are now in {1}".format(list(c_l1_10p6["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_1/Carbon0p5/lumi_data_c_l1_10p6.csv" % str(REPLAYPATH)))

lh2_l2_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5167) & (lumi_data["run number"] <= 5171)) 
                                 | ((lumi_data["run number"] >= 5302) & (lumi_data["run number"] <= 5303))])
convertDFtoCSV(lh2_l2_10p6,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_2/LH2/lumi_data_lh2_l2_10p6.csv" % str(REPLAYPATH))
print("\n\nLumi #2 LH2 runs {0} are now in {1}".format(list(lh2_l2_10p6["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_2/LH2/lumi_data_lh2_l2_10p6.csv" % str(REPLAYPATH)))

c_l2_10p6 = dict(lumi_data.loc[((lumi_data["run number"] >= 5174) & (lumi_data["run number"] <= 5181)) 
                               | ((lumi_data["run number"] >= 5300) & (lumi_data["run number"] <= 5301))])
convertDFtoCSV(c_l2_10p6,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_2/Carbon0p5/lumi_data_c_l2_10p6.csv" % str(REPLAYPATH))
print("\n\nLumi #2 Carbon0p5 runs {0} are now in {1}".format(list(c_l2_10p6["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/10p6/Lumi_2/Carbon0p5/lumi_data_c_l2_10p6.csv" % str(REPLAYPATH)))

lh2_l1_6p2 = dict(lumi_data.loc[((lumi_data["run number"] >= 7843) & (lumi_data["run number"] <= 7845)) 
                                | ((lumi_data["run number"] >= 7862) & (lumi_data["run number"] <= 7863))])
convertDFtoCSV(lh2_l1_6p2,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/6p2/Lumi_1/LH2/lumi_data_lh2_l1_6p2.csv" % str(REPLAYPATH))
print("\n\nLumi #1 LH2 runs {0} are now in {1}".format(list(lh2_l1_6p2["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/6p2/Lumi_1/LH2/lumi_data_lh2_l1_6p2.csv" % str(REPLAYPATH)))

c_l1_6p2 = dict(lumi_data.loc[(lumi_data["run number"] == 7841) | ((lumi_data["run number"] >= 7846) & (lumi_data["run number"] <= 7847)) 
                              | ((lumi_data["run number"] >= 7864) & (lumi_data["run number"] <= 7865))])
convertDFtoCSV(c_l1_6p2,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/6p2/Lumi_1/Carbon0p5/lumi_data_c_l1_6p2.csv" % str(REPLAYPATH))
print("\n\nLumi #1 Carbon0p5 runs {0} are now in {1}".format(list(c_l1_6p2["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/6p2/Lumi_1/Carbon0p5/lumi_data_c_l1_6p2.csv" % str(REPLAYPATH)))

lh2_l1_8p2 = dict(lumi_data.loc[((lumi_data["run number"] >= 7953) & (lumi_data["run number"] <= 7960))])
convertDFtoCSV(lh2_l1_8p2,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/8p2/Lumi_1/LH2/lumi_data_lh2_l1_8p2.csv" % str(REPLAYPATH))
print("\n\nLumi #1 LH2 runs {0} are now in {1}".format(list(lh2_l1_8p2["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/8p2/Lumi_1/LH2/lumi_data_lh2_l1_8p2.csv" % str(REPLAYPATH)))

c_l1_8p2 = dict(lumi_data.loc[((lumi_data["run number"] >= 7948) & (lumi_data["run number"] <= 7952))])
convertDFtoCSV(c_l1_8p2,"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/8p2/Lumi_1/Carbon0p5/lumi_data_c_l1_8p2.csv" % str(REPLAYPATH))
print("\n\nLumi #1 Carbon0p5 runs {0} are now in {1}".format(list(c_l1_8p2["run number"]),"%s/UTIL_KAONLT/scripts/luminosity/OUTPUTS/8p2/Lumi_1/Carbon0p5/lumi_data_c_l1_8p2.csv" % str(REPLAYPATH)))
