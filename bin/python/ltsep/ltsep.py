#! /usr/bin/python
#
# Description:
# ================================================================
# Time-stamp: "2022-05-31 15:30:46 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from contextlib import contextmanager
import uproot as up
import sys

from .cut import SetCuts 
from .pathing import SetPath

class Root():
    '''    
    Root()

    ----------------------------------------------------------------------------------------------

    # Not required for applying cuts, but required for converting back to root files
    r = klt.Root()

    ----------------------------------------------------------------------------------------------

    This class is for converting files into root files after the analysis steps
    '''

    def __init__(self, ROOTPrefix, runNum, MaxEvent, fout, cuts, CURRENT_ENV):
        '''
        __init__(self,CURRENT_ENV,cutDict=None)
                      |           |
                      |           --> cutDict: Sets the dictionary for the class
                      --> CURRENT_ENV: Input current enviroment path

        ----------------------------------------------------------------------------------------------
        
        Constructor of class takes the current enviroment path and an optional dictionary as input
        '''
        self.ROOTPrefix = ROOTPrefix
        self.runNum = runNum
        self.MaxEvent = MaxEvent
        self.cuts = cuts
        self.CURRENT_ENV = CURRENT_ENV
        # !!! Temporary, make a new class for finding this based off run number
        self.runType = "HeeP"
        # Add this to all files for more dynamic pathing
        self.USER =  SetPath(self.CURRENT_ENV).getPath("USER") # Grab user info for file finding
        self.HOST = SetPath(self.CURRENT_ENV).getPath("HOST")
        self.REPLAYPATH = SetPath(self.CURRENT_ENV).getPath("REPLAYPATH")
        self.UTILPATH = SetPath(self.CURRENT_ENV).getPath("UTILPATH")
        self.ANATYPE = SetPath(self.CURRENT_ENV).getPath("ANATYPE")
        ################################################################################################################################################

        self.fout = self.UTILPATH+fout

        # Add more path setting as needed in a similar manner
        self.OUTPATH = "%s/OUTPUT/Analysis/%s" % (self.UTILPATH, self.runType)      # Output folder location
        self.CUTPATH = "%s/DB/CUTS" % self.UTILPATH

        ################################################################################################################################################
        '''
        Check that root/output paths and files exist for use
        '''

        # Construct the name of the rootfile based upon the info we provided
        self.rootName = "%s/ROOTfiles/Analysis/%s/%s_%s_%s.root" % (self.UTILPATH, self.runType, self.ROOTPrefix, self.runNum, self.MaxEvent)     # Input file location and variables taking
        print ("Attempting to process %s" %(self.rootName))
        SetPath(self.CURRENT_ENV).checkDir(self.OUTPATH)
        SetPath(self.CURRENT_ENV).checkFile(self.rootName)
        print("Output path checks out, outputting to %s" % (self.OUTPATH))


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

    def check_runType(self):
        print(self.CURRENT_ENV)        

    def make_cutDict(self,DEBUG=False):
        '''
        This method calls several methods in kaonlt package. It is required to create properly formated
        dictionaries. The evaluation must be in the analysis script because the analysis variables (i.e. the
        leaves of interest) are not defined in the kaonlt package. This makes the system more flexible
        overall, but a bit more cumbersome in the analysis script. Perhaps one day a better solution will be
        implimented.
        '''

        e_tree = up.open(self.rootName)["T"]

        #################################################################################################################
        # !!!! Need to add if statements for each run type so that unused branches aren't being called and wasting time #
        #################################################################################################################
        # Timing info
        CTime_epCoinTime_ROC1 = e_tree.array("CTime.epCoinTime_ROC1")    #
        #P_RF_tdcTime = e_tree.array("T.coin.pRF_tdcTime")               #
        #P_hod_fpHitsTime = e_tree.array("P.hod.fpHitsTime")             #
        H_RF_Dist = e_tree.array("RFTime.HMS_RFtimeDist")                #
        P_RF_Dist = e_tree.array("RFTime.SHMS_RFtimeDist")               #

        # HMS info
        H_hod_goodscinhit = e_tree.array("H.hod.goodscinhit")            #
        H_hod_goodstarttime = e_tree.array("H.hod.goodstarttime")        #
        H_gtr_beta = e_tree.array("H.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
        H_gtr_xp = e_tree.array("H.gtr.th")                              # xpfp -> Theta
        H_gtr_yp = e_tree.array("H.gtr.ph")                              # ypfp -> Phi
        H_gtr_dp = e_tree.array("H.gtr.dp")                              # dp is Delta
        H_gtr_p = e_tree.array("H.gtr.p")                              # 
        H_cal_etotnorm = e_tree.array("H.cal.etotnorm")                  #
        H_cal_etottracknorm = e_tree.array("H.cal.etottracknorm")        #
        H_cer_npeSum = e_tree.array("H.cer.npeSum")                      #

        # SHMS info
        P_hod_goodscinhit = e_tree.array("P.hod.goodscinhit")            #
        P_hod_goodstarttime = e_tree.array("P.hod.goodstarttime")        #
        P_gtr_beta = e_tree.array("P.gtr.beta")                          # Beta is velocity of particle between pairs of hodoscopes
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
        #emiss = e_tree.array("P.kin.secondary.emiss")                   #
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
            "H_hod_goodscinhit" : H_hod_goodscinhit,
            "H_hod_goodstarttime" : H_hod_goodstarttime,
            "H_gtr_beta" : H_gtr_beta,
            "H_gtr_xp" : H_gtr_xp,
            "H_gtr_yp" : H_gtr_yp,
            "H_gtr_dp" : H_gtr_dp,
            "H_gtr_p" : H_gtr_p,
            "H_cal_etotnorm" : H_cal_etotnorm,
            "H_cal_etottracknorm" : H_cal_etottracknorm,
            "H_cer_npeSum" : H_cer_npeSum,
            "P_hod_goodscinhit" : P_hod_goodscinhit,
            "P_hod_goodstarttime" : P_hod_goodstarttime,
            "P_gtr_beta" : P_gtr_beta,
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
            "MMpi" : MMpi,
            "MMK" : MMK,
            "MMp" : MMp,
            "MandelT" : MandelT,
            "pmiss" : pmiss,
            "pmiss_x" : pmiss_x,
            "pmiss_y" : pmiss_y,
            "pmiss_z" : pmiss_z,
        }

        # read in cuts file and make dictionary
        importDict = SetCuts(self.CURRENT_ENV).importDict(self.cuts,self.fout,self.runNum,DEBUG)
        for i,cut in enumerate(self.cuts):
            x = SetCuts(self.CURRENT_ENV,importDict).booleanDict(cut)
            print("\n%s" % cut)
            print(x, "\n")
            if i == 0:
                inputDict = {}
            cutDict = SetCuts(self.CURRENT_ENV,importDict).readDict(cut,inputDict)
            for j,val in enumerate(x):
                cutDict = SetCuts(self.CURRENT_ENV,importDict).evalDict(cut,eval(x[j]),cutDict)
        return [SetCuts(self.CURRENT_ENV,cutDict),treeDict]

    def setup_ana(self,DEBUG=False):
        self.check_runType()
        make_cutDict = self.make_cutDict(DEBUG)
        bool_cuts = make_cutDict[0]
        treeDict = make_cutDict[1]
        return [bool_cuts,treeDict,self.OUTPATH]

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
