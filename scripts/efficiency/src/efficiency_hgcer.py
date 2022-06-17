#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-17 10:46:53 trottar"
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

InFile = ROOT.TFile.Open(rootName, "READ");
TOutFilename = OutFilename;
# Establish the names of our output files quickly
foutname = OUTPATH+"/" + TOutFilename + ".root";
foutpdf = OUTPATH+"/" + TOutFilename + ".pdf";

# Particles information with HGC cuts
Pions         = InFile.Get("SHMS_Pions") 
nEntries_Pions = Pions.GetEntries()
Kaons         = InFile.Get("SHMS_Kaons") 
nEntries_Kaons = Kaons.GetEntries()
Protons       = InFile.Get("SHMS_Protons")
nEntries_Protons = Protons.GetEntries()
Positrons     = InFile.Get("SHMS_Positrons") 
nEntries_Positrons = Positrons.GetEntries()

# Particles information no HGC cuts
Pions_No_HGC_Cuts         = InFile.Get("SHMS_Pions_Without_HGC_Cuts")      ;  
nEntries_Pions_No_HGC_Cuts       = Pions_No_HGC_Cuts.GetEntries();
Positrons_No_HGC_Cuts     = InFile.Get("SHMS_Positrons_Without_HGC_Cuts")  ;  
nEntries_Positrons_No_HGC_Cuts   = Positrons_No_HGC_Cuts.GetEntries();
Kaons_No_HGC_Cuts         = InFile.Get("SHMS_Kaons_Without_HGC_Cuts")      ;  
nEntries_Kaons_No_HGC_Cuts       = Kaons_No_HGC_Cuts.GetEntries();
Protons_No_HGC_Cuts       = InFile.Get("SHMS_Protons_Without_HGC_Cuts")    ;  
nEntries_Protons_No_HGC_Cuts     = Protons_No_HGC_Cuts.GetEntries();
Pions_No_Aero_Cuts        = InFile.Get("SHMS_Pions_Aero_Without_Aero_Cuts");  
nEntries_Pions_No_Aero_Cuts  = Pions_No_Aero_Cuts.GetEntries();
Pions_No_Cal_Cuts         = InFile.Get("SHMS_Pions_Cal_Without_Cal_Cuts")  ;  
nEntries_Pions_No_Cal_Cuts     = Pions_No_Cal_Cuts.GetEntries();

# Particles information no Cal HGC and Aero cuts
Events_no_cal_hgc_cuts       = InFile.Get("SHMS_cut_no_Cal_HGC")       ;  
nEntries_Events_no_cal_hgc_cuts       = Events_no_cal_hgc_cuts.GetEntries();
Events_no_cal_hgc_aero_cuts  = InFile.Get("SHMS_cut_no_Cal_HGC_Aero")  ;  
nEntries_Events_no_cal_hgc_aero_cuts  = Events_no_cal_hgc_aero_cuts.GetEntries();

# Particles information no cuts
SHMS_Events = InFile.Get("SHMS_Events")  ;  
nEntries_SHMS_Events = SHMS_Events.GetEntries();

#################################################################################################################################################

# Defined Geomatrical cuts
cutg = ROOT.TCutG("cutg",21);
cutg.SetVarX("P_hgcer_yAtCer");
cutg.SetVarY("P_hgcer_xAtCer");
cutg.SetPoint(0,-25,2);
cutg.SetPoint(1,-2,2);
cutg.SetPoint(2,-1,2.5);
cutg.SetPoint(3,0,3);
cutg.SetPoint(4,1,3);
cutg.SetPoint(5,2,3.3);
cutg.SetPoint(6,3,3.0);
cutg.SetPoint(7,4,2.5);
cutg.SetPoint(8,5,2);
cutg.SetPoint(9,25,2);
cutg.SetPoint(10,25,0.5);
cutg.SetPoint(11,5,0.5);
cutg.SetPoint(12,4,1);
cutg.SetPoint(13,3,-1);
cutg.SetPoint(14,2,-2);
cutg.SetPoint(15,1,-2.3);
cutg.SetPoint(16,0,-1.5);
cutg.SetPoint(17,-1,-1);
cutg.SetPoint(18,-2,0.5);
cutg.SetPoint(19,-25,0.5);
cutg.SetPoint(20,-25,2);

cutg.SetLineColor(kRed);
cutg.SetLineWidth(5);
# cut for npe

cutg1 = ROOT.TCutG("cutg1",21);
cutg1.SetVarX("P_hgcer_npeSum");
cutg1.SetVarY("P_aero_npeSum");
cutg1.SetPoint(0,-10,2);
cutg1.SetPoint(1,-2,2);
cutg1.SetPoint(2,-1,2.5);
cutg1.SetPoint(3,0,3);
cutg1.SetPoint(4,1,3);
cutg1.SetPoint(5,2,3.3);
cutg1.SetPoint(6,3,3.0);
cutg1.SetPoint(7,4,2.5);
cutg1.SetPoint(8,5,2);
cutg1.SetPoint(9,10,2);
cutg1.SetPoint(10,10,1);
cutg1.SetPoint(11,5,1);
cutg1.SetPoint(12,4,1);
cutg1.SetPoint(13,3,-1);
cutg1.SetPoint(14,2,-2);
cutg1.SetPoint(15,1,-2.3);
cutg1.SetPoint(16,0,-1.5);
cutg1.SetPoint(17,-1,-1);
cutg1.SetPoint(18,-2,1);
cutg1.SetPoint(19,-10,1);
cutg1.SetPoint(20,-10,2);

cutg1.SetLineColor(kRed);
cutg1.SetLineWidth(5);

#################################################################################################################################################

cutg2 = ROOT.TCutG("cutg2",21);
cutg2.SetVarX("P_hgcer_yAtCer");
cutg2.SetVarY("P_hgcer_xAtCer");
cutg2.SetPoint(0,-25,2);
cutg2.SetPoint(1,-2,2);
cutg2.SetPoint(2,-1,2.5);
cutg2.SetPoint(3,0,3);
cutg2.SetPoint(4,1,3);
cutg2.SetPoint(5,2,3.3);
cutg2.SetPoint(6,3,3.0);
cutg2.SetPoint(7,4,2.5);
cutg2.SetPoint(8,5,2);
cutg2.SetPoint(9,25,2);
cutg2.SetPoint(10,25,0.5);
cutg2.SetPoint(11,5,0.5);
cutg2.SetPoint(12,4,1);
cutg2.SetPoint(13,3,-1);
cutg2.SetPoint(14,2,-2);
cutg2.SetPoint(15,1,-2.3);
cutg2.SetPoint(16,0,-1.5);
cutg2.SetPoint(17,-1,-1);
cutg2.SetPoint(18,-2,0.5);
cutg2.SetPoint(19,-25,0.5);
cutg2.SetPoint(20,-25,2);

