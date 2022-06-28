#!/bin/bash

# Runs script in the ltsep python package that grabs current path enviroment
if [[ ${HOSTNAME} = *"cdaq"* ]]; then
    PATHFILE_INFO=`python3 /home/cdaq/pionLT-2021/PythonPackages3.6/lib/python3.6/site-packages/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
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

# Define flags for grabbing trigger windows of one or multiple runs
while getopts 'hpa' flag; do
    case "${flag}" in
	h)
	    echo "The following flags can be called for the luminosity analysis..."
	    echo "    -h, help"
	    echo "    -p, plot trig cuts (requires additional arguments)"
	    echo "    -a, plot trig cuts for all lumi runs"
	    exit 0 ;;
	p) p_flag='true' ;;
	a) a_flag='true' ;;
	*) print_usage
	exit 1 ;;
    esac
done

# Grab inputs depending on flags used
if [[ $p_flag != "true" && $a_flag != "true" ]]; then
    echo "I take as arguments the Run Number and max number of events!"
    RUNNUMBER=$1
    MAXEVENTS=$2
    #MAXEVENTS=12500
    if [[ $1 -eq "" ]]; then
	echo "I need a Run Number!"
	exit 2
    fi
    if [[ $2 -eq "" ]]; then
	echo "Only Run Number entered...I'll assume -1 events!" 
	MAXEVENTS=-1 
    fi
elif [[ $a_flag == "true" ]]; then
    echo "I take as arguments the Run Number and max number of events!"
    RUNNUMBER=$2
    MAXEVENTS=$3
    #MAXEVENTS=12500
    if [[ $2 -eq "" ]]; then
	echo "I need a Run Number!"
	exit 2
    fi
    if [[ $3 -eq "" ]]; then
	echo "Only Run Number entered...I'll assume -1 events!" 
	MAXEVENTS=-1 
    fi
elif [[ $p_flag == "true" ]]; then
    echo "I take as arguments the Run Number and max number of events!"
    RUNNUMBER=$2
    MAXEVENTS=$3
    #MAXEVENTS=12500
    if [[ $2 -eq "" ]]; then
	echo "I need a Run Number!"
	exit 2
    fi
    if [[ $3 -eq "" ]]; then
	echo "Only Run Number entered...I'll assume -1 events!" 
	MAXEVENTS=-1 
    fi
fi

# Get trigger windows for a particular run
if [[ $p_flag = "true" ]]; then
    cd ${UTILPATH}/scripts/trig_windows/src/
    python3 plot_trig.py Lumi ${ANATYPE}_replay_luminosity ${RUNNUMBER} ${MAXEVENTS}
# Get trigger windows for all runs
elif [[ $a_flag = "true" ]]; then
    cd ${UTILPATH}/scripts/trig_windows/src/
    python3 reana_trig.py
    cd ${UTILPATH}/scripts/trig_windows/OUTPUTS/
    convert curr_${ANATYPE}_replay_* trig_${ANATYPE}_replay_* curr_trig_cuts.pdf
else
    cd ${UTILPATH}/scripts/trig_windows/src/
    python3 trigcuts.py Lumi ${ANATYPE}_replay_luminosity ${RUNNUMBER} ${MAXEVENTS}
fi
