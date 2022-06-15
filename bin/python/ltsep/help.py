#! /usr/bin/python

#
# Description: Just calls help functions for various methods to help users
# ================================================================
# Time-stamp: "2022-06-15 13:21:17 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import os,glob

from .ltsep import Root, Equations, Misc
from .cut import SetCuts
from .pathing import SetPath

class Help():
    '''
    Help()

    ----------------------------------------------------------------------------------------------

    Class that is used to help users setup their scripts and get information on various functions 
    used throughout the ltsep package
    '''
        
    def info(func):
        '''
        info(func)
             |
             --> func: Input class/function to call help()

        ----------------------------------------------------------------------------------------------

        Calls help() to get description of function
        '''
        help(func)
    
    def getDoc(func):
        '''
        getDoc(func)

        ----------------------------------------------------------------------------------------------

        Decorator that allows docstring to be used inside the function being called
        '''
        def wrapper(*args, **kwargs):
            return func(func, *args, **kwargs)
        return wrapper

    @getDoc
    def path_setup(path_setup):
        '''
        ----------------------------------------------------------------------------------------------
        For the pathing you do not need to define all of the keys in the dictionary (like below),
        rather choose which paths are being used in your specific string. Make sure all references
        to UTIL_PION or UTIL_KAONLT are defined using UTILPATH (or any other useful path listed below)
        ----------------------------------------------------------------------------------------------

        ################################################################################################################################################
        \'''
        ltsep package import and pathing definitions
        \'''

        import os
        import ltsep as lt

        # To define just pathing variables...
        proc_root = lt.Root(os.path.realpath(__file__)).setup_ana()
        p = proc_root[2] # Dictionary of pathing variables

        # os.path.realpath(__file__) is your current directory path
        # This will grab the pathing for these variables based off the files in PATH_TO_DIR
        VOLATILEPATH=p["VOLATILEPATH"]
        ANALYSISPATH=p["ANALYSISPATH"]
        HCANAPATH=p["HCANAPATH"]
        REPLAYPATH=p["REPLAYPATH"]
        UTILPATH=p["UTILPATH"]
        PACKAGEPATH=p["PACKAGEPATH"]
        OUTPATH=p["OUTPATH"]
        ROOTPATH=p["ROOTPATH"]
        REPORTPATH=p["REPORTPATH"]
        CUTPATH=p["CUTPATH"]
        PARAMPATH=p["PARAMPATH"]
        SCRIPTPATH=p["SCRIPTPATH"]
        ANATYPE=p["ANATYPE"]
        USER=p["USER"]
        HOST=p["HOST"]

        ################################################################################################################################################

        print("Running as %s on %s, hallc_replay_lt path assumed as %s" % (USER, HOST, REPLAYPATH))

        ################################################################################################################################################
        \'''
        Check that root/output paths and files exist for use, this is depreciated and done backend in ltsep now
        \'''

        # Construct the name of the rootfile based upon the info we provided
        OUTPATH = UTILPATH+"/OUTPUT/Analysis/%sLT" % ANATYPE        # Output folder location
        rootName = UTILPATH+"/ROOTfiles/Analysis/Lumi/%s_%s_%s.root" % (ROOTPrefix,runNum,MaxEvent)     # Input file location and variables taking
        print ("Attempting to process %s" %(rootName))
        lt.SetPath(os.path.realpath(__file__)).checkDir(OUTPATH)
        lt.SetPath(os.path.realpath(__file__)).checkFile(rootName)
        print("Output path checks out, outputting to %s" % (OUTPATH))
        '''
        print(path_setup.__doc__)

    @getDoc
    def cut_setup(cut_setup):
        '''
        ----------------------------------------------------------------------------------------------
        Make sure you have the following in your script...
        ----------------------------------------------------------------------------------------------
        ################################################################################################################################################
        \'''
        Define and set up cuts
        \'''

        import ltsep as lt

        # ---> If multple run type files are required then define a new run type file altogether. Do not try to 
        # chain run type files. It can be done, but is computationally wasteful and pointless.
        f_cut = "<path_to_run_type_cut>"

        cuts = ["runTypeCut1","runTypeCut2",<etc>,...]

        # To apply cuts to array and define pathing variables...
        # Arrays are defined in ltsep, no need to redefine.
        proc_root = lt.Root(os.path.realpath(__file__),ROOTPrefix, "<Run Type (HeePCoin, HeePSing_<spec>, SimcCoin, SimcSing, KaonLT/PionLT, Plot_<Type>, None)>", runNum, MaxEvent, f_cut, cuts).setup_ana()
        c = proc_root[0] # Cut object
        b = proc_root[1] # Dictionary of branches
        p = proc_root[2] # Dictionary of pathing variables
        OUTPATH = proc_root[3] # Get pathing for OUTPATH

        # ----> See lt.Help.path_setup() for more info

        ################################################################################################################################################
        \'''
        If you wish to explicitly define arrays then do the following...
        \'''

        # To define pathing variables as well as check for existing root files (do this if plotting, this will NOT apply cuts)...
        proc_root = lt.Root(os.path.realpath(__file__),ROOTPrefix, "<Run Type (Plot_<Type>, None)>", runNum, MaxEvent).setup_ana()
        p = proc_root[2] # Dictionary of pathing variables
        OUTPATH = proc_root[3] # Get pathing for OUTPATH
        # To define just pathing variables...
        proc_root = lt.Root(os.path.realpath(__file__)).setup_ana()
        p = proc_root[2] # Dictionary of pathing variables

        import uproot as up
        # Convert root leaf to array with uproot
        # Array name must match what is defined in DB/CUTS/general/
        leaf_name  = tree.array("leaf.name") # The periods are replaced with underscores
        '''
        print(cut_setup.__doc__)

    def searchPathFile(CURRENT_ENV):
        '''
        searchPathFile(CURRENT_ENV)
                       |
                       --> CURRENT_ENV: Input current enviroment path

        ----------------------------------------------------------------------------------------------
        Outputs the current enviroment file and its contents which establish script pathing
        '''

        CURRENT_ENV = CURRENT_ENV.replace(os.getlogin(),"${USER}") # Replace username with general ${USER} so it can be used broadly
        CURRENT_ENV = CURRENT_ENV.split("/UTIL_",1)[0] # Redefine path to hallc_replay_lt (if in replay env)
        CURRENT_ENV = CURRENT_ENV.split("/cut.py",1)[0] # Redefine path to ltsep (if in package env)

        # Grab location of package (either in .local or in the UTIL dir)
        PACKAGE_ENV = os.path.dirname(os.path.realpath(__file__))

        # Grab username and hostname
        USER = os.getlogin()
        HOST = os.uname()[1]

        # Setup path to pathing files (see PATH_TO_DIR)
        path_check = "{}/PATH_TO_DIR".format(PACKAGE_ENV)
        
        # Check through all pathing files for the one that matches the current working enviroment
        for fname in glob.glob(path_check+"/*.path"):
            with open(fname) as f:
                search = f.read()
            if USER == "cdaq":
                if PACKAGE_ENV in search:
                    PATHFILE = fname
            else:
                if CURRENT_ENV in search:
                    PATHFILE = fname

        print("\t----------------------------------------------------------------------------------------------")
        print("\tThe current enviroment path file used is...\n\t{}".format(PATHFILE))
        print("\t----------------------------------------------------------------------------------------------\n")
        with open(PATHFILE) as f:
            for line in f:
                print("\t",line)
        print("\n\n")