cutg2.SetLineColor(kRed);
cutg2.SetLineWidth(5);

'''

#################################################################################################################################################

# Define Histograms for with HGC cuts

# For 1D histos, can easily create directly from the corresponding branch
#Pions.Draw("P_hgcer_npeSum >> h1_CT_Pions", "", "goff"); 
#Kaons.Draw("CTime_eKCoinTime_ROC1 >> h1_CT_Kaons", "", "goff"); 
#Protons.Draw("CTime_eKCoinTime_ROC1 >> h1_CT_Protons", "", "goff"); 

#Histograms for aerogel and Cal
h1_aero_npeSum = ROOT.TH1D("h1_aero_npeSum","Aerogel; P_aero_npeSum; Events;", 300, 0.0, 30);

for evt in Pions_No_Aero_Cuts:
    h1_aero_npeSum.Fill(evt.P_aero_npeSum);


h1_cal_etot = ROOT.TH1D("h1_cal_etot","Calorimeter; P_cal_etotnorm; Events;", 300, 0.0, 5);
#x h2_cal_vs_hgc = ROOT.TH2D("h2_cal_vs_hgc","Calorimeter VS HGC; P_cal_etotnorm; P_hgcer_npeSum;", 300, 0.0, 5, 300, 0.0, 30);

for evt in Pions_No_Cal_Cuts:
  h1_cal_etot.Fill(evt.P_cal_etotnorm); 

  #Histograms for not  cuts
  h1_hgcer_npeSum = ROOT.TH1D("h1_hgcer_npeSum","NPE vs Events; NPE; Events;", 300, 0.0, 30);
  h1_xAtCer = ROOT.TH1D("h1_xAtCer","xAtCer; xAtCer; Events;", 300, -40, 40);
  h1_yAtCer = ROOT.TH1D("h1_yAtCer","yAtCer; yAtCer; Events;", 300, -40, 40);
  h1_Cal = ROOT.TH1D("h1_Cal","Calorimeter; Cal; Events;", 300, 0.0, 10.0);
  h1_Prshower = ROOT.TH1D("h1_Prshower","Preshower; Prshower; Events;", 300, 0.0, 10.0);
  h1_Xgtr = ROOT.TH1D("h1_Xgtr","X gtr; X gtr ; Events;", 300, -3.0, 3.0);
  h1_Ygtr = ROOT.TH1D("h1_Ygtr","Y gtr; Y gtr ; Events;", 300, -3.0, 3.0);
  h1_P_etot = ROOT.TH1D("h1_P_etot","P_cal_etotnorm; P_cal_etotnorm; Events;", 300, 0.0, 10.0);
  h1_gtr_beta = ROOT.TH1D("h1_gtr_beta","P_gtr_beta; P_gtr_beta; Events;", 300, 0.0, 10.0);
  h1_gtr_p = ROOT.TH1D("h1_gtr_p","P_gtr_p; P_gtr_p; Events;", 300, -10.0, 10.0);
  h1_gtr_dp = ROOT.TH1D("h1_gtr_dp","P_gtr_dp; P_gtr_dp; Events;", 300, -30.0, 30.0);
  h1_gtr_xp = ROOT.TH1D("h1_gtr_xp","P_gtr_xp; P_gtr_xp; Events;", 300, -40.0, 40.0);
  h1_gtr_yp = ROOT.TH1D("h1_gtr_yp","P_gtr_yp; P_gtr_yp; Events;", 300, -40.0, 40.0);
  h1_CTime_ePi_ROC1 = ROOT.TH1D("h1_CTime_ePi_ROC1","CTime_ePiCoinTime_ROC1; CTime_ePiCoinTime_ROC1; Events;", 300, -10.0, 100.0);
  h1_CTime_eK_ROC1 = ROOT.TH1D("h1_CTime_eK_ROC1","CTime_eKCoinTime_ROC1; CTime_eKCoinTime_ROC1; Events;", 300, -10.0, 100.0);
  h1_CTime_eP_ROC1 = ROOT.TH1D("h1_CTime_eP_ROC1","CTime_epCoinTime_ROC1; CTime_epCoinTime_ROC1; Events;", 300, -10.0, 100.0);

for evt in SHMS_Events:
    h1_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);
    h1_xAtCer.Fill(evt.P_xAtCer);
    h1_yAtCer.Fill(evt.P_yAtCer);
    h1_Cal.Fill(evt.P_Cal/gtr_p);
    h1_Prshower.Fill(evt.P_Prshower/evt.P_gtr_p);
    h1_Xgtr.Fill(evt.P_gtr_x);
    h1_Ygtr.Fill(evt.P_gtr_y);
    h1_P_etot.Fill(evt.P_P_cal_etot);  
    h1_gtr_beta.Fill(evt.P_gtr_beta);  
    h1_gtr_p.Fill(evt.P_gtr_p);
    h1_gtr_dp.Fill(evt.P_gtr_dp);
    h1_gtr_xp.Fill(evt.P_gtr_xp);
    h1_gtr_yp.Fill(evt.P_gtr_yp);
    h1_CTime_ePi_ROC1.Fill(evt.CTime_ePi_ROC1);
    h1_CTime_eK_ROC1.Fill(evt.CTime_eK_ROC1);
    h1_CTime_eP_ROC1.Fill(evt.CTime_eP_ROC1);

#Histograms for cuts + no Cal, HGC and Aero cuts
h2_events_no_cal_hgc_cuts = ROOT.TH2D("h2_events_no_cal_hgc_cuts","Calorimeter VS HGC; P_cal_etotnorm; P_hgcer_npeSum;", 300, 0.0, 3.0, 300, 0.0, 30.0);
for evt in Events_no_cal_hgc_cuts:
  h2_events_no_cal_hgc_cuts.Fill(evt.P_cal_etotnorm, evt.P_hgcer_npeSum);


h2_events_no_cal_hgc_aero_cuts = ROOT.TH2D("h2_events_no_cal_hgc_aero_cuts","HGC vs Aero; P_hgcer_npeSum; P_aero_npeSum;", 300, 0.0, 30.0, 300, 0.0, 30.0);
h2_events_no_cal_aero_cuts = ROOT.TH2D("h2_events_no_cal_aero_cuts","Calorimeter VS Aero; P_cal_etotnorm; P_aero_npeSum;", 300, 0.0, 3.0, 300, 0.0, 30.0);
h3_events_no_cal_aero_cuts = ROOT.TH3D("h3_events_no_cal_aero_cuts","Aero; P_aero_xAtCer; P_aero_yAtCer;  P_aero_npeSum;", 300, -50, 50, 300, -50, 50, 300, 0, 30);

for evt in Events_no_cal_hgc_aero_cuts:
    h2_events_no_cal_hgc_aero_cuts.Fill(evt.P_hgcer_npeSum, evt.P_aero_npeSum);
    h2_events_no_cal_aero_cuts.Fill(evt.P_cal_etotnorm, evt.P_aero_npeSum);
    h3_events_no_cal_aero_cuts.Fill(evt.P_aero_xAtCer, evt.P_aero_yAtCer, evt.P_aero_npeSum);   

#Histograms for cuts + HGC cuts
#Pions
#1-D Histograms
h1_Pions_xAtCer = ROOT.TH1D("h1_Pions_xAtCer","HGC; P_hgcer_xAtCer; Events;", 300, -40, 40);
h1_Pions_yAtCer = ROOT.TH1D("h1_Pions_yAtCer","HGC; P_hgcer_yAtCer; Events;", 300, -40, 40);
h1_Pions_Prshower = ROOT.TH1D("h1_Pions_Prshower","Calorimeter; P_cal_pr_eplane; Events;", 300, 0.0, 10.0);
h1_Pions_Shower = ROOT.TH1D("h1_Pions_Shower","Calorimeter; P_cal_fly_earray; Events;", 300, 0.0, 10.0);
h1_Pions_Xgtr = ROOT.TH1D("h1_Pions_Xgtr","HGC; P_gtr_x ; Events;", 300, -3.0, 3.0);
h1_Pions_Ygtr = ROOT.TH1D("h1_Pions_Ygtr","HGC; P_gtr_y ; Events;", 300, -3.0, 3.0);
h1_Pions_P_etot = ROOT.TH1D("h1_Pions_P_etot","Calorimeter; P_cal_etotnorm; Events;", 300, 0.0, 10.0);
h1_Pions_gtr_beta = ROOT.TH1D("h1_Pions_gtr_beta","HGC; P_gtr_beta; Events;", 300, 0.0, 10.0);
h1_Pions_gtr_p = ROOT.TH1D("h1_Pions_gtr_p","HGC; P_gtr_p; Events;", 300, -10.0, 10.0);
h1_Pions_gtr_dp = ROOT.TH1D("h1_Pions_gtr_dp","HGC; P_gtr_dp; Events;", 300, -30.0, 30.0);
h1_Pions_gtr_xp = ROOT.TH1D("h1_Pions_gtr_xp","HGC; P_gtr_xp; Events;", 300, -40.0, 40.0);
h1_Pions_gtr_yp = ROOT.TH1D("h1_Pions_gtr_yp","HGC; P_gtr_yp; Events;", 300, -40.0, 40.0);
h1_Pions_CTime_ePi_ROC1 = ROOT.TH1D("h1_Pions_CTime_ePi_ROC1","CTime_ePiCoinTime_ROC1; CTime_ePiCoinTime_ROC1; Events;", 300, -10.0, 100.0);
h1_Pions_hgcer_npeSum = ROOT.TH1D("h1_Pions_hgcer_npeSum","HGC; P_hgcer_npeSum; Events;", 300, 0.0, 40);
h1_Pions_aero_npeSum = ROOT.TH1D("h1_Pions_aero_npeSum","Aero; P_aero_npeSum; Events;", 300, 0.0, 40);

#2-D Histograms
h3_Pions_XyAtCer_NPE = ROOT.TH3D("h3_Pions_XyAtCer_NPE","HGC; P_hgcer_xAtCer; P_hgcer_yAtCer; P_hgcer_npeSum", 300, -40, 40, 300, -40, 40, 300, 0.0, 30);
h2_Pions_XyAtCer = ROOT.TH2D("h2_Pions_XyAtCer","HGC; P_hgcer_yAtCer; P_hgcer_xAtCer;", 300, -40, 40, 300, -40, 40);
h2_Pions_Cal_Showers = ROOT.TH2D("h2_Pions_Cal_Showers","Calorimeter; P_cal_fly_earray; P_cal_pr_eplane;", 250, 0.0, 0.8, 250, 0.0, 0.7);
h2_Pions_XYgtr = ROOT.TH2D("h2_Pions_XYgtr","HGC; P_gtr_x ; P_gtr_y;", 250, -0.5, 0.8, 250, -2.5, 2.5);
h2_Pions_npeSum = ROOT.TH2D("h2_Pions_npeSum","HGC vs Aero; P_hgcer_npeSum ; P_aero_Sum;", 300, 0, 40, 300, 0, 40);

for evt in Pions:
    #2-D Histograms
    h3_Pions_XyAtCer_NPE.Fill(evt.P_hgcer_xAtCer, evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Pions_Cal_Showers.Fill(evt.P_cal_fly_earray/P_gtr_p, evt.P_cal_pr_eplane/evt.P_gtr_p);
    h2_Pions_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h2_Pions_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Pions_npeSum.Fill(evt.P_hgcer_npeSum, evt.P_aero_npeSum);
    # 1-D Histograms
    h1_Pions_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);
    h1_Pions_aero_npeSum.Fill(evt.P_aero_npeSum);     
    h1_Pions_xAtCer.Fill(evt.P_hgcer_xAtCer);
    h1_Pions_yAtCer.Fill(evt.P_hgcer_yAtCer);
    h1_Pions_Prshower.Fill(evt.P_cal_pr_eplane/evt.P_gtr_p);
    h1_Pions_Shower.Fill(evt.P_cal_fly_earray/evt.P_gtr_p);
    h1_Pions_Xgtr.Fill(evt.P_gtr_x);
    h1_Pions_Ygtr.Fill(evt.P_gtr_y);
    h1_Pions_gtr_beta.Fill(evt.P_gtr_beta);    
    h1_Pions_gtr_p.Fill(evt.P_gtr_p);
    h1_Pions_gtr_dp.Fill(evt.P_gtr_dp);
    h1_Pions_gtr_xp.Fill(evt.P_gtr_xp);
    h1_Pions_gtr_yp.Fill(evt.P_gtr_yp);
    h1_Pions_P_etot.Fill(evt.P_cal_etotnorm);  
    h1_Pions_CTime_ePi_ROC1.Fill(evt.CTime_ePiCoinTime_ROC1);

#Positrons
#1-D Histograms
h1_Positrons_xAtCer = ROOT.TH1D("h1_Positrons_xAtCer","HGC; P_hgcer_xAtCer; Events;", 300, -40, 40);
h1_Positrons_yAtCer = ROOT.TH1D("h1_Positrons_yAtCer","HGC; P_hgcer_yAtCer; Events;", 300, -40, 40);
h1_Positrons_Prshower = ROOT.TH1D("h1_Positrons_Prshower","Calorimeter; P_cal_pr_eplane; Events;", 300, 0.0, 10.0);
h1_Positrons_Shower = ROOT.TH1D("h1_Positrons_Shower","Calorimeter; P_cal_fly_earray; Events;", 300, 0.0, 10.0);
h1_Positrons_Xgtr = ROOT.TH1D("h1_Positrons_Xgtr","HGC; P_gtr_x ; Events;", 300, -3.0, 3.0);
h1_Positrons_Ygtr = ROOT.TH1D("h1_Positrons_Ygtr","HGC; P_gtr_y ; Events;", 300, -3.0, 3.0);
h1_Positrons_P_etot = ROOT.TH1D("h1_Positrons_P_etot","Calorimeter; P_cal_etotnorm; Events;", 300, 0.0, 10.0);
h1_Positrons_gtr_beta = ROOT.TH1D("h1_Positrons_gtr_beta","HGC; P_gtr_beta; Events;", 300, 0.0, 10.0);
h1_Positrons_gtr_p = ROOT.TH1D("h1_Positrons_gtr_p","HGC; P_gtr_p; Events;", 300, -10.0, 10.0);
h1_Positrons_gtr_dp = ROOT.TH1D("h1_Positrons_gtr_dp","HGC; P_gtr_dp; Events;", 300, -30.0, 30.0);
h1_Positrons_gtr_xp = ROOT.TH1D("h1_Positrons_gtr_xp","HGC; P_gtr_xp; Events;", 300, -40.0, 40.0);
h1_Positrons_gtr_yp = ROOT.TH1D("h1_Positrons_gtr_yp","HGC; P_gtr_yp; Events;", 300, -40.0, 40.0);
# h1_Pions_CTime_ePi_ROC1 = ROOT.TH1D("h1_Pions_CTime_ePi_ROC1","CTime_ePiCoinTime_ROC1; CTime_ePiCoinTime_ROC1; Events;", 300, -10.0, 100.0);
h1_Positrons_hgcer_npeSum = ROOT.TH1D("h1_Positrons_hgcer_npeSum","HGC; P_hgcer_npeSum; Events;", 300, 0.0, 40);
h1_Positrons_aero_npeSum = ROOT.TH1D("h1_Positrons_aero_npeSum","Aero; P_aero_npeSum; Events;", 300, 0.0, 40);

#2-D Histograms
h2_Positrons_XyAtCer = ROOT.TH2D("h2_Positrons_XyAtCer","HGC; P_hgcer_yAtCer; P_hgcer_xAtCer;", 300, -40, 40, 300, -40, 40);
h2_Positrons_Cal_Showers = ROOT.TH2D("h2_Positrons_Cal_Showers","Calorimeter; P_cal_fly_earray; P_cal_pr_eplane;", 250, 0.0, 1.5, 250, 0.0, 0.7);
h2_Positrons_XYgtr = ROOT.TH2D("h2_Positrons_XYgtr","HGC; P_gtr_x ; P_gtr_y;", 250, -0.5, 0.8, 250, -2.5, 2.5);

for evt in Positrons:
    #2-D Histograms
    h3_Positrons_XyAtCer_NPE.Fill(evt.P_hgcer_xAtCer, evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Positrons_Cal_Showers.Fill(evt.P_cal_fly_earray/P_gtr_p, evt.P_cal_pr_eplane/evt.P_gtr_p);
    h2_Positrons_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h2_Positrons_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Positrons_npeSum.Fill(evt.P_hgcer_npeSum, evt.P_aero_npeSum);
    # 1-D Histograms
    h1_Positrons_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);
    h1_Positrons_aero_npeSum.Fill(evt.P_aero_npeSum);     
    h1_Positrons_xAtCer.Fill(evt.P_hgcer_xAtCer);
    h1_Positrons_yAtCer.Fill(evt.P_hgcer_yAtCer);
    h1_Positrons_Prshower.Fill(evt.P_cal_pr_eplane/evt.P_gtr_p);
    h1_Positrons_Shower.Fill(evt.P_cal_fly_earray/evt.P_gtr_p);
    h1_Positrons_Xgtr.Fill(evt.P_gtr_x);
    h1_Positrons_Ygtr.Fill(evt.P_gtr_y);
    h1_Positrons_gtr_beta.Fill(evt.P_gtr_beta);    
    h1_Positrons_gtr_p.Fill(evt.P_gtr_p);
    h1_Positrons_gtr_dp.Fill(evt.P_gtr_dp);
    h1_Positrons_gtr_xp.Fill(evt.P_gtr_xp);
    h1_Positrons_gtr_yp.Fill(evt.P_gtr_yp);
    h1_Positrons_P_etot.Fill(evt.P_cal_etotnorm);  
    h1_Positrons_CTime_ePi_ROC1.Fill(evt.CTime_ePiCoinTime_ROC1);

#Histograms for cuts + HGC cuts
#Kaons
h1_Kaons_hgcer_npeSum = ROOT.TH1D("h1_Kaons_hgcer_npeSum","NPE vs Events; NPE; Events;", 300, 0.0, 40);
h2_Kaons_XyAtCer = ROOT.TH2D("h2_Kaons_XyAtCer","yAtCer vs xAtCer; yAtCer; xAtCer;", 200, -40, 40, 200, -40, 40);
h2_Kaons_Cal_Showers = ROOT.TH2D("h2_Kaons_Cal_Showers","Cal vs Pr-Shower; Cal; Pr-Shower;", 300, 0.0, 2.0, 300, 0.0, 1.0);
h2_Kaons_XYgtr = ROOT.TH2D("h2_Kaons_XYgtr","XY gtr; X gtr ; Y gtr;", 300, -3.0, 3.0, 300, -10, 10);

for evt in Kaons:
    h2_Kaons_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Kaons_Cal_Showers.Fill(evt.P_cal_fly_earray/6.053, evt.P_cal_pr_eplane/6.053);
    h2_Kaons_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h1_Kaons_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);

#Histograms for cuts + HGC cuts
#Protons
h1_Protons_hgcer_npeSum = ROOT.TH1D("h1_Protons_hgcer_npeSum","NPE vs Events; NPE; Events;", 300, 0.0, 40);
h2_Protons_XyAtCer = ROOT.TH2D("h2_Protons_XyAtCer","yAtCer vs xAtCer; yAtCer; xAtCer;", 200, -40, 40, 200, -40, 40);
h2_Protons_Cal_Showers = ROOT.TH2D("h2_Protons_Cal_Showers","Cal vs Pr-Shower; Cal; Pr-Shower;", 300, 0.0, 2.0, 300, 0.0, 1.0);
h2_Protons_XYgtr = ROOT.TH2D("h2_Protons_XYgtr","XY gtr; X gtr ; Y gtr;", 300, -3.0, 3.0, 300, -10, 10);

for evt in Protons:
    h2_Protons_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Protons_Cal_Showers.Fill(evt.P_cal_fly_earray/6.053, evt.P_cal_pr_eplane/6.053);
    h2_Protons_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h1_Protons_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);

#Histograms for cuts + no HGC cuts
#Pions
#1-D Histograms
h1_Pi_xAtCer = ROOT.TH1D("h1_Pi_xAtCer","HGC; P_hgcer_xAtCer; Events;", 300, -40, 40);
h1_Pi_yAtCer = ROOT.TH1D("h1_Pi_yAtCer","HGC; P_hgcer_yAtCer; Events;", 300, -40, 40);
h1_Pi_Prshower = ROOT.TH1D("h1_Pi_Prshower","Calorimeter; P_cal_pr_eplane; Events;", 300, 0.0, 10.0);
h1_Pi_Shower = ROOT.TH1D("h1_Pi_Shower","Calorimeter; P_cal_fly_earray; Events;", 300, 0.0, 10.0);
h1_Pi_Xgtr = ROOT.TH1D("h1_Pi_Xgtr","HGC; P_gtr_x ; Events;", 300, -3.0, 3.0);
h1_Pi_Ygtr = ROOT.TH1D("h1_Pi_Ygtr","HGC; P_gtr_y ; Events;", 300, -3.0, 3.0);
h1_Pi_P_etot = ROOT.TH1D("h1_Pi_P_etot","Calorimeter; P_cal_etotnorm; Events;", 300, 0.0, 10.0);
h1_Pi_gtr_beta = ROOT.TH1D("h1_Pi_gtr_beta","HGC; P_gtr_beta; Events;", 300, 0.0, 10.0);
h1_Pi_gtr_p = ROOT.TH1D("h1_Pi_gtr_p","HGC; P_gtr_p; Events;", 300, -10.0, 10.0);
h1_Pi_gtr_dp = ROOT.TH1D("h1_Pi_gtr_dp","HGC; P_gtr_dp; Events;", 300, -30.0, 30.0);
h1_Pi_gtr_xp = ROOT.TH1D("h1_Pi_gtr_xp","HGC; P_gtr_xp; Events;", 300, -40.0, 40.0);
h1_Pi_gtr_yp = ROOT.TH1D("h1_Pi_gtr_yp","HGC; P_gtr_yp; Events;", 300, -40.0, 40.0);
h1_Pi_CTime_ePi_ROC1 = ROOT.TH1D("h1_Pi_CTime_ePi_ROC1","CTime_ePiCoinTime_ROC1; CTime_ePiCoinTime_ROC1; Events;", 300, -10.0, 100.0);
h1_Pi_hgcer_npeSum = ROOT.TH1D("h1_Pi_hgcer_npeSum","HGC; P_hgcer_npeSum; Events;", 300, 0.0, 40);
h1_Pi_aero_npeSum = ROOT.TH1D("h1_Pi_aero_npeSum","Aero; P_aero_npeSum; Events;", 300, 0.0, 40);

#2-D Histograms
h3_Pi_XyAtCer_NPE = ROOT.TH3D("h3_Pi_XyAtCer_NPE","HGC; P_hgcer_xAtCer; P_hgcer_yAtCer; P_hgcer_npeSum", 300, -40, 40, 300, -40, 40, 300, 0.0, 30);    
h2_Pi_XyAtCer = ROOT.TH2D("h2_Pi_XyAtCer","HGC; P_hgcer_yAtCer; P_hgcer_xAtCer;", 300, -40, 40, 300, -40, 40);
h2_Pi_Cal_Showers = ROOT.TH2D("h2_Pi_Cal_Showers","Calorimeter; P_cal_fly_earray; P_cal_pr_eplane;", 250, 0.0, 0.8, 250, 0.0, 0.7);
h2_Pi_XYgtr = ROOT.TH2D("h2_Pi_XYgtr","HGC; P_gtr_x ; P_gtr_y;", 250, -0.5, 0.8, 250, -2.5, 2.5);

for evt in Pions_No_HGC_Cuts:
    #2-D Histograms
    h3_Pions_No_HGC_Cuts_XyAtCer_NPE.Fill(evt.P_hgcer_xAtCer, evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Pions_No_HGC_Cuts_Cal_Showers.Fill(evt.P_cal_fly_earray/P_gtr_p, evt.P_cal_pr_eplane/evt.P_gtr_p);
    h2_Pions_No_HGC_Cuts_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h2_Pions_No_HGC_Cuts_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Pions_No_HGC_Cuts_npeSum.Fill(evt.P_hgcer_npeSum, evt.P_aero_npeSum);
    # 1-D Histograms
    h1_Pions_No_HGC_Cuts_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);
    h1_Pions_No_HGC_Cuts_aero_npeSum.Fill(evt.P_aero_npeSum);     
    h1_Pions_No_HGC_Cuts_xAtCer.Fill(evt.P_hgcer_xAtCer);
    h1_Pions_No_HGC_Cuts_yAtCer.Fill(evt.P_hgcer_yAtCer);
    h1_Pions_No_HGC_Cuts_Prshower.Fill(evt.P_cal_pr_eplane/evt.P_gtr_p);
    h1_Pions_No_HGC_Cuts_Shower.Fill(evt.P_cal_fly_earray/evt.P_gtr_p);
    h1_Pions_No_HGC_Cuts_Xgtr.Fill(evt.P_gtr_x);
    h1_Pions_No_HGC_Cuts_Ygtr.Fill(evt.P_gtr_y);
    h1_Pions_No_HGC_Cuts_gtr_beta.Fill(evt.P_gtr_beta);    
    h1_Pions_No_HGC_Cuts_gtr_p.Fill(evt.P_gtr_p);
    h1_Pions_No_HGC_Cuts_gtr_dp.Fill(evt.P_gtr_dp);
    h1_Pions_No_HGC_Cuts_gtr_xp.Fill(evt.P_gtr_xp);
    h1_Pions_No_HGC_Cuts_gtr_yp.Fill(evt.P_gtr_yp);
    h1_Pions_No_HGC_Cuts_P_etot.Fill(evt.P_cal_etotnorm);  
    h1_Pions_No_HGC_Cuts_CTime_ePi_ROC1.Fill(evt.CTime_ePiCoinTime_ROC1);
    
#Positrons
#1-D Histograms
h1_Pos_xAtCer = ROOT.TH1D("h1_Pos_xAtCer","HGC; P_hgcer_xAtCer; Events;", 300, -40, 40);
h1_Pos_yAtCer = ROOT.TH1D("h1_Pos_yAtCer","HGC; P_hgcer_yAtCer; Events;", 300, -40, 40);
h1_Pos_Prshower = ROOT.TH1D("h1_Pos_Prshower","Calorimeter; P_cal_pr_eplane; Events;", 300, 0.0, 10.0);
h1_Pos_Shower = ROOT.TH1D("h1_Pos_Shower","Calorimeter; P_cal_fly_earray; Events;", 300, 0.0, 10.0);
h1_Pos_Xgtr = ROOT.TH1D("h1_Pos_Xgtr","HGC; P_gtr_x ; Events;", 300, -3.0, 3.0);
h1_Pos_Ygtr = ROOT.TH1D("h1_Pos_Ygtr","HGC; P_gtr_y ; Events;", 300, -3.0, 3.0);
h1_Pos_P_etot = ROOT.TH1D("h1_Pos_P_etot","Calorimeter; P_cal_etotnorm; Events;", 300, 0.0, 10.0);
h1_Pos_gtr_beta = ROOT.TH1D("h1_Pos_gtr_beta","HGC; P_gtr_beta; Events;", 300, 0.0, 10.0);
h1_Pos_gtr_p = ROOT.TH1D("h1_Pos_gtr_p","HGC; P_gtr_p; Events;", 300, -10.0, 10.0);
h1_Pos_gtr_dp = ROOT.TH1D("h1_Pos_gtr_dp","HGC; P_gtr_dp; Events;", 300, -30.0, 30.0);
h1_Pos_gtr_xp = ROOT.TH1D("h1_Pos_gtr_xp","HGC; P_gtr_xp; Events;", 300, -40.0, 40.0);
h1_Pos_gtr_yp = ROOT.TH1D("h1_Pos_gtr_yp","HGC; P_gtr_yp; Events;", 300, -40.0, 40.0);
# h1_Pos_CTime_ePi_ROC1 = ROOT.TH1D("h1_Pi_CTime_ePi_ROC1","CTime_ePiCoinTime_ROC1; CTime_ePiCoinTime_ROC1; Events;", 300, -10.0, 100.0);
h1_Pos_hgcer_npeSum = ROOT.TH1D("h1_Pos_hgcer_npeSum","HGC; P_hgcer_npeSum; Events;", 300, 0.0, 40);
h1_Pos_aero_npeSum = ROOT.TH1D("h1_Pos_aero_npeSum","Aero; P_aero_npeSum; Events;", 300, 0.0, 40);

#2-D Histograms
h2_Pos_XyAtCer = ROOT.TH2D("h2_Pos_XyAtCer","HGC; P_hgcer_yAtCer; P_hgcer_xAtCer;", 300, -40, 40, 300, -40, 40);
h2_Pos_Cal_Showers = ROOT.TH2D("h2_Pos_Cal_Showers","Calorimeter; P_cal_fly_earray; P_cal_pr_eplane;", 250, 0.0, 1.5, 250, 0.0, 0.7);
h2_Pos_XYgtr = ROOT.TH2D("h2_Pos_XYgtr","HGC; P_gtr_x ; P_gtr_y;", 250, -0.5, 0.8, 250, -2.5, 2.5);

for evt in Positrons_No_HGC_Cuts:
    #2-D Histograms
    h3_Positrons_No_HGC_Cuts_XyAtCer_NPE.Fill(evt.P_hgcer_xAtCer, evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Positrons_No_HGC_Cuts_Cal_Showers.Fill(evt.P_cal_fly_earray/P_gtr_p, evt.P_cal_pr_eplane/evt.P_gtr_p);
    h2_Positrons_No_HGC_Cuts_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h2_Positrons_No_HGC_Cuts_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Positrons_No_HGC_Cuts_npeSum.Fill(evt.P_hgcer_npeSum, evt.P_aero_npeSum);
    # 1-D Histograms
    h1_Positrons_No_HGC_Cuts_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);
    h1_Positrons_No_HGC_Cuts_aero_npeSum.Fill(evt.P_aero_npeSum);     
    h1_Positrons_No_HGC_Cuts_xAtCer.Fill(evt.P_hgcer_xAtCer);
    h1_Positrons_No_HGC_Cuts_yAtCer.Fill(evt.P_hgcer_yAtCer);
    h1_Positrons_No_HGC_Cuts_Prshower.Fill(evt.P_cal_pr_eplane/evt.P_gtr_p);
    h1_Positrons_No_HGC_Cuts_Shower.Fill(evt.P_cal_fly_earray/evt.P_gtr_p);
    h1_Positrons_No_HGC_Cuts_Xgtr.Fill(evt.P_gtr_x);
    h1_Positrons_No_HGC_Cuts_Ygtr.Fill(evt.P_gtr_y);
    h1_Positrons_No_HGC_Cuts_gtr_beta.Fill(evt.P_gtr_beta);    
    h1_Positrons_No_HGC_Cuts_gtr_p.Fill(evt.P_gtr_p);
    h1_Positrons_No_HGC_Cuts_gtr_dp.Fill(evt.P_gtr_dp);
    h1_Positrons_No_HGC_Cuts_gtr_xp.Fill(evt.P_gtr_xp);
    h1_Positrons_No_HGC_Cuts_gtr_yp.Fill(evt.P_gtr_yp);
    h1_Positrons_No_HGC_Cuts_P_etot.Fill(evt.P_cal_etotnorm);  
    h1_Positrons_No_HGC_Cuts_CTime_ePi_ROC1.Fill(evt.CTime_ePiCoinTime_ROC1);

h1_Kaons_No_HGC_Cuts_hgcer_npeSum = ROOT.TH1D("h1_Kaons_No_HGC_Cuts_hgcer_npeSum","NPE vs Events; NPE; Events;", 300, 0.0, 40);
h2_Kaons_No_HGC_Cuts_XyAtCer = ROOT.TH2D("h2_Kaons_No_HGC_Cuts_XyAtCer","yAtCer vs xAtCer; yAtCer; xAtCer;", 200, -40, 40, 200, -40, 40);
h2_Kaons_No_HGC_Cuts_Cal_Showers = ROOT.TH2D("h2_Kaons_No_HGC_Cuts_Cal_Showers","Cal vs Pr-Shower; Cal; Pr-Shower;", 300, 0.0, 2.0, 300, 0.0, 1.0);
h2_Kaons_No_HGC_Cuts_XYgtr = ROOT.TH2D("h2_Kaons_No_HGC_Cuts_XYgtr","XY gtr; X gtr ; Y gtr;", 300, -3.0, 3.0, 300, -10, 10);

for evt in Kaons_No_HGC_Cuts:
    h2_Kaons_No_HGC_Cuts_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Kaons_No_HGC_Cuts_Cal_Showers.Fill(evt.P_cal_fly_earray/6.053, evt.P_cal_pr_eplane/6.053);
    h2_Kaons_No_HGC_Cuts_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h1_Kaons_No_HGC_Cuts_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);

h1_Protons_No_HGC_Cuts_hgcer_npeSum = ROOT.TH1D("h1_Protons_No_HGC_Cuts_hgcer_npeSum","NPE vs Events; NPE; Events;", 300, 0.0, 40);
h2_Protons_No_HGC_Cuts_XyAtCer = ROOT.TH2D("h2_Protons_No_HGC_Cuts_XyAtCer","yAtCer vs xAtCer; yAtCer; xAtCer;", 200, -40, 40, 200, -40, 40);
h2_Protons_No_HGC_Cuts_Cal_Showers = ROOT.TH2D("h2_Protons_No_HGC_Cuts_Cal_Showers","Cal vs Pr-Shower; Cal; Pr-Shower;", 300, 0.0, 2.0, 300, 0.0, 1.0);
h2_Protons_No_HGC_Cuts_XYgtr = ROOT.TH2D("h2_Protons_No_HGC_Cuts_XYgtr","XY gtr; X gtr ; Y gtr;", 300, -3.0, 3.0, 300, -10, 10);

for evt in Protons_No_HGC_Cuts:
    h2_Protons_No_HGC_Cuts_XyAtCer.Fill(evt.P_hgcer_yAtCer, evt.P_hgcer_xAtCer);
    h2_Protons_No_HGC_Cuts_Cal_Showers.Fill(evt.P_cal_fly_earray/6.053, evt.P_cal_pr_eplane/6.053);
    h2_Protons_No_HGC_Cuts_XYgtr.Fill(evt.P_gtr_x, evt.P_gtr_y);
    h1_Protons_No_HGC_Cuts_hgcer_npeSum.Fill(evt.P_hgcer_npeSum);

'''

