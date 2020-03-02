#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2020-03-01 19:21:11 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

from ROOT import TChain, TProof, TSelector, TTree

import sys

RunNumber=sys.argv[1]
# MaxEvent=sys.argv[2]
MaxEvent=50000

report = "/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/REPORT_OUTPUT/COIN/PRODUCTION/Lumi_coin_replay_production_Offline_%s_%s.report" % (RunNumber,MaxEvent)

f = open(report)
fout = open("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/scripts_Luminosity/Yield_Data.dat","wb")

psList = ['Ps1_factor','Ps3_factor','Ps5_factor']

psValue = ['-1','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']

for line in f:
    data = line.split('=')
    for index, obj in enumerate(psList) :
        if (psList[index] in data[0]) : 
            if (index == 0) :  
                ps1_tmp = data[1].split(" ")
            if (index == 1) : 
                ps3_tmp = data[1].split(" ")
            if (index == 2) :
                ps5_tmp = data[1].split(" ")
ps1=float(ps1_tmp[1])
ps3=float(ps3_tmp[1])
ps5=float(ps5_tmp[1])
fout.write(RunNumber + " ")
fout.write(ps1 + " ")
fout.write(ps3 + " ")
f.close()
fout.close()

option = "%s.%s" % (ps1,ps3)

proof = TProof.Open("workers=4")

ch = TChain("T")

sc = TChain("TSH")

ch.Add("/u/group/c-kaonlt/tmp_TProofTest/Lumi_coin_replay_production_Offline_%s_%s.root" % (RunNumber,MaxEvent))
ch.SetProof()
ch.Process("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/scripts_Luminosity/LumiYield.C+",option)
  
sc.Add("/u/group/c-kaonlt/tmp_TProofTest/Lumi_coin_replay_production_Offline_%s_%s.root" % (RunNumber,MaxEvent))
sc.SetProof()
sc.Process("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/scripts_Luminosity/Scalers.C+",option)

proof.Close()
