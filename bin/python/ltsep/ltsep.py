#! /usr/bin/python
#
# Description:
# ================================================================
# Time-stamp: "2024-01-08 17:59:58 trottar"
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
    Define pathing only
    \'''

    # Import package for cuts
    from ltsep import Root

    lt=Root(os.path.realpath(__file__))

    # Add this to all files for more dynamic pathing
    VOLATILEPATH=lt.VOLATILEPATH
    ANALYSISPATH=lt.ANALYSISPATH
    HCANAPATH=lt.HCANAPATH
    REPLAYPATH=lt.REPLAYPATH
    UTILPATH=lt.UTILPATH
    PACKAGEPATH=lt.PACKAGEPATH
    OUTPATH=lt.OUTPATH
    ROOTPATH=lt.ROOTPATH
    REPORTPATH=lt.REPORTPATH
    CUTPATH=lt.CUTPATH
    PARAMPATH=lt.PARAMPATH
    SCRIPTPATH=lt.SCRIPTPATH
    SIMCPATH=lt.SIMCPATH
    LTANAPATH=lt.LTANAPATH
    CACHEPATH=lt.CACHEPATH
    ANATYPE=lt.ANATYPE
    USER=lt.USER
    HOST=lt.HOST
    # Note the OUTPATH is not defined unless RunType argument is given, see below

    # If you wish to explicitly define root branches then do the following...
    import uproot as up
    tree = up.open("<ROOT_FILE_NAME>")["<ROOT_TREE_NAME>"]
    # Convert root leaf to array with uproot
    branch_name  = tree.array("<ROOT_BRANCH_NAME>") # The periods are replaced with underscores

    ################################################################################################################################################
    \'''
    Define pathing with OUTPATH 
    \'''

    # Import package for cuts
    from ltsep import Root

    lt=Root(os.path.realpath(__file__), "<Run Type (HeePCoin, HeePSing_<spec>, SimcCoin, SimcSing, Prod, Plot_<Type>, None)>")

    # Add this to all files for more dynamic pathing
    VOLATILEPATH=lt.VOLATILEPATH
    ANALYSISPATH=lt.ANALYSISPATH
    HCANAPATH=lt.HCANAPATH
    REPLAYPATH=lt.REPLAYPATH
    UTILPATH=lt.UTILPATH
    PACKAGEPATH=lt.PACKAGEPATH
    OUTPATH=lt.OUTPATH
    ROOTPATH=lt.ROOTPATH
    REPORTPATH=lt.REPORTPATH
    CUTPATH=lt.CUTPATH
    PARAMPATH=lt.PARAMPATH
    SCRIPTPATH=lt.SCRIPTPATH
    SIMCPATH=lt.SIMCPATH
    LTANAPATH=lt.LTANAPATH
    CACHEPATH=lt.CACHEPATH
    ANATYPE=lt.ANATYPE
    USER=lt.USER
    HOST=lt.HOST
    OUTPATH=lt.OUTPATH

    # If you wish to explicitly define root branches then do the following...
    import uproot as up
    tree = up.open("<ROOT_FILE_NAME>")["<ROOT_TREE_NAME>"]
    # Convert root leaf to array with uproot
    branch_name  = tree.array("<ROOT_BRANCH_NAME>") # The periods are replaced with underscores

    ################################################################################################################################################
    \'''
    Define pathing with OUTPATH and root branches
    \'''

    # Import package for cuts
    from ltsep import Root

    # Note that now a ROOTPrefix, runNum, and MaxEvent is required
    lt=Root(os.path.realpath(__file__), "<Run Type (HeePCoin, HeePSing_<spec>, SimcCoin, SimcSing, Prod, Plot_<Type>, None)>", ROOTPrefix, runNum, MaxEvent)

    # Add this to all files for more dynamic pathing
    VOLATILEPATH=lt.VOLATILEPATH
    ANALYSISPATH=lt.ANALYSISPATH
    HCANAPATH=lt.HCANAPATH
    REPLAYPATH=lt.REPLAYPATH
    UTILPATH=lt.UTILPATH
    PACKAGEPATH=lt.PACKAGEPATH
    OUTPATH=lt.OUTPATH
    ROOTPATH=lt.ROOTPATH
    REPORTPATH=lt.REPORTPATH
    CUTPATH=lt.CUTPATH
    PARAMPATH=lt.PARAMPATH
    SCRIPTPATH=lt.SCRIPTPATH
    SIMCPATH=lt.SIMCPATH
    LTANAPATH=lt.LTANAPATH
    CACHEPATH=lt.CACHEPATH
    ANATYPE=lt.ANATYPE
    USER=lt.USER
    HOST=lt.HOST
    OUTPATH=lt.OUTPATH

    # This will allow access to a dictionary of root branches depending on the RunType given
    # Note in this example the cut object, c, is only useful for advanced usage. See below for general use.
    # Note the dictionary of cuts as strings, strDict, is a None object as there are no cuts defined.
    proc_root = lt.setup_ana()
    c = proc_root[0] # Cut object
    tree = proc_root[1] # Dictionary of branches
    strDict = proc_root[2] # Dictionary of cuts as strings

    # Call root branches with the dictionary key
    tree['<ROOT_BRANCH_NAME>']

    ################################################################################################################################################
    \'''
    Define pathing with OUTPATH, root branches, and set up cuts
    \'''

    # Import package for cuts
    from ltsep import Root

    # ---> If multple run type files are required then define a new run type file altogether. Do not try to 
    # chain run type files. It can be done, but is computationally wasteful and pointless.
    cut_f = "<path_to_run_type_cut>"

    cuts = ["<runTypeCut1>","<runTypeCut2>",<etc>,...]

    lt=Root(os.path.realpath(__file__), "<Run Type (HeePCoin, HeePSing_<spec>, SimcCoin, SimcSing, Prod, Plot_<Type>, None)>", ROOTPrefix, runNum, MaxEvent, cut_f, cuts)

    # Add this to all files for more dynamic pathing
    VOLATILEPATH=lt.VOLATILEPATH
    ANALYSISPATH=lt.ANALYSISPATH
    HCANAPATH=lt.HCANAPATH
    REPLAYPATH=lt.REPLAYPATH
    UTILPATH=lt.UTILPATH
    PACKAGEPATH=lt.PACKAGEPATH
    OUTPATH=lt.OUTPATH
    ROOTPATH=lt.ROOTPATH
    REPORTPATH=lt.REPORTPATH
    CUTPATH=lt.CUTPATH
    PARAMPATH=lt.PARAMPATH
    SCRIPTPATH=lt.SCRIPTPATH
    SIMCPATH=lt.SIMCPATH
    LTANAPATH=lt.LTANAPATH
    CACHEPATH=lt.CACHEPATH
    ANATYPE=lt.ANATYPE
    USER=lt.USER
    HOST=lt.HOST
    OUTPATH=lt.OUTPATH

    # Arrays are defined in ltsep, no need to redefine.
    # cut_f, cuts are optional flags. If you don't have cuts just leave these blank and the runtype root branches will be accessible, see above.
    # ROOTPrefix is also an optional flag, see above. This means your branches will need to be defined explicitly, see below.
    proc_root = lt.setup_ana()
    c = proc_root[0] # Cut object
    tree = proc_root[1] # Dictionary of branches
    strDict = proc_root[2] # Dictionary of cuts as 

    # Call root branches with the dictionary key
    tree['<ROOT_BRANCH_NAME>']

    # To apply cuts to root branches...
    # c is the cut object used to grab instance of add_cut
    # add_cut() applies the cut, i.e. "<runTypeCut#>", to the branch defined, i.e. tree['<ROOT_BRANCH_NAME>']
    c.add_cut(tree['<ROOT_BRANCH_NAME>'], "<runTypeCut#>")

    ################################################################################################################################################

    # ----> For more info
    from ltsep import Help

    # Some help examples
    Help.info(Root)
    Help.info(SetCuts.importDict)
    Help.path_setup()
    Help.cut_setup()
    Help.searchPathFile(os.path.realpath(__file__))

    ----------------------------------------------------------------------------------------------

    This is the most extensive class of the ltsep package. This class will grab many of the required 
    tasks for doing in depth analysis in python such as define pathing variables and cuts.
    '''

    def __init__(self, CURRENT_ENV, runType="None", ROOTPrefix="", runNum="-1", MaxEvent="-1", cut_f="", cuts=None, DEBUG=False):
        '''
        __init__(self, CURRENT_ENV, ROOTPrefix, runType, runNum, MaxEvent, cut_f, cuts=None, DEBUG=False)
                       |            |           |        |       |         |      |          |
                       |            |           |        |       |         |      |          --> DEBUG: Set true to show debug output
                       |            |           |        |       |         |      --> cuts: Specific cuts in run type cuts file to call
                       |            |           |        |       |         --> cut_f: File of defined run type cuts
                       |            |           |        |       --> MaxEvent: Max number of events replayed
                       |            |           |        --> runNum: Run number
                       |            |           --> runType: Type of run (HeePCoin, HeePSing_<spec>, SimcCoin, SimcSing, Prod, Plot_<Type>, None, etc.)
                       |            --> ROOTPrefix: ROOT prefix as defined by either the Replay script or other analysis scripts
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
        self.LTANAPATH=SetPath(self.CURRENT_ENV).getPath("LTANAPATH")
        self.CACHEPATH=SetPath(self.CURRENT_ENV).getPath("CACHEPATH")
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
            self.OUTPATH = "%s/OUTPUT/Analysis/HeeP" % self.LTANAPATH      # Output folder location
        elif "Prod" in self.runType:
            self.OUTPATH = "%s/OUTPUT/Analysis/%sLT" % (self.UTILPATH,self.ANATYPE)      # Output folder location
        elif "HGCer" in self.runType:
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
                elif "HGCer" in self.runType:
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
                elif "HGCer" in self.runType:
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
        methods to define cuts as well as grabs the dictionary of root branches.
        '''

        # Make cut dictionary and convert to boolean list for cut application
        make_cutDict = self.make_cutDict()
        bool_cuts = make_cutDict[0]

        # Get dictionary of branch names
        treeDict = make_cutDict[1]

        # Get dictionary of cut names and values as strings
        strDict = make_cutDict[2]

        return [bool_cuts,treeDict,strDict]

    def check_runType(self):
        '''
        Creates a list of the root branches for a specific run type.
        '''
        
        def_f = "%s/DB/BRANCH_DEF/%sLT/%s" % (self.UTILPATH,self.ANATYPE,self.runType)

        with open(def_f, 'r') as f:
            def_data = f.read().splitlines()
        return def_data

    def make_cutDict(self):
        '''
        This method calls several methods in ltsep package. It is required to create properly formated
        dictionaries. This will define the root branches based off the run type then define the cut object
        which contains the dictionary of cut boolean lists. 
        '''

        # Dictionary of all used branches
        # Add more if required (note: make sure to add to DB/BRANCH_DEF/<ANATYPE>LT/<RUNTYPE_FILE>)
        branch_mapping = {
            # HMS info
            "H_dc_InsideDipoleExit" : "H.dc.InsideDipoleExit",
            "H_hod_goodscinhit" : "H.hod.goodscinhit",
            "H_hod_goodstarttime" : "H.hod.goodstarttime",
            # Beta is velocity of particle between pairs of hodoscopes
            "H_gtr_beta" : "H.gtr.beta",
            "H_dc_x_fp" : "H.dc.x_fp",
            "H_dc_y_fp" : "H.dc.y_fp",
            "H_dc_xp_fp" : "H.dc.xp_fp",
            "H_dc_yp_fp" : "H.dc.yp_fp",
            # xpfp -> Theta
            "H_gtr_xp" : "H.gtr.th",
            # ypfp -> Phi
            "H_gtr_yp" : "H.gtr.ph",
            # dp is Delta
            "H_gtr_dp" : "H.gtr.dp",
            "H_gtr_p" : "H.gtr.p",
            "H_cal_etotnorm" : "H.cal.etotnorm",
            "H_cal_etottracknorm" : "H.cal.etottracknorm",
            "H_cer_npeSum" : "H.cer.npeSum",
            "H_W" : "H.kin.primary.W",
            "H_cal_etotnorm" : "H.cal.etotnorm",
            "H_cer_npeSum" : "H.cer.npeSum",
            "H_gtr_dp" : "H.gtr.dp",
            "H_tr_tg_th" : "H.gtr.th",
            "H_tr_tg_ph" : "H.gtr.ph",
            "H_gtr_beta" : "H.gtr.beta",
            "H_tr_chi2" : "H.tr.chi2",
            "H_tr_ndof" : "H.tr.ndof",
            "H_hod_goodscinhit" : "H.hod.goodscinhit",
            "H_hod_betanotrack" : "H.hod.betanotrack",
            "H_hod_goodstarttime" : "H.hod.goodstarttime",
            "H_dc_ntrack" : "H.dc.ntrack",
            "H_dc_1x1_nhit" : "H.dc.1x1.nhit",
            "H_dc_1u2_nhit" : "H.dc.1u2.nhit",
            "H_dc_1u1_nhit" : "H.dc.1u1.nhit",
            "H_dc_1v1_nhit" : "H.dc.1v1.nhit",
            "H_dc_1x2_nhit" : "H.dc.1x2.nhit",
            "H_dc_1v2_nhit" : "H.dc.1v2.nhit",
            "H_dc_2x1_nhit" : "H.dc.2x1.nhit",
            "H_dc_2u2_nhit" : "H.dc.2u2.nhit",
            "H_dc_2u1_nhit" : "H.dc.2u1.nhit",
            "H_dc_2v1_nhit" : "H.dc.2v1.nhit",
            "H_dc_2x2_nhit" : "H.dc.2x2.nhit",
            "H_dc_2v2_nhit" : "H.dc.2v2.nhit",

            # SHMS info
            "P_cal_fly_earray" : "P.cal.fly.earray",
            "P_cal_pr_eplane" : "P.cal.pr.eplane",
            "P_cal_etotnorm" : "P.cal.etotnorm",
            "P_aero_npeSum" : "P.aero.npeSum",
            "P_hgcer_npeSum" : "P.hgcer.npeSum",
            "P_hgcer_xAtCer" : "P.hgcer.xAtCer",
            "P_hgcer_yAtCer" : "P.hgcer.yAtCer",
            "P_aero_xAtCer" : "P.aero.xAtAero",
            "P_aero_yAtCer" : "P.aero.yAtAero",
            "P_dc_InsideDipoleExit" : "P.dc.InsideDipoleExit",
            "P_hod_goodscinhit" :     "P.hod.goodscinhit",
            "P_hod_goodstarttime" : "P.hod.goodstarttime",
            # Beta is velocity of particle between pairs of hodoscopes
            "P_gtr_beta" : "P.gtr.beta",
            "P_gtr_x" : "P.gtr.x",
            "P_gtr_y" : "P.gtr.y",
            "P_dc_x_fp" : "P.dc.x_fp",
            "P_dc_y_fp" : "P.dc.y_fp",
            "P_dc_xp_fp" : "P.dc.xp_fp",
            "P_dc_yp_fp" : "P.dc.yp_fp",
            # xpfp -> Theta
            "P_gtr_xp" : "P.gtr.th",
            # ypfp -> Phi
            "P_gtr_yp" : "P.gtr.ph",
            "P_gtr_p" : "P.gtr.p",
            # dp is Delta
            "P_gtr_dp" : "P.gtr.dp",
            "P_cal_etotnorm" : "P.cal.etotnorm",
            "P_cal_etottracknorm" : "P.cal.etottracknorm",
            "P_aero_npeSum" : "P.aero.npeSum",
            "P_aero_xAtAero" : "P.aero.xAtAero",
            "P_aero_yAtAero" : "P.aero.yAtAero",
            "P_hgcer_npeSum" : "P.hgcer.npeSum",
            "P_hgcer_xAtCer" : "P.hgcer.xAtCer",
            "P_hgcer_yAtCer" : "P.hgcer.yAtCer",
            "P_cal_etotnorm" : "P.cal.etotnorm",
            "P_hgcer_npeSum" : "P.hgcer.npeSum",
            "P_aero_npeSum" : "P.aero.npeSum",
            "P_gtr_dp" : "P.gtr.dp",
            "P_gtr_th" : "P.gtr.th",
            "P_gtr_ph" : "P.gtr.ph",
            "P_gtr_beta" : "P.gtr.beta",
            "P_tr_chi2" : "P.tr.chi2",
            "P_tr_ndof" : "P.tr.ndof",
            "P_hod_goodscinhit" : "P.hod.goodscinhit",
            "P_hod_betanotrack" : "P.hod.betanotrack",
            "P_hod_goodstarttime" : "P.hod.goodstarttime",
            "P_dc_ntrack" : "P.dc.ntrack",
            "P_dc_1x1_nhit" : "P.dc.1x1.nhit",
            "P_dc_1u2_nhit" : "P.dc.1u2.nhit",
            "P_dc_1u1_nhit" : "P.dc.1u1.nhit",
            "P_dc_1v1_nhit" : "P.dc.1v1.nhit",
            "P_dc_1x2_nhit" : "P.dc.1x2.nhit",
            "P_dc_1v2_nhit" : "P.dc.1v2.nhit",
            "P_dc_2x1_nhit" : "P.dc.2x1.nhit",
            "P_dc_2u2_nhit" : "P.dc.2u2.nhit",
            "P_dc_2u1_nhit" : "P.dc.2u1.nhit",
            "P_dc_2v1_nhit" : "P.dc.2v1.nhit",
            "P_dc_2x2_nhit" : "P.dc.2x2.nhit",
            "P_dc_2v2_nhit" : "P.dc.2v2.nhit",

            # Raster
            "raster_x" : "P.rb.x",
            "raster_y" : "P.rb.y",
            "raster_z" : "P.rb.z",

            # BPM target
            "bpm_tar_x" : "P.rb.raster.fr_xbpm_tar",
            "bpm_tar_y" : "P.rb.raster.fr_ybpm_tar",

            # Kinematic quantitites
            "Q2" : "H.kin.primary.Q2",
            "W" : "H.kin.primary.W",
            "epsilon" : "H.kin.primary.epsilon",
            "ph_q" : "P.kin.secondary.ph_xq",
            "ph_recoil" : "P.kin.secondary.ph_bq",
            "th_q" : "P.kin.secondary.th_xq",
            "th_recoil" : "P.kin.secondary.th_bq",
            "emiss" : "P.kin.secondary.emiss",
            "MMpi" : "P.kin.secondary.MMpi",
            "MMK" : "P.kin.secondary.MMK",
            "MMp" : "P.kin.secondary.MMp",
            "MandelT" : "P.kin.secondary.MandelT",
            "MandelU" : "P.kin.secondary.MandelU",
            "pmiss" : "P.kin.secondary.pmiss",
            "pmiss_x" : "P.kin.secondary.pmiss_x",
            "pmiss_y" : "P.kin.secondary.pmiss_y",
            "pmiss_z" : "P.kin.secondary.pmiss_z",
            "Erecoil" : "P.kin.secondary.Erecoil",
            "emiss_nuc" : "P.kin.secondary.emiss_nuc",
            "Mrecoil" : "P.kin.secondary.Mrecoil",

            # Current
            "H_bcm_bcm1_AvgCurrent" : "H.bcm.bcm1.AvgCurrent",
            "H_bcm_bcm2_AvgCurrent" : "H.bcm.bcm2.AvgCurrent",
            "H_bcm_bcm4a_AvgCurrent" : "H.bcm.bcm4a.AvgCurrent",
            "H_bcm_bcm4b_AvgCurrent" : "H.bcm.bcm4b.AvgCurrent",
            "H_bcm_bcm4c_AvgCurrent" : "H.bcm.bcm4c.AvgCurrent",

            # Timing info
            "CTime_eKCoinTime_ROC1" : "CTime.eKCoinTime_ROC1",
            "CTime_ePiCoinTime_ROC1" : "CTime.ePiCoinTime_ROC1",
            "CTime_epCoinTime_ROC1" : "CTime.epCoinTime_ROC1",

            "P_RF_tdcTime" : "T.coin.pRF_tdcTime",
            "P_hod_fpHitsTime" : "P.hod.fpHitsTime",
            "H_RF_Dist" : "RFTime.HMS_RFtimeDist",
            "P_RF_Dist" : "RFTime.SHMS_RFtimeDist",


            "T_coin_pTRIG1_ROC1_tdcTimeRaw" : "T.coin.pTRIG1_ROC1_tdcTimeRaw",
            "T_coin_pTRIG1_ROC2_tdcTimeRaw" : "T.coin.pTRIG1_ROC2_tdcTimeRaw",
            "T_coin_pTRIG1_ROC1_tdcTime" : "T.coin.pTRIG1_ROC1_tdcTime",
            "T_coin_pTRIG1_ROC2_tdcTime" : "T.coin.pTRIG1_ROC2_tdcTime",

            "T_coin_pTRIG2_ROC1_tdcTimeRaw" : "T.coin.pTRIG2_ROC1_tdcTimeRaw",
            "T_coin_pTRIG2_ROC2_tdcTimeRaw" : "T.coin.pTRIG2_ROC2_tdcTimeRaw",
            "T_coin_pTRIG2_ROC1_tdcTime" : "T.coin.pTRIG2_ROC1_tdcTime",
            "T_coin_pTRIG2_ROC2_tdcTime" : "T.coin.pTRIG2_ROC2_tdcTime",

            "T_coin_pTRIG3_ROC1_tdcTimeRaw" : "T.coin.pTRIG3_ROC1_tdcTimeRaw",
            "T_coin_pTRIG3_ROC2_tdcTimeRaw" : "T.coin.pTRIG3_ROC2_tdcTimeRaw",
            "T_coin_pTRIG3_ROC1_tdcTime" : "T.coin.pTRIG3_ROC1_tdcTime",
            "T_coin_pTRIG3_ROC2_tdcTime" : "T.coin.pTRIG3_ROC2_tdcTime",

            "T_coin_pTRIG4_ROC1_tdcTimeRaw" : "T.coin.pTRIG4_ROC1_tdcTimeRaw",
            "T_coin_pTRIG4_ROC2_tdcTimeRaw" : "T.coin.pTRIG4_ROC2_tdcTimeRaw",
            "T_coin_pTRIG4_ROC1_tdcTime" : "T.coin.pTRIG4_ROC1_tdcTime",
            "T_coin_pTRIG4_ROC2_tdcTime" : "T.coin.pTRIG4_ROC2_tdcTime",

            "T_coin_pTRIG5_ROC1_tdcTimeRaw" : "T.coin.pTRIG5_ROC1_tdcTimeRaw",
            "T_coin_pTRIG5_ROC2_tdcTimeRaw" : "T.coin.pTRIG5_ROC2_tdcTimeRaw",
            "T_coin_pTRIG5_ROC1_tdcTime" : "T.coin.pTRIG5_ROC1_tdcTime",
            "T_coin_pTRIG5_ROC2_tdcTime" : "T.coin.pTRIG5_ROC2_tdcTime",

            "T_coin_pTRIG6_ROC1_tdcTimeRaw" : "T.coin.pTRIG6_ROC1_tdcTimeRaw",
            "T_coin_pTRIG6_ROC2_tdcTimeRaw" : "T.coin.pTRIG6_ROC2_tdcTimeRaw",
            "T_coin_pTRIG6_ROC1_tdcTime" : "T.coin.pTRIG6_ROC1_tdcTime",
            "T_coin_pTRIG6_ROC2_tdcTime" : "T.coin.pTRIG6_ROC2_tdcTime",

            "T_coin_pFADC_TREF_ROC2_adcPed" : "T.coin.pFADC_TREF_ROC2_adcPed",
            "T_coin_hFADC_TREF_ROC1_adcPed" : "T.coin.hFADC_TREF_ROC1_adcPed",
            "T_coin_pFADC_TREF_ROC2_adcPulseTimeRaw" : "T.coin.pFADC_TREF_ROC2_adcPulseTimeRaw",
            "T_coin_hFADC_TREF_ROC1_adcPulseTimeRaw" : "T.coin.hFADC_TREF_ROC1_adcPulseTimeRaw",
            "T_coin_pEDTM_tdcTimeRaw" : "T.coin.pEDTM_tdcTimeRaw",
            "T_coin_pEDTM_tdcTime" : "T.coin.pEDTM_tdcTime",

            # Misc quantities
            "RFFreq" : "MOFC1FREQ",
            "RFFreqDiff" : "MOFC1DELTA",
            "EvtType" : "fEvtHdr.fEvtType",
        }

        # Initiate dictionary of root branches
        treeDict = {}
        
        print("Grabbing branches from {}...".format(self.rootName))
        with up.open(self.rootName) as root_file:
        
            # Grab tree from root file
            e_tree = root_file["T"]
            
            # 1) Loops over the root branches of a specific run type (defined in UTILPATH/DB/BRANCH_DEF/<RunTypeFile>)
            # 2) Grabs the branch from the root tree (defined above) and defines as array
            # 3) Adds branch to dictionary
            for branch in self.check_runType():
                if branch in branch_mapping:
                    treeDict[branch] = e_tree.array(branch_mapping[branch])

        #################################################################################################################
            
        # For better explaination of the methods below use the Help class defined above
        cutNames = []        
        cutVals = []
        if self.cuts != None:
            # read in cuts file and makes dictionary
            importDict = SetCuts(self.CURRENT_ENV).importDict(self.cuts,self.cut_f,self.runNum,self.DEBUG)
            for i,cut in enumerate(self.cuts):
                # Converts the dictionary to a list of strings that need to be evaluated and converted
                # into a boolean list
                x = SetCuts(self.CURRENT_ENV,importDict).booleanDict(cut)
                print("\n%s" % cut)
                print(x, "\n")
                # Saves string names of cuts and their values
                cutNames.append(cut)
                cutVals.append(x)
                if i == 0:
                    inputDict = {}
                # Redefines the dictionary to be reimplemented below
                cutDict = SetCuts(self.CURRENT_ENV,importDict).readDict(cut,inputDict)
                for j,val in enumerate(x):
                    try:
                        # Evaluates the list of strings which converts them to a list of boolean values
                        # corresponding to the cuts applied
                        cutDict = SetCuts(self.CURRENT_ENV,importDict).evalDict(cut,eval(x[j]),cutDict)
                        # This is the cython defined version, slightly faster but 
                        # requires it to be compiled fist
                        #cutDict = evalDict(cut,eval(x[j]),cutDict)
                    except NameError:
                        if "pid" in x[j]:
                            err_dir = self.UTILPATH+"/DB/PARAM/PID_Parameters.csv"
                        if "track" in x[j]:
                            err_dir = self.UTILPATH+"/DB/PARAM/Tracking_Parameters.csv"
                        if "accept" in x[j]:
                            err_dir = self.UTILPATH+"/DB/PARAM/Acceptance_Parameters.csv"
                        if "coin_time" in x[j]:
                            err_dir = self.UTILPATH+"/DB/PARAM/Timing_Parameters.csv"
                        if "current" in x[j]:
                            err_dir = self.UTILPATH+"/DB/PARAM/Current_Parameters.csv"
                        if "misc" in x[j]:
                            err_dir = self.UTILPATH+"/DB/PARAM/Misc_Parameters.csv"
                        raise InvalidEntry('''
                        ======================================================================
                          ERROR: %s invalid.

                          Improperly defined cut at... 
                          %s
                        ----------------------------------------------------------------------
                          Check that run number %s is properly defined in...
                          %s
                        ======================================================================
                        ''' % (cut,x[j],self.runNum,err_dir))
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