'''
h = ROOT.TH2D("h","XY gtr; X gtr ; Y gtr;", 300, 0.0, 30.0, 300, 0, 30);
for evt in Events_no_cal_hgc_aero_cuts:
    if !cutg2.IsInside(P_no_cal_hgc_aero_cuts_hgcer_yAtCer, P_no_cal_hgc_aero_cuts_hgcer_xAtCer):
        continue;
    h.Fill(evt.P_no_cal_hgc_aero_cuts_hgcer_npeSum, evt.P_no_cal_hgc_aero_cuts_aero_npeSum);
'''

#################################################################################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE); # Set ROOT to batch mode explicitly, does not splash anything to screen
#################################################################################################################################################

c_CT = TCanvas("c_CT", "HGC (with TCutG)");  
c_CT.Divide(2,2);   
c_CT.cd(1);
Events_no_cal_hgc_aero_cuts.Draw("P_hgcer_npeSum:P_aero_npeSum>>h1(300,0.0,30,300,0,30)", "cutg",  "colz");
c_CT.cd(2);
Events_no_cal_hgc_aero_cuts.Draw("P_hgcer_npeSum>>h2(300,0.3,30)", "cutg",  "colz");
c_CT.cd(3);
Events_no_cal_hgc_aero_cuts.Draw("P_hgcer_npeSum:P_aero_npeSum>>h3(300,0,30, 300, 0, 30)", "!cutg",  "colz"); 
c_CT.cd(4);
Events_no_cal_hgc_aero_cuts.Draw("P_hgcer_npeSum>>h4(300,0.3,30)", "!cutg",  "colz"); 
c_CT.Print(foutpdf);

