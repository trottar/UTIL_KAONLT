#! /bin/bash

# Runs script in the ltsep python package that grabs current path enviroment
if [[ ${HOSTNAME} = *"cdaq"* ]]; then
    PATHFILE_INFO=`python3 /home/cdaq/pionLT-2021/hallc_replay_lt/UTIL_PION/bin/python/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
elif [[ ${HOSTNAME} = *"farm"* ]]; then
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
SIMCPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f16`
LTANAPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f17`

# Function that calls python script to grab run numbers
grab_runs () {
    RunList=$1
    # Location of list of run lists
    INPDIR="${UTILPATH}/run_list/${ANATYPE}LT/${RunList}"
    if [[ -e $INPDIR ]]; then
	cd "${LTANAPATH}/src/setup"
	RunNumArr=$(python3 getRunNumbers.py $INPDIR)
	echo $RunNumArr
    else
	exit
    fi
}

#KIN="Q0p5W2p40"
#KIN="Q2p1W2p95"
#KIN="Q3p0W3p14"
#KIN="Q3p0W2p32"
KIN="Q4p4W2p74"
#KIN="Q5p5W3p02"

TARGET=("LH2" "dummy")
EPS=("high" "low")
PHISET=("center" "left" "right")

for t in "${TARGET[@]}"; do
    for e in "${EPS[@]}"; do
        for p in "${PHISET[@]}"; do

	    if [ $t = "dummy" ]; then
		file_name="${KIN}${p}_${e}e_dummy"
	    else
		file_name="${KIN}${p}_${e}e"
	    fi

	    numbers_to_match=()
	    IFS=', ' read -r -a numbers_to_match <<< "$( grab_runs ${file_name} )"
	    echo
	    echo "${file_name}"
	    echo "Run Numbers: [${numbers_to_match[@]}]"

            # Check if numbers_to_match is empty and break the loop
            if [ ${#numbers_to_match[@]} -eq 0 ]; then
                echo "No run numbers to process. Exiting loop."
                break
            fi

	    inpFile="${UTILPATH}/run_list/${ANATYPE}LT/${file_name}"
	    # Loop through each number in the list
	    for number in "${numbers_to_match[@]}"
	    do
		echo
		echo "Checking ${number}"
		python3 check_CT.py "${REPLAYPATH}/DBASE/COIN/DB_KaonLT/standard_OfflineKaonLT.kinematics" ${number}
	    done
        done
    done
done
