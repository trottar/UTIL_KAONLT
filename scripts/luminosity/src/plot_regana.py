#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-05-15 07:34:26 trottar"
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
import sys

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

settingsList = ["10p6cl1","10p6cl2","10p6cl3","8p2cl1"]

dataDict = {}

for s in settingList:
    data_path = data_path.get_file(inp_name,SCRIPTPATH)
    target = data_path[0]
    inp_f = data_path[1]
    out_f = data_path[2]

    # Converts csv data to dataframe
    try:
        data = pd.read_csv(inp_f)
        print(inp_f)
        print(data.keys())
        dataDict['current'] = data['current']
        dataDict['yield'] = data['yieldRel_HMS_track']
        dataDict['yield_error'] = data['uncern_yieldRel_HMS_track']
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(0)

################################################################################################################################################

# reshape the currents, yields, and yield errors into column vectors
X = dataDict["current"].reshape(-1, 1)
y = dataDict["yield"].reshape(-1, 1)

# create a linear regression object and fit the data
reg = LinearRegression().fit(X, y)

# calculate the chi-squared value
expected_y = reg.predict(X)
chi_squared = np.sum((y - expected_y)**2 / dataDict["yield_error"]**2)

# plot the data with error bars and the regression line
plt.errorbar(X[:,0], y[:,0], yerr=dataDict["yield_error"], fmt='o', label='Data')
plt.plot(X, reg.predict(X), label='Linear Regression')
plt.xlabel('Current')
plt.ylabel('Yield')
plt.title('Yield vs Current')
plt.legend()
plt.show()

# print the slope, intercept, and chi-squared value
print('Slope:', reg.coef_[0][0])
print('Intercept:', reg.intercept_[0])
print('Chi-squared:', chi_squared)