#################################################################################################################################################

#  TProfile2D h3_Pions_XyAtCer_NPE = Project3DProfile("xy") 
OutHisto_file = ROOT.TFile.Open(foutname,"RECREATE");
Pions_info = OutHisto_file.mkdir("Pions_info");
Pions_info.cd();

# Pions_XyAtCer_NPE;
# Pions_XyAtCer_NPE = dynamic_cast<TH3D*> (GetOutputList().FindObject("h3_Pions_XyAtCer_NPE"));
h3_Pions_XyAtCer_NPE_pxy = ROOT.TProfile2D("h3_Pions_XyAtCer_NPE_pxy","NPE vs X vs Y; X ; Y ",300,-40,40, 300,-40,40,0.0,40);
h3_Pions_XyAtCer_NPE.Project3DProfile("xy");

h3_Pi_XyAtCer_NPE_pxy = ROOT.TProfile2D("h3_Pi_XyAtCer_NPE_pxy","NPE vs X vs Y; X ; Y ",300,-40,40, 300,-40,40,0.0,40);
h3_Pi_XyAtCer_NPE.Project3DProfile("xy");

h3_events_no_cal_aero_cuts_pxy = ROOT.TProfile2D("h3_events_no_cal_aero_cuts_pxy","NPE vs X vs Y; X ; Y ",300,-50,50, 300,-50,50,0.0,30);
h3_events_no_cal_aero_cuts.Project3DProfile("xy");

