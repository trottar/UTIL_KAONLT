#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2021-08-31 03:30:21 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
##################################################################################
# Created - 10/July/2021, Author - Muhammad Junaid, University of Regina, Canada
##################################################################################
# This version of script is for shift workers at JLAB
# Executes the replay script and python analysis script and at the end python plotting script
# To run this script, execute ./scriptname $RUNNUMBER$

#################################################################################################################################################

echo "Starting analysis of Proton events"
echo "I take as arguments the run number and number of events!"
# Input params - run number and max number of events
RUNNUMBER=$1
if [[ -z "$1" ]]; then
    echo "I need a run number"
    echo "Please provide a run number as input"
fi
MAXEVENTS=$2
if [[ -z "$2" ]]; then
    echo "Only Run Number entered...I'll assume -1 (all) events!" 
    MAXEVENTS=-1 
fi

#################################################################################################################################################

# Set path depending upon hostname. Change or add more as needed  
if [[ "${HOSTNAME}" = *"farm"* ]]; then  
    REPLAYPATH="/group/c-kaonlt/USERS/${USER}/hallc_replay_lt"
    if [[ "${HOSTNAME}" != *"ifarm"* ]]; then
	source /site/12gev_phys/softenv.sh 2.3
	source /apps/root/6.18.04/setroot_CUE.bash
    fi
    cd "/group/c-kaonlt/hcana/"
    source "/group/c-kaonlt/hcana/setup.sh"
    cd "$REPLAYPATH"
    source "$REPLAYPATH/setup.sh"
elif [[ "${HOSTNAME}" = *"qcd"* ]]; then
    REPLAYPATH="/group/c-kaonlt/USERS/${USER}/hallc_replay_lt"
    cd "$REPLAYPATH"
    source "$REPLAYPATH/setup.sh" 
elif [[ "${HOSTNAME}" = *"cdaq"* ]]; then
    REPLAYPATH="/home/cdaq/hallc-online/hallc_replay_lt"
elif [[ "${HOSTNAME}" = *"phys.uregina.ca"* ]]; then
    REPLAYPATH="/home/${USER}/work/JLab/hallc_replay_lt"
fi

UTILPATH="${REPLAYPATH}/UTIL_KAONLT"
cd $REPLAYPATH

###################################################################################################################################################

# Section for HeeP replay script
if [ ! -f "$REPLAYPATH/UTIL_KAONLT/ROOTfiles/Scalers/coin_replay_scalers_${RUNNUMBER}_150000.root" ]; then
    eval "$REPLAYPATH/hcana -l -q \"SCRIPTS/COIN/SCALERS/replay_coin_scalers.C($RUNNUMBER,150000)\""
    cd "$REPLAYPATH/CALIBRATION/bcm_current_map"
    root -b -l<<EOF 
.L ScalerCalib.C+
.x run.C("${REPLAYPATH}/UTIL_KAONLT/ROOTfiles/Scalers/coin_replay_scalers_${RUNNUMBER}_150000.root")
.q  
EOF
    mv bcmcurrent_$RUNNUMBER.param $REPLAYPATH/PARAM/HMS/BCM/CALIB/bcmcurrent_$RUNNUMBER.param
    cd $REPLAYPATH
else echo "Scaler replayfile already found for this run in $REPLAYPATH/ROOTfiles/Scalers - Skipping scaler replay step"
fi

sleep 3
# SJDK 31/08/21 - Replays for HeeP analysis should output to Analysis/HeeP, for now this is probably fine
if [ ! -f "$REPLAYPATH/UTIL_KAONLT/ROOTfiles/Analysis/HeeP/Pion_coin_replay_production_${RUNNUMBER}_${MAXEVENTS}.root" ]; then
    if [[ "${HOSTNAME}" != *"ifarm"* ]]; then
	if [[ "${HOSTNAME}" == *"cdaq"* ]]; then
	    eval "$REPLAYPATH/hcana -l -q \"UTIL_KAONLT/scripts/replay/replay_coin_heep.C($RUNNUMBER,$MAXEVENTS)\""| tee $REPLAYPATH/UTIL_KAONLT/REPORT_OUTPUT/Analysis/HeeP/Pion_output_coin_production_Summary_${RUNNUMBER}_${MAXEVENTS}.report
	else	
	    eval "$REPLAYPATH/hcana -l -q \"UTIL_KAONLT/scripts/replay/replay_coin_heep.C($RUNNUMBER,$MAXEVENTS)\"" 
	fi
    elif [[ "${HOSTNAME}" == *"ifarm"* ]]; then
	eval "$REPLAYPATH/hcana -l -q \"UTIL_KAONLT/scripts/replay/replay_coin_heep.C($RUNNUMBER,$MAXEVENTS)\""| tee $REPLAYPATH/UTIL_KAONLT/REPORT_OUTPUT/Analysis/HeeP/Pion_output_coin_production_Summary_${RUNNUMBER}_${MAXEVENTS}.report
    fi
else echo "Replayfile already found for this run in $REPLAYPATH/UTIL_KAONLT/ROOTfiles/Analysis/HeeP/ - Skipping replay step"
fi

sleep 3

################################################################################################################################                                                                                   
# Section for HeeP analysis script
if [ -f "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_Analysed_Data.root" ]; then
    read -p "Pion production analysed file already exists, do you want to reprocess it? <Y/N> " option1
    if [[ $option1 == "y" || $option1 == "Y" || $option1 == "yes" || $option1 == "Yes" ]]; then
	rm "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_Analysed_Data.root"
	echo "Reprocessing"
	python3 ${UTILPATH}/scripts/heep/src/coinyield.py Pion_coin_replay_production ${RUNNUMBER} ${MAXEVENTS}
    else
	echo "Skipping python analysis script step"
    fi
elif [ ! -f "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_Analysed_Data.root" ]; then
	python3 ${UTILPATH}/scripts/heep/src/coinyield.py Pion_coin_replay_production ${RUNNUMBER} ${MAXEVENTS}
else echo "Analysed root file already found in ${UTILPATH}/OUTPUT/Analysis/HeeP/ - Skipped python analyzer script step"
fi

sleep 3

##################################################################################################################################

# Section for HeeP physics ploting script
if [ -f "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_Output_Data.root" ]; then
    read -p "HeeP output plots file already exists, do you want to reprocess it? <Y/N> " option2
    if [[ $option2 == "y" || $option2 == "Y" || $option2 == "yes" || $option2 == "Yes" ]]; then
	rm "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_Output_Data.root"
	echo "Reprocessing"
	python3 ${UTILPATH}/scripts/heep/src/plot_coin.py ${RUNNUMBER} ${MAXEVENTS} Analysed_Data
    else
	echo "Skipping python HeeP plotting script step"
    fi
elif [ ! -f  "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_Output_Data.root" ]; then
	python3 ${UTILPATH}/scripts/heep/src/plot_coin.py ${RUNNUMBER} ${MAXEVENTS} Analysed_Data
else echo "Pion physics output root file already found in ${UTILPATH}/OUTPUT/Analysis/HeeP/ - Skipped python plotting script step"
fi
evince "${UTILPATH}/OUTPUT/Analysis/HeeP/${RUNNUMBER}_${MAXEVENTS}_sw_heep_Proton_Analysis_Distributions.pdf" &
exit 0
