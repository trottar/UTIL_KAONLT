#! /usr/bin/python
#
# Description:
# ================================================================
# Time-stamp: "2022-06-29 09:28:05 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import uproot as up
import sys

from .cut import SetCuts 
from .pathing import SetPath

#########################
# Cython implimentation #
#from .setcut import *  
#########################

class InvalidEntry(Exception):
    '''
    Raise this exception when something goes wrong with the cuts
    '''
    pass

class Root():
    '''    
    Root()

    ----------------------------------------------------------------------------------------------
    ################################################################################################################################################
    \'''
    Define and set up cuts
    \'''

    import ltsep as lt

    p=lt.SetPath(os.path.realpath(__file__))

    # Add this to all files for more dynamic pathing
    VOLATILEPATH=p.getPath("VOLATILEPATH")
    ANALYSISPATH=p.getPath("ANALYSISPATH")
    HCANAPATH=p.getPath("HCANAPATH")
    REPLAYPATH=p.getPath("REPLAYPATH")
    UTILPATH=p.getPath("UTILPATH")
    PACKAGEPATH=p.getPath("PACKAGEPATH")
    OUTPATH=p.getPath("OUTPATH")
    ROOTPATH=p.getPath("ROOTPATH")
    REPORTPATH=p.getPath("REPORTPATH")
    CUTPATH=p.getPath("CUTPATH")
    PARAMPATH=p.getPath("PARAMPATH")
    SCRIPTPATH=p.getPath("SCRIPTPATH")
    SIMCPATH=p.getPath("SIMCPATH")
    ANATYPE=p.getPath("ANATYPE")
    USER=p.getPath("USER")
    HOST=p.getPath("HOST")

    # ---> If multple run type files are required then define a new run type file altogether. Do not try to 
    # chain run type files. It can be done, but is computationally wasteful and pointless.
    cut_f = "<path_to_run_type_cut>"

    cuts = ["runTypeCut1","runTypeCut2",<etc>,...]

    # To apply cuts to array and define pathing variables...
    # Arrays are defined in ltsep, no need to redefine.
    # cut_f, cuts are optional flags. If you don't have cuts just leave these blank and the runtype root branches will be accessible
    # ROOTPrefix is also an optional flag but this means your branches will need to be defined explicitly
    proc_root = lt.Root(os.path.realpath(__file__), "<Run Type (HeePCoin, HeePSing_<spec>, SimcCoin, SimcSing, KaonLT/PionLT, Plot_<Type>, None)>", ROOTPrefix, runNum, MaxEvent, cut_f, cuts).setup_ana()
    c = proc_root[0] # Cut object
    tree = proc_root[1] # Dictionary of branches
    OUTPATH = proc_root[2] # Get pathing for OUTPATH
    strDict = proc_root[3] # Dictionary of cuts as strings

    # ----> See lt.Help.path_setup() for more info

    ################################################################################################################################################
    \'''
    If you wish to explicitly define arrays then do the following...
    \'''

    import uproot as up
    # Convert root leaf to array with uproot
    leaf_name  = tree.array("leaf.name") # The periods are replaced with underscores

    ----------------------------------------------------------------------------------------------

    This is the most extensive class of the ltsep package. This class will grab many of the required 
    tasks for doing in depth analysis in python such as define pathing variables and cuts.
    '''

    def __init__(self, CURRENT_ENV, runType="None", ROOTPrefix="", runNum="-1", MaxEvent="-1", cut_f="", cuts=None, DEBUG=False):
        '''
        __init__(self, CURRENT_ENV, ROOTPrefix, runType, runNum, MaxEvent, cut_f, cuts=None, DEBUG=False)
                       |            |           |        |       |         |      |          |
                       |            |           |        |       |         |      |          --> DEBUG: Set true to show debug output
                       |            |           |        |       |         |      --> cuts: 
                       |            |           |        |       |         --> cut_f:
                       |            |           |        |       --> MaxEvent:
                       |            |           |        --> runNum:
                       |            |           --> runType:
                       |            --> ROOTPrefix:
                       --> CURRENT_ENV: Input current enviroment path

        ----------------------------------------------------------------------------------------------
        
        Constructor of class takes the current enviroment path and an optional dictionary as input
        '''
        self.DEBUG = DEBUG
        self.ROOTPrefix = ROOTPrefix
        self.runNum = runNum
        self.MaxEvent = MaxEvent
        self.cuts = cuts
        self.CURRENT_ENV = CURRENT_ENV    
        self.runType = runType

        # Defines dynamic pathing variables
        self.VOLATILEPATH=SetPath(self.CURRENT_ENV).getPath("VOLATILEPATH")
        self.ANALYSISPATH=SetPath(self.CURRENT_ENV).getPath("ANALYSISPATH")
        self.HCANAPATH=SetPath(self.CURRENT_ENV).getPath("HCANAPATH")
        self.REPLAYPATH=SetPath(self.CURRENT_ENV).getPath("REPLAYPATH")
        self.UTILPATH=SetPath(self.CURRENT_ENV).getPath("UTILPATH")
        self.PACKAGEPATH=SetPath(self.CURRENT_ENV).getPath("PACKAGEPATH")
        self.OUTPATH=SetPath(self.CURRENT_ENV).getPath("OUTPATH")
        self.ROOTPATH=SetPath(self.CURRENT_ENV).getPath("ROOTPATH")
        self.REPORTPATH=SetPath(self.CURRENT_ENV).getPath("REPORTPATH")
        self.CUTPATH=SetPath(self.CURRENT_ENV).getPath("CUTPATH")
        self.PARAMPATH=SetPath(self.CURRENT_ENV).getPath("PARAMPATH")
        self.SCRIPTPATH=SetPath(self.CURRENT_ENV).getPath("SCRIPTPATH")
        self.SIMCPATH=SetPath(self.CURRENT_ENV).getPath("SIMCPATH")
        self.ANATYPE=SetPath(self.CURRENT_ENV).getPath("ANATYPE")
        self.USER=SetPath(self.CURRENT_ENV).getPath("USER")
        self.HOST=SetPath(self.CURRENT_ENV).getPath("HOST",self.DEBUG)

        ################################################################################################################################################
        '''
        Defines Output pathing and cut location
        '''

        self.cut_f = self.UTILPATH+cut_f

        # Add more path setting as needed in a similar manner
        if "HeeP" in self.runType:
            self.OUTPATH = "%s/OUTPUT/Analysis/HeeP" % self.UTILPATH      # Output folder location
        elif "Simc" in self.runType:
            self.OUTPATH = "%s/OUTPUT/Analysis/HeeP" % self.SIMCPATH      # Output folder location
        elif "Prod" in self.runType:
            self.OUTPATH = "%s/OUTPUT/Analysis/%sLT" % (self.UTILPATH,self.ANATYPE)      # Output folder location
        elif "Hodo" in self.runType:
            self.OUTPATH = "%s/OUTPUT/Calib/Hodo" % self.UTILPATH      # Output folder location
        else:
            self.OUTPATH = "%s/OUTPUT/Analysis/%s" % (self.UTILPATH, self.runType)      # Output folder location
        self.CUTPATH = "%s/DB/CUTS" % self.UTILPATH

        ################################################################################################################################################
        '''
        Check that root/output paths and files exist for use
        '''

        if self.ROOTPrefix is not "":
            if "Plot" in self.runType:
                # Construct the name of the rootfile based upon the info we provided
                if "Prod" in self.runType:
                    self.rootName = "%s/OUTPUT/Analysis/%sLT/%s_%s_%s.root" % (self.UTILPATH, self.ANATYPE, self.runNum, self.MaxEvent, self.ROOTPrefix,)     # Input file location and variables taking
                elif "HeeP" in self.runType:
                    self.rootName = "%s/OUTPUT/Analysis/HeeP/%s_%s_%s.root" % (self.UTILPATH, self.runNum, self.MaxEvent, self.ROOTPrefix,)     # Input file location and variables taking
                elif "Simc" in self.runType:
                    self.rootName = "%s/OUTPUT/Analysis/HeeP/%s_%s_%s.root" % (self.UTILPATH, self.runNum, self.MaxEvent, self.ROOTPrefix,)     # Input file location and variables taking
                else:
                    self.rootName = "%s/OUTPUT/Analysis/%s/%s_%s_%s.root" % (self.UTILPATH, self.runType, self.runNum, self.MaxEvent, self.ROOTPrefix)     # Input file location and variables taking
                print ("Attempting to process %s" %(self.rootName))
                SetPath(self.CURRENT_ENV).checkDir(self.OUTPATH)
                SetPath(self.CURRENT_ENV).checkFile(self.rootName)
                print("Output path checks out, outputting to %s" % (self.OUTPATH))
            else:
                # Construct the name of the rootfile based upon the info we provided
                if "Prod" in self.runType:
                    self.rootName = "%s/ROOTfiles/Analysis/%sLT/%s_%s_%s.root" % (self.UTILPATH, self.ANATYPE, self.ROOTPrefix, self.runNum, self.MaxEvent)     # Input file location and variables taking
                elif "Hodo" in self.runType:
                    self.rootName = "%s/ROOTfiles/Analysis/%sLT/%s_%s_%s.root" % (self.UTILPATH, self.ANATYPE, self.ROOTPrefix, self.runNum, self.MaxEvent)     # Input file location and variables taking
                elif "HeeP" in self.runType:
                    self.rootName = "%s/ROOTfiles/Analysis/HeeP/%s_%s_%s.root" % (self.UTILPATH, self.ROOTPrefix, self.runNum, self.MaxEvent)     # Input file location and variables taking
                elif "Simc" in self.runType:
                    self.rootName = "%s/ROOTfiles/Analysis/HeeP/%s_%s_%s.root" % (self.UTILPATH, self.ROOTPrefix, self.runNum, self.MaxEvent)     # Input file location and variables taking
                else:
                    self.rootName = "%s/ROOTfiles/Analysis/%s/%s_%s_%s.root" % (self.UTILPATH, self.runType, self.ROOTPrefix, self.runNum, self.MaxEvent)     # Input file location and variables taking
                print ("Attempting to process %s" %(self.rootName))
                SetPath(self.CURRENT_ENV).checkDir(self.OUTPATH)
                SetPath(self.CURRENT_ENV).checkFile(self.rootName)
                print("Output path checks out, outputting to %s" % (self.OUTPATH))

        ################################################################################################################################################


    def __str__(self):
        '''
        __str__(self)

        ----------------------------------------------------------------------------------------------

        String representation of class if called as string (eg print(SetCuts))
        '''

        return "{REPLAYPATH : {self.REPLAYPATH}, UTILPATH : {self.UTILPATH}}"

    def __repr__(self):
        '''
        __repr__(self)

        ----------------------------------------------------------------------------------------------

        String representation of class if called as is (eg SetCuts)
        '''

        return "Root([{self.REPLAYPATH},{self.UTILPATH}])"  

    def setup_ana(self):
        '''
        This method brings all the data together and makes it accessible to the script. It calls the other 
        methods to define cuts. It also defines pathing variables and grabs dictionary of branches.
        '''

        # Make cut dictionary and convert to boolean list for cut application
        make_cutDict = self.make_cutDict()
        bool_cuts = make_cutDict[0]

        # Get dictionary of branch names
        treeDict = make_cutDict[1]

        # Get dictionary of cut names and values as strings
        strDict = make_cutDict[2]

        return [bool_cuts,treeDict,strDict]


    def make_cutDict(self):
        '''
        This method calls several methods in kaonlt package. It is required to create properly formated
        dictionaries. The evaluation must be in the analysis script because the analysis variables (i.e. the
        leaves of interest) are not defined in the kaonlt package. This makes the system more flexible
        overall, but a bit more cumbersome in the analysis script. Perhaps one day a better solution will be
        implimented.
        '''

        e_tree = up.open(self.rootName)["T"]

        # Define arrays from root file based off run type
        if "Coin" in self.runType:

            #################################################################################################################

            # Timing info
            CTime_epCoinTime_ROC1 = e_tree.array("CTime.epCoinTime_ROC1")    #
            #P_RF_tdcTime = e_tree.array("T.coin.pRF_tdcTime")               #
            #P_hod_fpHitsTime = e_tree.array("P.hod.fpHitsTime")             #
            H_RF_Dist = e_tree.array("RFTime.HMS_RFtimeDist")                #
            P_RF_Dist = e_tree.array("RFTime.SHMS_RFtimeDist")               #

            # HMS info
            H_dc_InsideDipoleExit = e_tree.array("H.dc.InsideDipoleExit")    #
            H_hod_goodscinhit = e_tree.array("H.hod.goodscinhit")            #
            H_hod_goodstarttime = e_tree.array("H.hod.goodstarttime")        #
            H_gtr_beta = e_tree.array("H.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
            H_dc_x_fp = e_tree.array("H.dc.x_fp")                            #
            H_dc_y_fp = e_tree.array("H.dc.y_fp")                            #
            H_dc_xp_fp = e_tree.array("H.dc.xp_fp")                          #
            H_dc_yp_fp = e_tree.array("H.dc.yp_fp")                          #
            H_gtr_xp = e_tree.array("H.gtr.th")                              # xpfp -> Theta
            H_gtr_yp = e_tree.array("H.gtr.ph")                              # ypfp -> Phi
            H_gtr_dp = e_tree.array("H.gtr.dp")                              # dp is Delta
            H_gtr_p = e_tree.array("H.gtr.p")                                # 
            H_cal_etotnorm = e_tree.array("H.cal.etotnorm")                  #
            H_cal_etottracknorm = e_tree.array("H.cal.etottracknorm")        #
            H_cer_npeSum = e_tree.array("H.cer.npeSum")                      #

            # SHMS info
            P_dc_InsideDipoleExit = e_tree.array("P.dc.InsideDipoleExit")    #
            P_hod_goodscinhit = e_tree.array("P.hod.goodscinhit")            #
            P_hod_goodstarttime = e_tree.array("P.hod.goodstarttime")        #
            P_gtr_beta = e_tree.array("P.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
            P_dc_x_fp = e_tree.array("P.dc.x_fp")                            #
            P_dc_y_fp = e_tree.array("P.dc.y_fp")                            #
            P_dc_xp_fp = e_tree.array("P.dc.xp_fp")                          #
            P_dc_yp_fp = e_tree.array("P.dc.yp_fp")                          #
            P_gtr_xp = e_tree.array("P.gtr.th")                              # xpfp -> Theta
            P_gtr_yp = e_tree.array("P.gtr.ph")                              # ypfp -> Phi
            P_gtr_p = e_tree.array("P.gtr.p")                                #
            P_gtr_dp = e_tree.array("P.gtr.dp")                              # dp is Delta 
            P_cal_etotnorm = e_tree.array("P.cal.etotnorm")                  #
            P_cal_etottracknorm = e_tree.array("P.cal.etottracknorm")        #
            P_aero_npeSum = e_tree.array("P.aero.npeSum")                    #
            P_aero_xAtAero = e_tree.array("P.aero.xAtAero")                  #
            P_aero_yAtAero = e_tree.array("P.aero.yAtAero")                  #
            P_hgcer_npeSum = e_tree.array("P.hgcer.npeSum")                  #
            P_hgcer_xAtCer = e_tree.array("P.hgcer.xAtCer")                  #
            P_hgcer_yAtCer = e_tree.array("P.hgcer.yAtCer")                  #

            # Kinematic quantitites
            Q2 = e_tree.array("H.kin.primary.Q2")                            #
            W = e_tree.array("H.kin.primary.W")                              #
            epsilon = e_tree.array("H.kin.primary.epsilon")                  #
            ph_q = e_tree.array("P.kin.secondary.ph_xq")                     #
            emiss = e_tree.array("P.kin.secondary.emiss")                    #
            #pmiss = e_tree.array("P.kin.secondary.pmiss")                   #
            MMpi = e_tree.array("P.kin.secondary.MMpi")                      #
            MMK = e_tree.array("P.kin.secondary.MMK")                        #
            MMp = e_tree.array("P.kin.secondary.MMp")                        #
            MandelT = e_tree.array("P.kin.secondary.MandelT")                #
            #MandelU = e_tree.array("P.kin.secondary.MandelU")               #
            pmiss = e_tree.array("P.kin.secondary.pmiss")                    #
            pmiss_x = e_tree.array("P.kin.secondary.pmiss_x")                #
            pmiss_y = e_tree.array("P.kin.secondary.pmiss_y")                #
            pmiss_z = e_tree.array("P.kin.secondary.pmiss_z")                #

            # Misc quantities
            #fEvtType = e_tree.array("fEvtHdr.fEvtType")                     #
            #RFFreq = e_tree.array("MOFC1FREQ")                              #
            #RFFreqDiff = e_tree.array("MOFC1DELTA")                         #
            #pEDTM = e_tree.array("T.coin.pEDTM_tdcTime")                    #
            # Relevant branches now stored as NP arrays

            treeDict = {
                "CTime_epCoinTime_ROC1" : CTime_epCoinTime_ROC1,
                "H_RF_Dist" : H_RF_Dist,
                "P_RF_Dist" : P_RF_Dist,
                "H_dc_InsideDipoleExit" : H_dc_InsideDipoleExit,
                "H_hod_goodscinhit" : H_hod_goodscinhit,
                "H_hod_goodstarttime" : H_hod_goodstarttime,
                "H_gtr_beta" : H_gtr_beta,
                "H_dc_x_fp" : H_dc_x_fp,
                "H_dc_y_fp" : H_dc_y_fp,
                "H_dc_xp_fp" : H_dc_xp_fp,
                "H_dc_yp_fp" : H_dc_yp_fp,
                "H_gtr_xp" : H_gtr_xp,
                "H_gtr_yp" : H_gtr_yp,
                "H_gtr_dp" : H_gtr_dp,
                "H_gtr_p" : H_gtr_p,
                "H_cal_etotnorm" : H_cal_etotnorm,
                "H_cal_etottracknorm" : H_cal_etottracknorm,
                "H_cer_npeSum" : H_cer_npeSum,
                "P_dc_InsideDipoleExit" : P_dc_InsideDipoleExit,
                "P_hod_goodscinhit" : P_hod_goodscinhit,
                "P_hod_goodstarttime" : P_hod_goodstarttime,
                "P_gtr_beta" : P_gtr_beta,
                "P_dc_x_fp" : P_dc_x_fp,
                "P_dc_y_fp" : P_dc_y_fp,
                "P_dc_xp_fp" : P_dc_xp_fp,
                "P_dc_yp_fp" : P_dc_yp_fp,
                "P_gtr_xp" : P_gtr_xp,
                "P_gtr_yp" : P_gtr_yp,
                "P_gtr_p" : P_gtr_p,
                "P_gtr_dp" : P_gtr_dp,
                "P_cal_etotnorm" : P_cal_etotnorm,
                "P_cal_etottracknorm" : P_cal_etottracknorm,
                "P_aero_npeSum" : P_aero_npeSum,
                "P_aero_xAtAero" : P_aero_xAtAero,
                "P_aero_yAtAero" : P_aero_yAtAero,
                "P_hgcer_npeSum" : P_hgcer_npeSum,
                "P_hgcer_xAtCer" : P_hgcer_xAtCer,
                "P_hgcer_yAtCer" : P_hgcer_yAtCer,
                "Q2" : Q2,
                "W" : W,
                "epsilon" : epsilon,
                "ph_q" : ph_q,
                "emiss" : emiss,
                "MMpi" : MMpi,
                "MMK" : MMK,
                "MMp" : MMp,
                "MandelT" : MandelT,
                "pmiss" : pmiss,
                "pmiss_x" : pmiss_x,
                "pmiss_y" : pmiss_y,
                "pmiss_z" : pmiss_z,
            }

        elif "hgcer" in self.runType:

            CTime_eKCoinTime_ROC1           = e_tree.array("CTime.eKCoinTime_ROC1")
            CTime_ePiCoinTime_ROC1          = e_tree.array("CTime.ePiCoinTime_ROC1")
            CTime_epCoinTime_ROC1           = e_tree.array("CTime.epCoinTime_ROC1")
            H_cal_etotnorm                  = e_tree.array("H.cal.etotnorm")
            P_hgcer_npe                     = e_tree.array("P.hgcer.npe")
            P_cal_fly_earray                = e_tree.array("P.cal.fly.earray")
            P_cal_pr_eplane                 = e_tree.array("P.cal.pr.eplane")
            P_gtr_beta                      = e_tree.array("P.gtr.beta")
            P_gtr_xp                        = e_tree.array("P.gtr.th") # xpfp -> Theta
            P_gtr_yp                        = e_tree.array("P.gtr.ph") # ypfp -> Phi
            P_gtr_p                         = e_tree.array("P.gtr.p")
            P_gtr_dp                        = e_tree.array("P.gtr.dp")
            P_cal_etotnorm                  = e_tree.array("P.cal.etotnorm")
            P_aero_npeSum                   = e_tree.array("P.aero.npeSum")
            P_hgcer_npeSum                  = e_tree.array("P.hgcer.npeSum")
            P_hgcer_xAtCer                  = e_tree.array("P.hgcer.xAtCer")
            P_hgcer_yAtCer                  = e_tree.array("P.hgcer.yAtCer")
            P_aero_xAtCer                   = e_tree.array("P.aero.xAtAero")
            P_aero_yAtCer                   = e_tree.array("P.aero.yAtAero")
            P_gtr_x                         = e_tree.array("P.gtr.x")
            P_gtr_y                         = e_tree.array("P.gtr.y")
            emiss                           = e_tree.array("P.kin.secondary.emiss") 
            pmiss                           = e_tree.array("P.kin.secondary.pmiss")

            treeDict = {
            "CTime_eKCoinTime_ROC1" : CTime_eKCoinTime_ROC1,
            "CTime_ePiCoinTime_ROC1" : CTime_ePiCoinTime_ROC1,
            "CTime_epCoinTime_ROC1" : CTime_epCoinTime_ROC1,
            "H_cal_etotnorm" : H_cal_etotnorm,
            "P_hgcer_npe" : P_hgcer_npe,
            "P_cal_fly_earray" : P_cal_fly_earray,
            "P_cal_pr_eplane" : P_cal_pr_eplane,
            "P_gtr_beta" : P_gtr_beta,
            "P_gtr_xp" : P_gtr_xp,
            "P_gtr_yp" : P_gtr_yp,
            "P_gtr_p" : P_gtr_p,
            "P_gtr_dp" : P_gtr_dp,
            "P_cal_etotnorm" : P_cal_etotnorm,
            "P_aero_npeSum" : P_aero_npeSum,
            "P_hgcer_npeSum" : P_hgcer_npeSum,
            "P_hgcer_xAtCer" : P_hgcer_xAtCer,
            "P_hgcer_yAtCer" : P_hgcer_yAtCer,
            "P_aero_xAtCer" : P_aero_xAtCer,
            "P_aero_yAtCer" : P_aero_yAtCer,
            "P_gtr_x" : P_gtr_x,
            "P_gtr_y" : P_gtr_y,
            "emiss" : emiss,
            "pmiss" : pmiss,

            }

        elif "Sing" in self.runType:

            if "SHMS" in self.runType:
                
                # SHMS info
                P_RF_Dist = e_tree.array("RFTime.SHMS_RFtimeDist")               #
                P_dc_InsideDipoleExit = e_tree.array("P.dc.InsideDipoleExit")    #
                P_hod_goodscinhit = e_tree.array("P.hod.goodscinhit")            #
                P_hod_goodstarttime = e_tree.array("P.hod.goodstarttime")        #
                P_gtr_beta = e_tree.array("P.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
                P_dc_x_fp = e_tree.array("P.dc.x_fp")                            #
                P_dc_y_fp = e_tree.array("P.dc.y_fp")                            #
                P_dc_xp_fp = e_tree.array("P.dc.xp_fp")                          #
                P_dc_yp_fp = e_tree.array("P.dc.yp_fp")                          #
                P_gtr_xp = e_tree.array("P.gtr.th")                              # xpfp -> Theta
                P_gtr_yp = e_tree.array("P.gtr.ph")                              # ypfp -> Phi
                P_gtr_p = e_tree.array("P.gtr.p")                                #
                P_gtr_dp = e_tree.array("P.gtr.dp")                              # dp is Delta 
                P_cal_etotnorm = e_tree.array("P.cal.etotnorm")                  #
                P_cal_etottracknorm = e_tree.array("P.cal.etottracknorm")        #
                P_aero_npeSum = e_tree.array("P.aero.npeSum")                    #
                P_aero_xAtAero = e_tree.array("P.aero.xAtAero")                  #
                P_aero_yAtAero = e_tree.array("P.aero.yAtAero")                  #
                P_hgcer_npeSum = e_tree.array("P.hgcer.npeSum")                  #
                P_hgcer_xAtCer = e_tree.array("P.hgcer.xAtCer")                  #
                P_hgcer_yAtCer = e_tree.array("P.hgcer.yAtCer")                  #
                emiss = e_tree.array("P.kin.secondary.emiss")                   
                pmiss = e_tree.array("P.kin.secondary.pmiss")                   
                MMpi = e_tree.array("P.kin.secondary.MMpi")                      
                W = e_tree.array("P.kin.primary.W")                              
                pmiss_x = e_tree.array("P.kin.secondary.pmiss_x")                
                pmiss_y = e_tree.array("P.kin.secondary.pmiss_y")                
                pmiss_z = e_tree.array("P.kin.secondary.pmiss_z")  

                treeDict = {
                    "P_RF_Dist" : P_RF_Dist,
                    "P_dc_InsideDipoleExit" : P_dc_InsideDipoleExit,
                    "P_hod_goodscinhit" : P_hod_goodscinhit,
                    "P_hod_goodstarttime" : P_hod_goodstarttime,
                    "P_gtr_beta" : P_gtr_beta,
                    "P_dc_x_fp" : P_dc_x_fp,
                    "P_dc_y_fp" : P_dc_y_fp,
                    "P_dc_xp_fp" : P_dc_xp_fp,
                    "P_dc_yp_fp" : P_dc_yp_fp,
                    "P_gtr_xp" : P_gtr_xp,
                    "P_gtr_yp" : P_gtr_yp,
                    "P_gtr_p" : P_gtr_p,
                    "P_gtr_dp" : P_gtr_dp,
                    "P_cal_etotnorm" : P_cal_etotnorm,
                    "P_cal_etottracknorm" : P_cal_etottracknorm,
                    "P_aero_npeSum" : P_aero_npeSum,
                    "P_aero_xAtAero" : P_aero_xAtAero,
                    "P_aero_yAtAero" : P_aero_yAtAero,
                    "P_hgcer_npeSum" : P_hgcer_npeSum,
                    "P_hgcer_xAtCer" : P_hgcer_xAtCer,
                    "P_hgcer_yAtCer" : P_hgcer_yAtCer,
                    "emiss" : emiss,
                    "pmiss" : pmiss,
                    "MMpi" : MMpi,
                    "W" : W,
                    "pmiss_x" : pmiss_x,
                    "pmiss_y" : pmiss_y,
                    "pmiss_z" : pmiss_z,
                }

            #if "HMS" in self.runType:
            else:

                # HMS info
                H_RF_Dist = e_tree.array("RFTime.HMS_RFtimeDist")                #
                H_dc_InsideDipoleExit = e_tree.array("H.dc.InsideDipoleExit")    #
                H_hod_goodscinhit = e_tree.array("H.hod.goodscinhit")            #
                H_hod_goodstarttime = e_tree.array("H.hod.goodstarttime")        #
                H_gtr_beta = e_tree.array("H.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
                H_dc_x_fp = e_tree.array("H.dc.x_fp")                            #
                H_dc_y_fp = e_tree.array("H.dc.y_fp")                            #
                H_dc_xp_fp = e_tree.array("H.dc.xp_fp")                          #
                H_dc_yp_fp = e_tree.array("H.dc.yp_fp")                          #
                H_gtr_xp = e_tree.array("H.gtr.th")                              # xpfp -> Theta
                H_gtr_yp = e_tree.array("H.gtr.ph")                              # ypfp -> Phi
                H_gtr_dp = e_tree.array("H.gtr.dp")                              # dp is Delta
                H_gtr_p = e_tree.array("H.gtr.p")                                # 
                H_cal_etotnorm = e_tree.array("H.cal.etotnorm")                  #
                H_cal_etottracknorm = e_tree.array("H.cal.etottracknorm")        #
                H_cer_npeSum = e_tree.array("H.cer.npeSum")                      #
                H_W = e_tree.array("H.kin.primary.W")                            #

                treeDict = {
                    "H_RF_Dist" : H_RF_Dist,
                    "H_dc_InsideDipoleExit" : H_dc_InsideDipoleExit,
                    "H_hod_goodscinhit" : H_hod_goodscinhit,
                    "H_hod_goodstarttime" : H_hod_goodstarttime,
                    "H_gtr_beta" : H_gtr_beta,
                    "H_dc_x_fp" : H_dc_x_fp,
                    "H_dc_y_fp" : H_dc_y_fp,
                    "H_dc_xp_fp" : H_dc_xp_fp,
                    "H_dc_yp_fp" : H_dc_yp_fp,
                    "H_gtr_xp" : H_gtr_xp,
                    "H_gtr_yp" : H_gtr_yp,
                    "H_gtr_dp" : H_gtr_dp,
                    "H_gtr_p" : H_gtr_p,
                    "H_cal_etotnorm" : H_cal_etotnorm,
                    "H_cal_etottracknorm" : H_cal_etottracknorm,
                    "H_cer_npeSum" : H_cer_npeSum,
                    "H_W" : H_W,
                }  

        elif "Hodo" in self.runType:

            if "SHMS" in self.runType:
                
                # SHMS info
                P_gtr_beta = e_tree.array("P.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
                P_dc_x_fp = e_tree.array("P.dc.x_fp")                            #
                P_dc_y_fp = e_tree.array("P.dc.y_fp")                            #
                P_gtr_dp = e_tree.array("P.gtr.dp")                              # dp is Delta 

                treeDict = {
                    "P_gtr_beta" : P_gtr_beta,
                    "P_dc_x_fp" : P_dc_x_fp,
                    "P_dc_y_fp" : P_dc_y_fp,
                    "P_gtr_dp" : P_gtr_dp,
                }

            #if "HMS" in self.runType:
            else:

                # HMS info
                H_gtr_beta = e_tree.array("H.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
                H_dc_x_fp = e_tree.array("H.dc.x_fp")                            #
                H_dc_y_fp = e_tree.array("H.dc.y_fp")                            #
                H_gtr_dp = e_tree.array("H.gtr.dp")                              # dp is Delta 

                treeDict = {
                    "H_gtr_beta" : H_gtr_beta,
                    "H_dc_x_fp" : H_dc_x_fp,
                    "H_dc_y_fp" : H_dc_y_fp,
                    "H_gtr_dp" : H_gtr_dp,
                }

        elif "Lumi" in self.runType:

            P_cal_etotnorm = e_tree.array("P.cal.etotnorm")
            P_hgcer_npeSum = e_tree.array("P.hgcer.npeSum")
            P_aero_npeSum = e_tree.array("P.aero.npeSum")
            P_gtr_dp = e_tree.array("P.gtr.dp")
            P_gtr_th = e_tree.array("P.gtr.th")
            P_gtr_ph = e_tree.array("P.gtr.ph")
            P_gtr_beta = e_tree.array("P.gtr.beta")
            P_tr_chi2 = e_tree.array("P.tr.chi2")
            P_tr_ndof = e_tree.array("P.tr.ndof")
            P_hod_goodscinhit = e_tree.array("P.hod.goodscinhit")
            P_hod_betanotrack = e_tree.array("P.hod.betanotrack")
            P_hod_goodstarttime = e_tree.array("P.hod.goodstarttime")
            P_dc_ntrack = e_tree.array("P.dc.ntrack")
            if self.ANATYPE == "Pion":
                P_ngcer_npeSum = e_tree.array("P.ngcer.npeSum")

            P_dc_1x1_nhit = e_tree.array("P.dc.1x1.nhit")
            P_dc_1u2_nhit = e_tree.array("P.dc.1u2.nhit")
            P_dc_1u1_nhit = e_tree.array("P.dc.1u1.nhit")
            P_dc_1v1_nhit = e_tree.array("P.dc.1v1.nhit")
            P_dc_1x2_nhit = e_tree.array("P.dc.1x2.nhit")
            P_dc_1v2_nhit = e_tree.array("P.dc.1v2.nhit")
            P_dc_2x1_nhit = e_tree.array("P.dc.2x1.nhit")
            P_dc_2u2_nhit = e_tree.array("P.dc.2u2.nhit")
            P_dc_2u1_nhit = e_tree.array("P.dc.2u1.nhit")
            P_dc_2v1_nhit = e_tree.array("P.dc.2v1.nhit")
            P_dc_2x2_nhit = e_tree.array("P.dc.2x2.nhit")
            P_dc_2v2_nhit = e_tree.array("P.dc.2v2.nhit")

            P_cal_etottracknorm = e_tree.array("P.cal.etottracknorm")

            H_cal_etotnorm = e_tree.array("H.cal.etotnorm")
            H_cer_npeSum = e_tree.array("H.cer.npeSum")
            H_gtr_dp = e_tree.array("H.gtr.dp")
            H_tr_tg_th = e_tree.array("H.gtr.th")
            H_tr_tg_ph = e_tree.array("H.gtr.ph")
            H_gtr_beta = e_tree.array("H.gtr.beta")
            H_tr_chi2 = e_tree.array("H.tr.chi2")
            H_tr_ndof = e_tree.array("H.tr.ndof")
            H_hod_goodscinhit = e_tree.array("H.hod.goodscinhit")
            H_hod_betanotrack = e_tree.array("H.hod.betanotrack")
            H_hod_goodstarttime = e_tree.array("H.hod.goodstarttime")
            H_dc_ntrack = e_tree.array("H.dc.ntrack")

            H_dc_1x1_nhit = e_tree.array("H.dc.1x1.nhit")
            H_dc_1u2_nhit = e_tree.array("H.dc.1u2.nhit")
            H_dc_1u1_nhit = e_tree.array("H.dc.1u1.nhit")
            H_dc_1v1_nhit = e_tree.array("H.dc.1v1.nhit")
            H_dc_1x2_nhit = e_tree.array("H.dc.1x2.nhit")
            H_dc_1v2_nhit = e_tree.array("H.dc.1v2.nhit")
            H_dc_2x1_nhit = e_tree.array("H.dc.2x1.nhit")
            H_dc_2u2_nhit = e_tree.array("H.dc.2u2.nhit")
            H_dc_2u1_nhit = e_tree.array("H.dc.2u1.nhit")
            H_dc_2v1_nhit = e_tree.array("H.dc.2v1.nhit")
            H_dc_2x2_nhit = e_tree.array("H.dc.2x2.nhit")
            H_dc_2v2_nhit = e_tree.array("H.dc.2v2.nhit")

            H_cal_etottracknorm = e_tree.array("H.cal.etottracknorm")

            if self.ANATYPE == "Pion":
                armDict = {
                    "P_cal_etotnorm" : P_cal_etotnorm,
                    "P_hgcer_npeSum" : P_hgcer_npeSum,
                    "P_aero_npeSum" : P_aero_npeSum,
                    "P_gtr_dp" : P_gtr_dp,
                    "P_gtr_th" : P_gtr_th,
                    "P_gtr_ph" : P_gtr_ph,
                    "P_gtr_beta" : P_gtr_beta,
                    "P_tr_chi2" : P_tr_chi2,
                    "P_tr_ndof" : P_tr_ndof,
                    "P_hod_goodscinhit" : P_hod_goodscinhit,
                    "P_hod_betanotrack" : P_hod_betanotrack,
                    "P_hod_goodstarttime" : P_hod_goodstarttime,
                    "P_dc_ntrack" : P_dc_ntrack,

                    "P_ngcer_npeSum" : P_ngcer_npeSum,

                    "P_dc_1x1_nhit" : P_dc_1x1_nhit,
                    "P_dc_1u2_nhit" : P_dc_1u2_nhit,
                    "P_dc_1u1_nhit" : P_dc_1u1_nhit,
                    "P_dc_1v1_nhit" : P_dc_1v1_nhit,
                    "P_dc_1x2_nhit" : P_dc_1x2_nhit,
                    "P_dc_1v2_nhit" : P_dc_1v2_nhit,
                    "P_dc_2x1_nhit" : P_dc_2x1_nhit,
                    "P_dc_2u2_nhit" : P_dc_2u2_nhit,
                    "P_dc_2u1_nhit" : P_dc_2u1_nhit,
                    "P_dc_2v1_nhit" : P_dc_2v1_nhit,
                    "P_dc_2x2_nhit" : P_dc_2x2_nhit,
                    "P_dc_2v2_nhit" : P_dc_2v2_nhit,

                    "P_cal_etottracknorm" : P_cal_etottracknorm,

                    "H_cal_etotnorm" : H_cal_etotnorm,
                    "H_cer_npeSum" : H_cer_npeSum,
                    "H_gtr_dp" : H_gtr_dp,
                    "H_tr_tg_th" : H_tr_tg_th,
                    "H_tr_tg_ph" : H_tr_tg_ph,
                    "H_gtr_beta" : H_gtr_beta,
                    "H_tr_chi2" : H_tr_chi2,
                    "H_tr_ndof" : H_tr_ndof,
                    "H_hod_goodscinhit" : H_hod_goodscinhit,
                    "H_hod_betanotrack" : H_hod_betanotrack,
                    "H_hod_goodstarttime" : H_hod_goodstarttime,
                    "H_dc_ntrack" : H_dc_ntrack,

                    "H_dc_1x1_nhit" : H_dc_1x1_nhit,
                    "H_dc_1u2_nhit" : H_dc_1u2_nhit,
                    "H_dc_1u1_nhit" : H_dc_1u1_nhit,
                    "H_dc_1v1_nhit" : H_dc_1v1_nhit,
                    "H_dc_1x2_nhit" : H_dc_1x2_nhit,
                    "H_dc_1v2_nhit" : H_dc_1v2_nhit,
                    "H_dc_2x1_nhit" : H_dc_2x1_nhit,
                    "H_dc_2u2_nhit" : H_dc_2u2_nhit,
                    "H_dc_2u1_nhit" : H_dc_2u1_nhit,
                    "H_dc_2v1_nhit" : H_dc_2v1_nhit,
                    "H_dc_2x2_nhit" : H_dc_2x2_nhit,
                    "H_dc_2v2_nhit" : H_dc_2v2_nhit,

                    "H_cal_etottracknorm" : H_cal_etottracknorm,

                }

            else:
                armDict = {
                    "P_cal_etotnorm" : P_cal_etotnorm,
                    "P_hgcer_npeSum" : P_hgcer_npeSum,
                    "P_aero_npeSum" : P_aero_npeSum,
                    "P_gtr_dp" : P_gtr_dp,
                    "P_gtr_th" : P_gtr_th,
                    "P_gtr_ph" : P_gtr_ph,
                    "P_gtr_beta" : P_gtr_beta,
                    "P_tr_chi2" : P_tr_chi2,
                    "P_tr_ndof" : P_tr_ndof,
                    "P_hod_goodscinhit" : P_hod_goodscinhit,
                    "P_hod_betanotrack" : P_hod_betanotrack,
                    "P_hod_goodstarttime" : P_hod_goodstarttime,
                    "P_dc_ntrack" : P_dc_ntrack,

                    "P_dc_1x1_nhit" : P_dc_1x1_nhit,
                    "P_dc_1u2_nhit" : P_dc_1u2_nhit,
                    "P_dc_1u1_nhit" : P_dc_1u1_nhit,
                    "P_dc_1v1_nhit" : P_dc_1v1_nhit,
                    "P_dc_1x2_nhit" : P_dc_1x2_nhit,
                    "P_dc_1v2_nhit" : P_dc_1v2_nhit,
                    "P_dc_2x1_nhit" : P_dc_2x1_nhit,
                    "P_dc_2u2_nhit" : P_dc_2u2_nhit,
                    "P_dc_2u1_nhit" : P_dc_2u1_nhit,
                    "P_dc_2v1_nhit" : P_dc_2v1_nhit,
                    "P_dc_2x2_nhit" : P_dc_2x2_nhit,
                    "P_dc_2v2_nhit" : P_dc_2v2_nhit,

                    "P_cal_etottracknorm" : P_cal_etottracknorm,

                    "H_cal_etotnorm" : H_cal_etotnorm,
                    "H_cer_npeSum" : H_cer_npeSum,
                    "H_gtr_dp" : H_gtr_dp,
                    "H_tr_tg_th" : H_tr_tg_th,
                    "H_tr_tg_ph" : H_tr_tg_ph,
                    "H_gtr_beta" : H_gtr_beta,
                    "H_tr_chi2" : H_tr_chi2,
                    "H_tr_ndof" : H_tr_ndof,
                    "H_hod_goodscinhit" : H_hod_goodscinhit,
                    "H_hod_betanotrack" : H_hod_betanotrack,
                    "H_hod_goodstarttime" : H_hod_goodstarttime,
                    "H_dc_ntrack" : H_dc_ntrack,

                    "H_dc_1x1_nhit" : H_dc_1x1_nhit,
                    "H_dc_1u2_nhit" : H_dc_1u2_nhit,
                    "H_dc_1u1_nhit" : H_dc_1u1_nhit,
                    "H_dc_1v1_nhit" : H_dc_1v1_nhit,
                    "H_dc_1x2_nhit" : H_dc_1x2_nhit,
                    "H_dc_1v2_nhit" : H_dc_1v2_nhit,
                    "H_dc_2x1_nhit" : H_dc_2x1_nhit,
                    "H_dc_2u2_nhit" : H_dc_2u2_nhit,
                    "H_dc_2u1_nhit" : H_dc_2u1_nhit,
                    "H_dc_2v1_nhit" : H_dc_2v1_nhit,
                    "H_dc_2x2_nhit" : H_dc_2x2_nhit,
                    "H_dc_2v2_nhit" : H_dc_2v2_nhit,

                    "H_cal_etottracknorm" : H_cal_etottracknorm,

                }

            H_bcm_bcm1_AvgCurrent = e_tree.array("H.bcm.bcm1.AvgCurrent")
            H_bcm_bcm2_AvgCurrent = e_tree.array("H.bcm.bcm2.AvgCurrent")
            H_bcm_bcm4a_AvgCurrent = e_tree.array("H.bcm.bcm4a.AvgCurrent")
            H_bcm_bcm4b_AvgCurrent = e_tree.array("H.bcm.bcm4b.AvgCurrent")
            H_bcm_bcm4c_AvgCurrent = e_tree.array("H.bcm.bcm4c.AvgCurrent")

            T_coin_pTRIG1_ROC1_tdcTimeRaw = e_tree.array("T.coin.pTRIG1_ROC1_tdcTimeRaw")
            T_coin_pTRIG1_ROC2_tdcTimeRaw = e_tree.array("T.coin.pTRIG1_ROC2_tdcTimeRaw")
            T_coin_pTRIG1_ROC1_tdcTime = e_tree.array("T.coin.pTRIG1_ROC1_tdcTime")
            T_coin_pTRIG1_ROC2_tdcTime = e_tree.array("T.coin.pTRIG1_ROC2_tdcTime")

            T_coin_pTRIG2_ROC1_tdcTimeRaw = e_tree.array("T.coin.pTRIG2_ROC1_tdcTimeRaw")
            T_coin_pTRIG2_ROC2_tdcTimeRaw = e_tree.array("T.coin.pTRIG2_ROC2_tdcTimeRaw")
            T_coin_pTRIG2_ROC1_tdcTime = e_tree.array("T.coin.pTRIG2_ROC1_tdcTime")
            T_coin_pTRIG2_ROC2_tdcTime = e_tree.array("T.coin.pTRIG2_ROC2_tdcTime")

            T_coin_pTRIG3_ROC1_tdcTimeRaw = e_tree.array("T.coin.pTRIG3_ROC1_tdcTimeRaw")
            T_coin_pTRIG3_ROC2_tdcTimeRaw = e_tree.array("T.coin.pTRIG3_ROC2_tdcTimeRaw")
            T_coin_pTRIG3_ROC1_tdcTime = e_tree.array("T.coin.pTRIG3_ROC1_tdcTime")
            T_coin_pTRIG3_ROC2_tdcTime = e_tree.array("T.coin.pTRIG3_ROC2_tdcTime")

            T_coin_pTRIG4_ROC1_tdcTimeRaw = e_tree.array("T.coin.pTRIG4_ROC1_tdcTimeRaw")
            T_coin_pTRIG4_ROC2_tdcTimeRaw = e_tree.array("T.coin.pTRIG4_ROC2_tdcTimeRaw")
            T_coin_pTRIG4_ROC1_tdcTime = e_tree.array("T.coin.pTRIG4_ROC1_tdcTime")
            T_coin_pTRIG4_ROC2_tdcTime = e_tree.array("T.coin.pTRIG4_ROC2_tdcTime")

            T_coin_pTRIG5_ROC1_tdcTimeRaw = e_tree.array("T.coin.pTRIG5_ROC1_tdcTimeRaw")
            T_coin_pTRIG5_ROC2_tdcTimeRaw = e_tree.array("T.coin.pTRIG5_ROC2_tdcTimeRaw")
            T_coin_pTRIG5_ROC1_tdcTime = e_tree.array("T.coin.pTRIG5_ROC1_tdcTime")
            T_coin_pTRIG5_ROC2_tdcTime = e_tree.array("T.coin.pTRIG5_ROC2_tdcTime")

            T_coin_pTRIG6_ROC1_tdcTimeRaw = e_tree.array("T.coin.pTRIG6_ROC1_tdcTimeRaw")
            T_coin_pTRIG6_ROC2_tdcTimeRaw = e_tree.array("T.coin.pTRIG6_ROC2_tdcTimeRaw")
            T_coin_pTRIG6_ROC1_tdcTime = e_tree.array("T.coin.pTRIG6_ROC1_tdcTime")
            T_coin_pTRIG6_ROC2_tdcTime = e_tree.array("T.coin.pTRIG6_ROC2_tdcTime")

            T_coin_pFADC_TREF_ROC2_adcPed = e_tree.array("T.coin.pFADC_TREF_ROC2_adcPed")
            T_coin_hFADC_TREF_ROC1_adcPed = e_tree.array("T.coin.hFADC_TREF_ROC1_adcPed")
            T_coin_pFADC_TREF_ROC2_adcPulseTimeRaw = e_tree.array("T.coin.pFADC_TREF_ROC2_adcPulseTimeRaw")
            T_coin_hFADC_TREF_ROC1_adcPulseTimeRaw = e_tree.array("T.coin.hFADC_TREF_ROC1_adcPulseTimeRaw")
            T_coin_pEDTM_tdcTimeRaw = e_tree.array("T.coin.pEDTM_tdcTimeRaw")
            T_coin_pEDTM_tdcTime = e_tree.array("T.coin.pEDTM_tdcTime")
            EvtType = e_tree.array("fEvtHdr.fEvtType")

            treeDict = {
                "H_bcm_bcm1_AvgCurrent" : H_bcm_bcm1_AvgCurrent,
                "H_bcm_bcm2_AvgCurrent" : H_bcm_bcm2_AvgCurrent,
                "H_bcm_bcm4a_AvgCurrent" : H_bcm_bcm4a_AvgCurrent,
                "H_bcm_bcm4b_AvgCurrent" : H_bcm_bcm4b_AvgCurrent,
                "H_bcm_bcm4c_AvgCurrent" : H_bcm_bcm4c_AvgCurrent,


                "T_coin_pTRIG1_ROC1_tdcTimeRaw" : T_coin_pTRIG1_ROC1_tdcTimeRaw,
                "T_coin_pTRIG1_ROC2_tdcTimeRaw" : T_coin_pTRIG1_ROC2_tdcTimeRaw,
                "T_coin_pTRIG1_ROC1_tdcTime" : T_coin_pTRIG1_ROC1_tdcTime,
                "T_coin_pTRIG1_ROC2_tdcTime" : T_coin_pTRIG1_ROC2_tdcTime,

                "T_coin_pTRIG2_ROC1_tdcTimeRaw" : T_coin_pTRIG2_ROC1_tdcTimeRaw,
                "T_coin_pTRIG2_ROC2_tdcTimeRaw" : T_coin_pTRIG2_ROC2_tdcTimeRaw,
                "T_coin_pTRIG2_ROC1_tdcTime" : T_coin_pTRIG2_ROC1_tdcTime,
                "T_coin_pTRIG2_ROC2_tdcTime" : T_coin_pTRIG2_ROC2_tdcTime,

                "T_coin_pTRIG3_ROC1_tdcTimeRaw" : T_coin_pTRIG3_ROC1_tdcTimeRaw,
                "T_coin_pTRIG3_ROC2_tdcTimeRaw" : T_coin_pTRIG3_ROC2_tdcTimeRaw,
                "T_coin_pTRIG3_ROC1_tdcTime" : T_coin_pTRIG3_ROC1_tdcTime,
                "T_coin_pTRIG3_ROC2_tdcTime" : T_coin_pTRIG3_ROC2_tdcTime,

                "T_coin_pTRIG4_ROC1_tdcTimeRaw" : T_coin_pTRIG4_ROC1_tdcTimeRaw,
                "T_coin_pTRIG4_ROC2_tdcTimeRaw" : T_coin_pTRIG4_ROC2_tdcTimeRaw,
                "T_coin_pTRIG4_ROC1_tdcTime" : T_coin_pTRIG4_ROC1_tdcTime,
                "T_coin_pTRIG4_ROC2_tdcTime" : T_coin_pTRIG4_ROC2_tdcTime,

                "T_coin_pTRIG5_ROC1_tdcTimeRaw" : T_coin_pTRIG5_ROC1_tdcTimeRaw,
                "T_coin_pTRIG5_ROC2_tdcTimeRaw" : T_coin_pTRIG5_ROC2_tdcTimeRaw,
                "T_coin_pTRIG5_ROC1_tdcTime" : T_coin_pTRIG5_ROC1_tdcTime,
                "T_coin_pTRIG5_ROC2_tdcTime" : T_coin_pTRIG5_ROC2_tdcTime,

                "T_coin_pTRIG6_ROC1_tdcTimeRaw" : T_coin_pTRIG6_ROC1_tdcTimeRaw,
                "T_coin_pTRIG6_ROC2_tdcTimeRaw" : T_coin_pTRIG6_ROC2_tdcTimeRaw,
                "T_coin_pTRIG6_ROC1_tdcTime" : T_coin_pTRIG6_ROC1_tdcTime,
                "T_coin_pTRIG6_ROC2_tdcTime" : T_coin_pTRIG6_ROC2_tdcTime,

                "T_coin_pFADC_TREF_ROC2_adcPed" : T_coin_pFADC_TREF_ROC2_adcPed,
                "T_coin_hFADC_TREF_ROC1_adcPed" : T_coin_hFADC_TREF_ROC1_adcPed,
                "T_coin_pFADC_TREF_ROC2_adcPulseTimeRaw" : T_coin_pFADC_TREF_ROC2_adcPulseTimeRaw,
                "T_coin_hFADC_TREF_ROC1_adcPulseTimeRaw" : T_coin_hFADC_TREF_ROC1_adcPulseTimeRaw,
                "T_coin_pEDTM_tdcTimeRaw" : T_coin_pEDTM_tdcTimeRaw,
                "T_coin_pEDTM_tdcTime" : T_coin_pEDTM_tdcTime,
                "EvtType" : EvtType,
            }

            # Include single arm arrays
            treeDict.update(armDict)

        else:
            print("!!!!ERROR!!!!: Invalid run type %s " % (self.runType)) # Error 4

        cutNames = []        
        cutVals = []
        if self.cuts != None:
            # read in cuts file and make dictionary
            importDict = SetCuts(self.CURRENT_ENV).importDict(self.cuts,self.cut_f,self.runNum,self.DEBUG)
            for i,cut in enumerate(self.cuts):
                x = SetCuts(self.CURRENT_ENV,importDict).booleanDict(cut)
                print("\n%s" % cut)
                print(x, "\n")
                cutNames.append(cut)
                cutVals.append(x)
                if i == 0:
                    inputDict = {}
                cutDict = SetCuts(self.CURRENT_ENV,importDict).readDict(cut,inputDict)
                try:
                    for j,val in enumerate(x):
                        cutDict = SetCuts(self.CURRENT_ENV,importDict).evalDict(cut,eval(x[j]),cutDict)
                        #cutDict = evalDict(cut,eval(x[j]),cutDict)
                except NameError:
                    raise InvalidEntry('''
                    ======================================================================
                      ERROR: %s invalid.
                      Check that run number %s is properly defined in...
                      %s/DB/PARAM
                    ======================================================================
                    ''' % (cut,self.runNum,self.UTILPATH))
            strDict = dict(zip(cutNames,cutVals))

            return [SetCuts(self.CURRENT_ENV,cutDict),treeDict,strDict]
        else:
            return [SetCuts(self.CURRENT_ENV),treeDict,None]
        
    def csv2root(inputDict,rootName):
        '''
        csv2root(inputDict,rootName)
                 |         |
                 |         --> rootName: Output root file name
                 --> inputDict: Input dictionary with csv data to be converted to root

        ----------------------------------------------------------------------------------------------
        Converts csv file to root file. Save arrays,lists,etc. from csv to root file as histograms
        '''
        try:
            tmp = ""
            hist_key = []*len(inputDict)
            hist_val = []*len(inputDict)
            for key,val in inputDict.items():
                tmp = "hist_%s" % key
                tmp = TH1F( tmp, '%s' % key, len(val), 0., max(val))
                hist_key.append(tmp)
                hist_val.append(val)

            f = TFile( rootName, 'recreate' )
            for i, evt in enumerate(hist_val):
                for j, hevt in enumerate(hist_val[i]):
                    print(hist_key[i], "-> ", hevt)
                    hist_key[i].Fill(hevt)
                hist_key[i].Write()
 
            f.Write()
            f.Close()
        except TypeError:
            print("\nERROR 1: Only current accepting 1D array/list values\n")

class Equations():
    '''        
    Equations()

    ----------------------------------------------------------------------------------------------
    
    This class stores a variety of equations often used in the KaonLT analysis procedure
    '''

    def missmass():
        '''
        missmass()

        ----------------------------------------------------------------------------------------------

        Define missing mass calculation. !!! Not currently implimented !!!
        '''
        print("missmass")

class Misc():
    '''
    Misc()

    ----------------------------------------------------------------------------------------------

    Current functions...
            - progressBar

    ----------------------------------------------------------------------------------------------

    Class of miscellaneous methods
    '''
    
    def progressBar(value, endvalue, bar_length=50):
        '''
        progressBar(value, endvalue, bar_length=50)
                    |      |         |
                    |      |         --> bar_length: Length of bar to output to terminal (default = 50)
                    |      --> endvalue: End of loop value - 1
                    --> value: Iteration value
                        
        ----------------------------------------------------------------------------------------------

        A simple progress bar to use in loops
        '''

        percent = float(value) / endvalue
        arrow = '=' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        if percent == 1:
            endl = '\n'
        else:
            endl = ''

        sys.stdout.write(" \r[{0}] {1}%\r{2}".format(arrow + spaces, round(percent * 100), endl))
        sys.stdout.flush()

    @contextmanager
    def suppress_stdout():
        '''
        suppress_stdout()

        ----------------------------------------------------------------------------------------------

        Suppresses python output. Use in a with statement and everything within will be suppressed
        '''
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:  
                yield
            finally:
                sys.stdout = old_stdout

    def test_cpp():
        print('')