#2-D Histograms
h3_Pions_XyAtCer_NPE_pxy.GetListOfFunctions().Add(cutg,"L"); 
h3_Pions_XyAtCer_NPE_pxy.Write();
#Pions_XyAtCer_NPE.Write();
# h3_Pions_XyAtCer_NPE.Write();
h2_Pions_Cal_Showers.Write();
h2_Pions_XYgtr.Write();
h2_Pions_XyAtCer.GetListOfFunctions().Add(cutg,"L"); 
h2_Pions_XyAtCer.Write();
#    h2_Pions_npeSum.GetListOfFunctions().Add(cutg1,"L");
h2_Pions_npeSum.Write();
#1-D Histograms
h1_Pions_hgcer_npeSum.Write();
h1_Pions_aero_npeSum.Write();   
h1_Pions_xAtCer.Write();
h1_Pions_yAtCer.Write();
h1_Pions_Shower.Write();
h1_Pions_Prshower.Write();
h1_Pions_Xgtr.Write();
h1_Pions_Ygtr.Write();
h1_Pions_P_etot.Write();
h1_Pions_gtr_beta.Write();
h1_Pions_gtr_p.Write();
h1_Pions_gtr_dp.Write();
h1_Pions_gtr_xp.Write();  
h1_Pions_gtr_yp.Write();  
h1_Pions_CTime_ePi_ROC1.Write();  

