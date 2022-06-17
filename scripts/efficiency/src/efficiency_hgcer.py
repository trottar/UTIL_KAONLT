#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-17 11:30:37 trottar"
# ================================================================
# 
# Author:  Richard L. Trotta III <trotta@cua.edu>
# 
# Copyright (c) trottar
#

# 19/10/20 - Stephen Kay, University of Regina

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
import array
from ROOT import TCanvas, TColor, TGaxis, TH1F, TH2F, TPad, TStyle, gStyle, gPad, TGaxis, TLine, TMath, TPaveText, TArc, TGraphPolar 
from ROOT import kBlack, kBlue, kRed

# Input should be the input root file name (including suffix) and an output file name string (without any suffix)
#def hgcer_plots():

#ROOTPrefix = sys.argv[1]
ROOTPrefix = "efficiency"
OutFilename = sys.argv[1]
runNum = sys.argv[2]
MaxEvent = sys.argv[3]

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

proc_root = lt.Root(os.path.realpath(__file__),"Plot_KaonLT_hgcer",ROOTPrefix,runNum,MaxEvent).setup_ana()
p = proc_root[2] # Dictionary of pathing variables
OUTPATH = proc_root[3] # Get pathing for OUTPATH

# Add this to all files for more dynamic pathing
USER =  p["USER"] # Grab user info for file finding
HOST = p["HOST"]
REPLAYPATH = p["REPLAYPATH"]
SCRIPTPATH = p["SCRIPTPATH"]
UTILPATH = p["UTILPATH"]
ANATYPE=p["ANATYPE"]

################################################################################################################################################

rootName = "%s/%s_%s_%s.root" % (OUTPATH, runNum, MaxEvent, ROOTPrefix)

#################################################################################################################################################

InFile = ROOT.TFile.Open(rootName, "READ")
TOutFilename = OutFilename
# Establish the names of our output files quickly
foutname = OUTPATH+"/" + TOutFilename + ".root"
foutpdf = OUTPATH+"/" + TOutFilename + ".pdf"

Events_no_cal_hgc_aero_cuts  = InFile.Get("SHMS_cut_no_Cal_HGC_Aero")  
nEntries_Events_no_cal_hgc_aero_cuts  = Events_no_cal_hgc_aero_cuts.GetEntries()

# Particles information no cuts
SHMS_Events = InFile.Get("SHMS_Events")    
nEntries_SHMS_Events = SHMS_Events.GetEntries()

#################################################################################################################################################

# Defined Geomatrical cuts
cutg = ROOT.TCutG("cutg",21)
cutg.SetVarX("P_hgcer_yAtCer")
cutg.SetVarY("P_hgcer_xAtCer")
cutg.SetPoint(0,-25,2)
cutg.SetPoint(1,-2,2)
cutg.SetPoint(2,-1,2.5)
cutg.SetPoint(3,0,3)
cutg.SetPoint(4,1,3)
cutg.SetPoint(5,2,3.3)
cutg.SetPoint(6,3,3.0)
cutg.SetPoint(7,4,2.5)
cutg.SetPoint(8,5,2)
cutg.SetPoint(9,25,2)
cutg.SetPoint(10,25,0.5)
cutg.SetPoint(11,5,0.5)
cutg.SetPoint(12,4,1)
cutg.SetPoint(13,3,-1)
cutg.SetPoint(14,2,-2)
cutg.SetPoint(15,1,-2.3)
cutg.SetPoint(16,0,-1.5)
cutg.SetPoint(17,-1,-1)
cutg.SetPoint(18,-2,0.5)
cutg.SetPoint(19,-25,0.5)
cutg.SetPoint(20,-25,2)

cutg.SetLineColor(kRed)
cutg.SetLineWidth(5)

h_hgcer_npeSum  = ROOT.TH1D("P_hgcer_npeSum","hgcer", 300,0.3,30)

for evt in Events_no_cal_hgc_aero_cuts:
    h_hgcer_npeSum.Fill(evt.P_hgcer_npeSum)

#################################################################################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE) # Set ROOT to batch mode explicitly, does not splash anything to screen
#################################################################################################################################################

c_CT = TCanvas("c_CT", "HGC (with TCutG)")  
c_CT.Divide(2,2)   
c_CT.cd(1)
Events_no_cal_hgc_aero_cuts.Draw("P_hgcer_npeSum:P_aero_npeSum>>h1(300,0.0,30,300,0,30)", "cutg",  "colz")
c_CT.cd(2)
h_hgcer_npeSum.Draw("colz [cutg]")
print(h_hgcer_npeSum.Integral())
c_CT.cd(3)
Events_no_cal_hgc_aero_cuts.Draw("P_hgcer_npeSum:P_aero_npeSum>>h3(300,0,30, 300, 0, 30)", "!cutg",  "colz") 
c_CT.cd(4)
h_hgcer_npeSum.Draw("colz [!cutg]")
print(h_hgcer_npeSum.Integral())
c_CT.Print(foutpdf)
