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
{ 

echo "Running ${script} for run  ${runNum}"
# eval ${runScript}
python run_LumiYield.py runNum numEvts

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"          
echo "END OF RUN ${runNum}"                                                                                        
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 

}

# done < "$inputFile" 