Positrons_info = OutHisto_file.mkdir("Positrons_info");

Positrons_info.cd();
#2-D Histograms
h2_Positrons_XyAtCer.Write();
h2_Positrons_Cal_Showers.Write();
h2_Positrons_XYgtr.Write();

#1-D Histograms
h1_Positrons_hgcer_npeSum.Write();
h1_Positrons_aero_npeSum.Write();   
h1_Positrons_xAtCer.Write();
h1_Positrons_yAtCer.Write();
h1_Positrons_Shower.Write();
h1_Positrons_Prshower.Write();
h1_Positrons_Xgtr.Write();
h1_Positrons_Ygtr.Write();
h1_Positrons_P_etot.Write();
h1_Positrons_gtr_beta.Write();
h1_Positrons_gtr_p.Write();
h1_Positrons_gtr_dp.Write();
h1_Positrons_gtr_xp.Write();  
h1_Positrons_gtr_yp.Write();  
#h1_Pions_CTime_ePi_ROC1.Write();  


Kaons_info = OutHisto_file.mkdir("Kaons_info");

Kaons_info.cd();
h2_Kaons_XyAtCer.Write();
h2_Kaons_Cal_Showers.Write();
h2_Kaons_XYgtr.Write();
h1_Kaons_hgcer_npeSum.Write();

