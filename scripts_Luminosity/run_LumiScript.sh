#! /bin/bash

#Input run numbers                                                                                                 
inputFile="/home/trottar/ResearchNP/ROOTAnalysis/kaonlt_analysis/lumiscan/inputRuns"                                                                              
                                                                                                                   
while IFS='' read -r line || [[ -n "$line" ]];                                                                     
do                                                                                                                 
    echo "Run number read from file: $line"                                                                        
    #Which run                                                                                                     
    runNum=$line
    #Number of events
    numEvts=-1 
    #Number of runs for plots
    numRuns=5;
    #Script to run
    script="run_LumiYield.C"
    plotScript="plot_LumiYield.C" 
    #Parameters for script 
    runScript="root -l -b -q \"${script}(${runNum},${numEvts})\""
    runPlotScript="root -l -b -q \"${plotScript}(${numRuns})\""
    #Excecute                                                                                                      
    echo "Running ${script} for run  ${runNum}"
    eval ${runScript}
    sleep 2
    mv OUTPUT/Luminosity_PID.pdf OUTPUT/Luminosity_PID_${runNum}.pdf
    echo "File name Luminosity_PID.pdf changed to Luminosity_PID_${runNum}.pdf"
    mv OUTPUT/Luminosity_PID.root OUTPUT/Luminosity_PID_${runNum}.root
    echo "File name Luminosity_PID.root changed to Luminosity_PID_${runNum}.root"
    sleep 2
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 
    echo "END OF RUN ${runNum}"                                                                                   
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 
done < "$inputFile" 

echo "Running ${plotScript}"
eval ${runPlotScript}
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"          
echo "END OF SCRIPT"                                                                                        
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
