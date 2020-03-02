#! /bin/bash

#Input run numbers                                                                                                 
inputFile="inputRuns"                                                                              

REPLAYPATH="/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt"

# while IFS='' read -r line || [[ -n "$line" ]];                                                                     
# do                                                                                                                 
    # echo "Run number read from file: $line"                                                                        

#Which run                                                                                                         
# runNum=$line            

runNum=$1
    
#Number of events                                                                                                  
numEvts=50000
# numEvts=-1

#Script to run
script="$REPLAYPATH/UTIL_KAONLT/scripts_Luminosity/run_LumiYield.C" 

#Parameters for script 
# runScript="root -l -b -q \"${script}(${runNum},${numEvts})\""
runScript="root -l \"${script}(${runNum},${numEvts})\""

#Excecute
source /site/12gev_phys/2.3/Linux_CentOS7.7.1908-x86_64-gcc4.8.5/root/6.14.04/bin/thisroot.csh

echo "Running ${script} for run  ${runNum}"
# eval ${runScript}
python run_LumiYield.py $runNum $numEvts

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"          
echo "END OF RUN ${runNum}"                                                                                        
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 