Protons_info = OutHisto_file.mkdir("Protons_info");

Protons_info.cd();
h2_Protons_XyAtCer.Write();
h2_Protons_Cal_Showers.Write();
h2_Protons_XYgtr.Write();
h1_Protons_hgcer_npeSum.Write();

Pions_No_HGC_Cuts_info = OutHisto_file.mkdir("Pions_No_HGC_Cuts_info");

Pions_No_HGC_Cuts_info.cd();

#2-D Histograms
h3_Pi_XyAtCer_NPE_pxy.GetListOfFunctions().Add(cutg,"L");       
h3_Pi_XyAtCer_NPE_pxy.Write();
h2_Pi_Cal_Showers.Write();
h2_Pi_XYgtr.Write();
h2_Pi_XyAtCer.GetListOfFunctions().Add(cutg,"L"); 
h2_Pi_XyAtCer.Write();
#1-D Histograms
h1_Pi_hgcer_npeSum.Write();
h1_Pi_aero_npeSum.Write();   
h1_Pi_xAtCer.Write();
h1_Pi_yAtCer.Write();
h1_Pi_Shower.Write();
h1_Pi_Prshower.Write();
h1_Pi_Xgtr.Write();
h1_Pi_Ygtr.Write();
h1_Pi_P_etot.Write();
h1_Pi_gtr_beta.Write();
h1_Pi_gtr_p.Write();
h1_Pi_gtr_dp.Write();
h1_Pi_gtr_xp.Write();  
h1_Pi_gtr_yp.Write();  
h1_Pi_CTime_ePi_ROC1.Write();  

