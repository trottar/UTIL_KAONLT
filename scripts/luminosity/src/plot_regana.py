#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-05-15 13:31:09 trottar"
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
import statsmodels.api as sm
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
momentumList = [-3.266, -4.204, -6.269, -5.745] # HMS
#momentumList = [6.842, 6.053, -6.269, -5.745] # SHMS

dataDict = {}

all_relyield = np.array([])
all_uncern_relyield = np.array([])
all_current = np.array([])

for i,s in enumerate(settingList):
    dataDict[s] = {}
    data_val = data_path.get_file(s,SCRIPTPATH)
    target = data_val[0]
    inp_f = data_val[2] # out_f is inp_f for global analysis

    # Converts csv data to dataframe
    try:
        data = pd.read_csv(inp_f)
        # replace NaN values with the mean of the column
        data = data.fillna(data.mean())
        print(inp_f)
        print(data.keys())
        dataDict[s]['momentum'] = momentumList[i]
        dataDict[s]['current'] = data['current']
        dataDict[s]['rel_yield'] = data['yieldRel_HMS_track']
        dataDict[s]['yield'] = data['yield_HMS_track']
        dataDict[s]['yield_error'] = data['yieldRel_HMS_track']*data['uncern_yieldRel_HMS_track']
        # reshape the currents, yields, and yield errors into column vectors
        dataDict[s]['x'] = dataDict[s]["current"][:, np.newaxis]
        dataDict[s]['y'] = dataDict[s]["rel_yield"][:, np.newaxis]
        dataDict[s]['yerr'] = dataDict[s]["yield_error"][:, np.newaxis]

        # create a linear regression object and fit the data
        #dataDict[s]['reg'] = LinearRegression().fit(dataDict[s]['x'], dataDict[s]['y'])
        # perform weighted least squares regression
        dataDict[s]['reg'] = sm.WLS(dataDict[s]['y'], sm.add_constant(dataDict[s]['x']), weights=1.0/dataDict[s]['yerr']**2).fit()

        # calculate the chi-squared value
        dataDict[s]['expected_y'] = dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x']))
        dataDict[s]['chi_sq'] = np.sum(((np.array(dataDict[s]['y']) - np.array(dataDict[s]['expected_y']))/np.array(dataDict[s]['yerr']))**2)

        all_current = np.concatenate([all_current, data['current']])
        all_relyield = np.concatenate([all_relyield, data['yieldRel_HMS_track']])
        all_uncern_relyield = np.concatenate([all_uncern_relyield, data['yieldRel_HMS_track']*data['uncern_yieldRel_HMS_track']])
        
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(0)

print(dataDict.keys())
print(dataDict.values())

################################################################################################################################################

all_current = all_current[:, np.newaxis]
all_relyield = all_relyield[:, np.newaxis]
all_uncern_relyield = all_uncern_relyield[:, np.newaxis]
#all_reg = LinearRegression().fit(all_current, all_relyield)
all_reg = sm.WLS(all_relyield, sm.add_constant(all_current), weights=1.0/all_uncern_relyield**2).fit()
all_expected_y = all_reg.predict(sm.add_constant(all_current))
residuals = all_relyield - all_expected_y
all_chi_sq = np.sum((residuals)**2 / np.array(all_uncern_relyield)**2)
corr_y = all_relyield - residuals

i = 0
for s in settingList:
    tmp1 = []
    tmp2 = []
    for val in dataDict[s]['current']:
        tmp1.append(corr_y[:,0][i])
        tmp2.append(residuals[:,0][i])
        i+=1
    dataDict[s]['corr_y'] = tmp1
    dataDict[s]['residuals'] = tmp2

################################################################################################################################################

# Define a list of error bar formats and plot styles to cycle through
fmt_list = ['o', 's', '^', 'd']
style_list = ['-', '--', ':', '-.']
color_list = ['red', 'green', 'blue', 'orange']

relyield_fig = plt.figure(figsize=(12,8))

# plot the data with error bars and the regression line
for i, s in enumerate(settingList):
    plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    #plt.scatter(dataDict[s]['current'], dataDict[s]['corr_y'], label="{0}, {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
plt.plot(all_current, all_reg.predict(sm.add_constant(all_current)), linewidth = 2.0, linestyle=':', color='purple')
conf_int = all_reg..conf_int(alpha=0.05)
upper_bounds = conf_int[:, 0]
lower_bounds = conf_int[:, 1]
plt.fill_between(all_current[:,0], upper_bounds, lower_bounds, alpha=0.2)
# print the slope, intercept, and chi-squared value
print('\n\nSlope:', all_reg.params[1])
print('Intercept:', all_reg.params[0])
print('Chi-squared:', all_chi_sq,"\n\n")
plt.xlabel('Current')
plt.ylabel('Rel. Yield')
plt.title('Rel. Yield vs Current')
plt.legend()

relyield_fig = plt.figure(figsize=(12,8))

# plot the data with error bars and the regression line
for i, s in enumerate(settingList):
    plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['y'][:,0], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(dataDict[s]['x'], dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x'])), linewidth = 2.0, linestyle=style_list[i], color=color_list[i])
    conf_int = dataDict[s]['reg'].conf_int(alpha=0.05)
    upper_bounds = conf_int[:, 0]
    lower_bounds = conf_int[:, 1]
    plt.fill_between(dataDict[s]['x'][:,0], upper_bounds, lower_bounds, alpha=0.2)
    # print the slope, intercept, and chi-squared value
    print('Slope:', dataDict[s]['reg'].params[1])
    print('Intercept:', dataDict[s]['reg'].params[0])
    print('Chi-squared:', dataDict[s]['chi_sq'])
plt.xlabel('Current')
plt.ylabel('Rel. Yield')
plt.title('Rel. Yield vs Current')
plt.legend()

yield_fig = plt.figure(figsize=(12,8))

# plot the data with error bars and the regression line
for i, s in enumerate(settingList):
    plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['yield'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
plt.xlabel('Current')
plt.ylabel('Yield')
plt.title('Yield vs Current')
plt.legend()

momentum_fig = plt.figure(figsize=(12,8))

# plot the data with error bars and the regression line
for i, s in enumerate(settingList):
    plt.errorbar(dataDict[s]['x'][:,0], np.ones_like(dataDict[s]['x'][:,0])*dataDict[s]['momentum'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}".format(s), color=color_list[i])
plt.xlabel('Current')
plt.ylabel('Momentum')
plt.title('Momentum vs Current')
plt.legend()

plt.show()
