#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2022-06-13 08:09:01 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

while getopts 'hp' flag; do
    case "${flag}" in
        h) 
        echo "---------------------------------------------------"
        echo "./add_efficiencies_table.sh -{flags} {run list}"
        echo "---------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -p, plot efficiencies"
        exit 0
        ;;
        p) p_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

# Runs script in the ltsep python package that grabs current path enviroment
if [[ ${HOSTNAME} = *"cdaq"* ]]; then
    PATHFILE_INFO=`python3 /home/cdaq/pionLT-2021/hallc_replay_lt/UTIL_PION/bin/python/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
elif [[ "${HOSTNAME}" = *"farm"* ]]; then
    PATHFILE_INFO=`python3 /u/home/${USER}/.local/lib/python3.4/site-packages/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
fi

# Split the string we get to individual variables, easier for printing and use later
VOLATILEPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f1` # Cut the string on , delimitter, select field (f) 1, set variable to output of command
ANALYSISPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f2`
HCANAPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f3`
REPLAYPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f4`
UTILPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f5`
PACKAGEPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f6`
OUTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f7`
ROOTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f8`
REPORTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f9`
CUTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f10`
PARAMPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f11`
SCRIPTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f12`
ANATYPE=`echo ${PATHFILE_INFO} | cut -d ','  -f13`
USER=`echo ${PATHFILE_INFO} | cut -d ','  -f14`
HOST=`echo ${PATHFILE_INFO} | cut -d ','  -f15`

cd "${SCRIPTPATH}/efficiency/src/"

if [[ $p_flag = "true" ]]; then
    RunType=$2
    DATE=$3
    python3 plot_efficiency.py replay_coin_production ${RunType} ${DATE}
    exit 1
else
    RunType=$1
fi

if [[ $RunType = "HeePCoin" ]]; then
    inputFile="${REPLAYPATH}/UTIL_BATCH/InputRunLists/KaonLT_2018_2019/HeepCoin_ALL"

    while true; do
	read -p "Do you wish to append efficiency table with run list ${RunList}? (Please answer yes or no) " yn
	case $yn in
	    [Yy]* )
		i=-1
		(
		##Reads in input file##
		while IFS='' read -r line || [[ -n "$line" ]]; do
		    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		    echo "Run number read from file: $line"
		    echo ""
		    python3 efficiency_main.py replay_coin_production $RunType $line -1
		done < "$inputFile"
		)
		break;;
	    [Nn]* ) 
		exit;;
	    * ) echo "Please answer yes or no.";;
	esac
    done
else
    inputFile="${REPLAYPATH}/UTIL_BATCH/InputRunLists/KaonLT_2018_2019/ProductionLH2_ALL"

    while true; do
	read -p "Do you wish to append efficiency table with run list ${RunList}? (Please answer yes or no) " yn
	case $yn in
	    [Yy]* )
		i=-1
		(
		##Reads in input file##
		while IFS='' read -r line || [[ -n "$line" ]]; do
		    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		    echo "Run number read from file: $line"
		    echo ""
		    python3 efficiency_main.py replay_coin_production $RunType $line -1
		done < "$inputFile"
		)
		break;;
	    [Nn]* ) 
		exit;;
	    * ) echo "Please answer yes or no.";;
	esac
    done
fi