Positrons_No_HGC_Cuts_info = OutHisto_file.mkdir("Positrons_No_HGC_Cuts_info");

Positrons_No_HGC_Cuts_info.cd();

#2-D Histograms
h2_Pos_XyAtCer.Write();
h2_Pos_Cal_Showers.Write();
h2_Pos_XYgtr.Write();

#1-D Histograms
h1_Pos_hgcer_npeSum.Write();
h1_Pos_aero_npeSum.Write();   
h1_Pos_xAtCer.Write();
h1_Pos_yAtCer.Write();
h1_Pos_Shower.Write();
h1_Pos_Prshower.Write();
h1_Pos_Xgtr.Write();
h1_Pos_Ygtr.Write();
h1_Pos_P_etot.Write();
h1_Pos_gtr_beta.Write();
h1_Pos_gtr_p.Write();
h1_Pos_gtr_dp.Write();
h1_Pos_gtr_xp.Write();  
h1_Pos_gtr_yp.Write();  
#h1_Pos_CTime_ePi_ROC1.Write();  


Kaons_No_HGC_Cuts_info = OutHisto_file.mkdir("Kaons_No_HGC_Cuts_info");

Kaons_No_HGC_Cuts_info.cd();
h2_Kaons_No_HGC_Cuts_XyAtCer.Write();
h2_Kaons_No_HGC_Cuts_Cal_Showers.Write();
h2_Kaons_No_HGC_Cuts_XYgtr.Write();
h1_Kaons_No_HGC_Cuts_hgcer_npeSum.Write();
Protons_No_HGC_Cuts_info = OutHisto_file.mkdir("Protons_No_HGC_Cuts_info");

Protons_No_HGC_Cuts_info.cd();
h2_Protons_No_HGC_Cuts_XyAtCer.Write();
h2_Protons_No_HGC_Cuts_Cal_Showers.Write();
h2_Protons_No_HGC_Cuts_XYgtr.Write();
h1_Protons_No_HGC_Cuts_hgcer_npeSum.Write();

SHMS_Events_No_Cuts = OutHisto_file.mkdir("SHMS_Events_No_Cuts");

SHMS_Events_No_Cuts.cd();
h1_xAtCer.Write();
h1_yAtCer.Write();
h1_Cal.Write();
h1_Prshower.Write();
h1_Xgtr.Write();
h1_Ygtr.Write();
h1_hgcer_npeSum.Write();
h1_P_etot.Write();
h1_gtr_beta.Write();
h1_gtr_p.Write();
h1_gtr_dp.Write();
h1_gtr_xp.Write();  
h1_gtr_yp.Write();  
h1_CTime_ePi_ROC1.Write();  
h1_CTime_eK_ROC1.Write();  
h1_CTime_eP_ROC1.Write();  

SHMS_Events_No_Aero_Cuts = OutHisto_file.mkdir("SHMS_Events_No_Aero_Cuts");

SHMS_Events_No_Aero_Cuts.cd();

h1_aero_npeSum.Write();

SHMS_Events_No_Cal_HGC_Aero_Cuts = OutHisto_file.mkdir("SHMS_Events_No_Cal_HGC_Aero_Cuts");
SHMS_Events_No_Cal_HGC_Aero_Cuts.cd();

h1_cal_etot.Write();
h2_events_no_cal_hgc_cuts.Write();
# h2_events_no_cal_hgc_aero_cuts.GetListOfFunctions().Add(cutg,"L"); 
#h2_events_no_cal_hgc_aero_cuts.Write();
h2_events_no_cal_aero_cuts.Write();
h3_events_no_cal_aero_cuts_pxy.Write();
h.Write(); 
OutHisto_file.Close();
