#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-05-15 07:53:43 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sys, os

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
USER=lt.USER # Grab user info for file finding
HOST=lt.HOST
REPLAYPATH=lt.REPLAYPATH
UTILPATH=lt.UTILPATH
SCRIPTPATH=lt.SCRIPTPATH
ANATYPE=lt.ANATYPE

################################################################################################################################################

print("\nRunning as %s on %s, hallc_replay_lt path assumed as %s" % (USER, HOST, REPLAYPATH))

sys.path.insert(0,"%s/luminosity/src/%sLT" % (SCRIPTPATH,ANATYPE))
import data_path

settingList = ["10p6cl1","10p6cl2","10p6cl3","8p2cl1"]

dataDict = {}

for s in settingList:
    data_val = data_path.get_file(s,SCRIPTPATH)
    target = data_val[0]
    inp_f = data_val[2] # out_f is inp_f for global analysis

    # Converts csv data to dataframe
    try:
        data = pd.read_csv(inp_f)
        print(inp_f)
        print(data.keys())
        dataDict[s]['current'] = data['current']
        dataDict[s]['yield'] = data['yieldRel_HMS_track']
        dataDict[s]['yield_error'] = data['uncern_yieldRel_HMS_track']
        # reshape the currents, yields, and yield errors into column vectors
        dataDict[s]['x'] = dataDict[s]["current"].reshape(-1, 1)
        dataDict[s]['y'] = dataDict[s]["yield"].reshape(-1, 1)

        # create a linear regression object and fit the data
        dataDict[s]['reg'] = LinearRegression().fit(dataDict[s]['x'], dataDict[s]['y'])

        # calculate the chi-squared value
        dataDict[s]['expected_y'] = reg.predict(dataDict[s]['x'])
        dataDict[s]['chi_squared'] = np.sum((dataDict[s]['y'] - dataDict[s]['expected_y'])**2 / dataDict[s]["yield_error"]**2)
        
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(0)

print(dataDict.keys())
print(dataDict.values())
        
################################################################################################################################################

# plot the data with error bars and the regression line
for s in settingList:
    plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['y'][:,0], yerr=dataDict[s]["yield_error"], fmt='o', label='Data')
    plt.plot(dataDict[s]['x'], dataDict[s]['reg'].predict(dataDict[s]['x']), label='Linear Regression')
    # print the slope, intercept, and chi-squared value
    print('Slope:', dataDict[s]['reg'].coef_[0][0])
    print('Intercept:', dataDict[s]['reg'].intercept_[0])
    print('Chi-squared:', dataDict[s]['chi_squared'])    
plt.xlabel('Current')
plt.ylabel('Yield')
plt.title('Yield vs Current')
plt.legend()
plt.show()
