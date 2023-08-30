#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2023-08-30 12:39:44 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from matplotlib.backends.backend_pdf import PdfPages
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

################################################################################################################################################

settingList = ["10p6cl1","10p6cl2","10p6cl3","8p2cl1"]
momentumList = [-3.266, -4.204, -6.269, -5.745] # HMS

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
        # Drop column if empty, prevents issues with singles
        data = data[data['HMS_PS'].notnull()]
        # replace NaN with the mean of column
        data = data.fillna(data.mean())
        print(inp_f)
        print(data.keys())
        dataDict[s]['momentum'] = momentumList[i]
        dataDict[s]['current'] = data['current']
        dataDict[s]['run number'] = data['run number']
        dataDict[s]['rel_yield'] = data['yieldRel_HMS_track']
        dataDict[s]['yield'] = data['yield_HMS_track']
        dataDict[s]['yield_error'] = data['uncern_yieldRel_HMS_track']
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
# Linear regression (unweighted)
all_reg_uw = sm.OLS(all_relyield, sm.add_constant(all_current)).fit()
# Linear regression (weighted)
all_reg = sm.WLS(all_relyield, sm.add_constant(all_current), weights=1.0/all_uncern_relyield**2).fit()
all_expected_y = all_reg.predict(sm.add_constant(all_current))
residuals = all_relyield - all_expected_y
all_chi_sq = np.sum((residuals)**2 / np.array(all_uncern_relyield)**2)
#corr_y = all_relyield - residuals
corr_y = all_relyield

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

# Create a PDF file
with PdfPages(SCRIPTPATH+'/luminosity/OUTPUTS/plots/hms_regression_current_%s.pdf' % target) as pdf:


    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['run number'], eff_boil, yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Run Number')
    plt.ylabel('Boil Factor')
    plt.title('HMS Boil Factor vs Run Number')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)
    
    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    #plt.errorbar(all_current[:,0], corr_y[:,0], yerr=all_uncern_relyield[:,0], markersize=10.0, fmt='o', label="Corrected Data", color='teal')  
    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2} = {3:0.2e}".format(s,dataDict[s]['momentum'],r'$\overline{\epsilon_{boil}}$',np.average(eff_boil)), color=color_list[i])
    plt.plot(all_current, all_reg.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='purple', label='Weighted linear regression\n{0}={1:0.2e}\nm={2:0.2e}, b={3:0.2e}'.format(r'$\chi^2$',all_chi_sq,all_reg.params[1],all_reg.params[0]))
    plt.plot(all_current, all_reg_uw.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='violet', label='Unweighted linear regression')
    # calculate the upper and lower confidence intervals for the regression line
    conf_int = all_reg.conf_int() # 95% confidence level
    upper_bounds = conf_int[0][0] + conf_int[1][0]*np.sort(all_current[:,0]) # mx+b, upper
    lower_bounds = conf_int[0][1] + conf_int[1][1]*np.sort(all_current[:,0]) # mx+b, lower
    plt.fill_between(np.sort(all_current[:,0]), upper_bounds, lower_bounds, alpha=0.2)

    # print the slope, intercept, and chi-squared value
    print('\n\nSlope:', all_reg.params[1])
    print('Intercept:', all_reg.params[0])
    print('Chi-squared:', all_chi_sq,"\n\n")
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('HMS Rel. Yield vs Current')
    plt.legend()
    #plt.show()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['y'][:,0], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2}={3:0.2e}".format(s,dataDict[s]['momentum'],r'$\chi^2$',dataDict[s]['chi_sq']), color=color_list[i])
        plt.plot(dataDict[s]['x'], dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x'])), linewidth=2.0, linestyle=style_list[i], color=color_list[i])
        # print the slope, intercept, and chi-squared value
        print('Slope:', dataDict[s]['reg'].params[1])
        print('Intercept:', dataDict[s]['reg'].params[0])
        print('Chi-squared:', dataDict[s]['chi_sq'])
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('HMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    slope, intercept = np.polyfit(all_expected_y, all_relyield, 1, w=1/all_uncern_relyield[:,0])
    ext_x = np.linspace(0.0,np.max(all_expected_y)+1,100)
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['expected_y'], dataDict[s]['y'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(ext_x, slope*ext_x+intercept, linewidth=2.0, linestyle=':', color='purple', label='Linear fit')
    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.xlim(0.9,1.1)
    plt.title('Rel. Yield vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        tmp_res = dataDict[s]['y'][:,0]-dataDict[s]['expected_y']
        plt.errorbar(dataDict[s]['expected_y'], tmp_res, fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])

    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Residuals')
    #plt.ylim(0.5,0.5)
    plt.xlim(0.9,1.1)
    plt.title('Residuals vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['yield'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Yield')
    plt.title('HMS Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], np.ones_like(dataDict[s]['x'][:,0])*dataDict[s]['momentum'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}".format(s), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Momentum')
    plt.title('HMS Momentum vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

settingList = ["10p6cl3","8p2cl1"]
momentumList = [-6.269, -5.745] # SHMS

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
        # Drop column if empty, prevents issues with singles
        data = data[data['SHMS_PS'].notnull()]
        # replace NaN with the mean of column
        data = data.fillna(data.mean())
        print(inp_f)
        print(data.keys())
        dataDict[s]['momentum'] = momentumList[i]
        dataDict[s]['current'] = data['current']
        dataDict[s]['run number'] = data['run number']
        dataDict[s]['rel_yield'] = data['yieldRel_SHMS_track']
        dataDict[s]['yield'] = data['yield_SHMS_track']
        dataDict[s]['yield_error'] = data['uncern_yieldRel_SHMS_track']
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
        all_relyield = np.concatenate([all_relyield, data['yieldRel_SHMS_track']])
        all_uncern_relyield = np.concatenate([all_uncern_relyield, data['yieldRel_SHMS_track']*data['uncern_yieldRel_SHMS_track']])
        
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(0)

print(dataDict.keys())
print(dataDict.values())

################################################################################################################################################

all_current = all_current[:, np.newaxis]
all_relyield = all_relyield[:, np.newaxis]
all_uncern_relyield = all_uncern_relyield[:, np.newaxis]
# Linear regression (unweighted)
all_reg_uw = sm.OLS(all_relyield, sm.add_constant(all_current)).fit()
# Linear regression (weighted)
all_reg = sm.WLS(all_relyield, sm.add_constant(all_current), weights=1.0/all_uncern_relyield**2).fit()
all_expected_y = all_reg.predict(sm.add_constant(all_current))
residuals = all_relyield - all_expected_y
all_chi_sq = np.sum((residuals)**2 / np.array(all_uncern_relyield)**2)
#corr_y = all_relyield - residuals
corr_y = all_relyield

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

# Create a PDF file
with PdfPages(SCRIPTPATH+'/luminosity/OUTPUTS/plots/shms_regression_current_%s.pdf' % target) as pdf:

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['run number'], eff_boil, yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Run Number')
    plt.ylabel('Boil Factor')
    plt.title('SHMS Boil Factor vs Run Number')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)
    
    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    #plt.errorbar(all_current[:,0], corr_y[:,0], yerr=all_uncern_relyield[:,0], markersize=10.0, fmt='o', label="Corrected Data", color='black')    
    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2} = {3:0.2e}".format(s,dataDict[s]['momentum'],r'$\overline{\epsilon_{boil}}$',np.average(eff_boil)), color=color_list[i])
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(all_current, all_reg.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='purple', label='Weighted linear regression\n{0}={1:0.2e}\nm={2:0.2e}, b={3:0.2e}'.format(r'$\chi^2$',all_chi_sq,all_reg.params[1],all_reg.params[0]))
    plt.plot(all_current, all_reg_uw.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='violet', label='Unweighted linear regression')
    # calculate the upper and lower confidence intervals for the regression line
    conf_int = all_reg.conf_int() # 95% confidence level
    upper_bounds = conf_int[0][0] + conf_int[1][0]*np.sort(all_current[:,0]) # mx+b, upper
    lower_bounds = conf_int[0][1] + conf_int[1][1]*np.sort(all_current[:,0]) # mx+b, lower
    plt.fill_between(np.sort(all_current[:,0]), upper_bounds, lower_bounds, alpha=0.2)
    # print the slope, intercept, and chi-squared value
    print('\n\nSlope:', all_reg.params[1])
    print('Intercept:', all_reg.params[0])
    print('Chi-squared:', all_chi_sq,"\n\n")
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('SHMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['y'][:,0], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2}={3:0.2e}".format(s,dataDict[s]['momentum'],r'$\chi^2$',dataDict[s]['chi_sq']), color=color_list[i])
        plt.plot(dataDict[s]['x'], dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x'])), linewidth=2.0, linestyle=style_list[i], color=color_list[i])
        # print the slope, intercept, and chi-squared value
        print('Slope:', dataDict[s]['reg'].params[1])
        print('Intercept:', dataDict[s]['reg'].params[0])
        print('Chi-squared:', dataDict[s]['chi_sq'])
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('SHMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    slope, intercept = np.polyfit(all_expected_y, all_relyield, 1, w=1/all_uncern_relyield[:,0])
    ext_x = np.linspace(0.0,np.max(all_expected_y)+1,100)
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['expected_y'], dataDict[s]['y'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(ext_x, slope*ext_x+intercept, linewidth=2.0, linestyle=':', color='purple', label='Linear fit')
    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.xlim(0.9,1.1)
    plt.title('Rel. Yield vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        tmp_res = dataDict[s]['y'][:,0]-dataDict[s]['expected_y']
        plt.errorbar(dataDict[s]['expected_y'], tmp_res, fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])

    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Residuals')
    #plt.ylim(0.5,0.5)
    plt.xlim(0.9,1.1)
    plt.title('Residuals vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['yield'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Yield')
    plt.title('SHMS Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], np.ones_like(dataDict[s]['x'][:,0])*dataDict[s]['momentum'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}".format(s), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Momentum')
    plt.title('SHMS Momentum vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

#settingList = ["10p6lh2l1","10p6lh2l2","10p6lh2l3","8p2lh2l1"]
#momentumList = [-3.266, -4.204, -6.269, -5.745] # HMS
# Removing 10p6 l3 because of terrible TLT for almost all runs
settingList = ["10p6lh2l1","10p6lh2l2","8p2lh2l1"]
momentumList = [-3.266, -4.204, -5.745] # HMS

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
        # Drop column if empty, prevents issues with singles
        data = data[data['HMS_PS'].notnull()]
        # replace NaN with the mean of column
        data = data.fillna(data.mean())
        print(inp_f)
        print(data.keys())
        dataDict[s]['momentum'] = momentumList[i]
        dataDict[s]['current'] = data['current']
        dataDict[s]['run number'] = data['run number']
        dataDict[s]['rel_yield'] = data['yieldRel_HMS_track']
        dataDict[s]['yield'] = data['yield_HMS_track']
        dataDict[s]['yield_error'] = data['uncern_yieldRel_HMS_track']
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
# Linear regression (unweighted)
all_reg_uw = sm.OLS(all_relyield, sm.add_constant(all_current)).fit()
# Linear regression (weighted)
all_reg = sm.WLS(all_relyield, sm.add_constant(all_current), weights=1.0/all_uncern_relyield**2).fit()
all_expected_y = all_reg.predict(sm.add_constant(all_current))
residuals = all_relyield - all_expected_y
all_chi_sq = np.sum((residuals)**2 / np.array(all_uncern_relyield)**2)
#corr_y = all_relyield - residuals
corr_y = all_relyield

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

# Create a PDF file
with PdfPages(SCRIPTPATH+'/luminosity/OUTPUTS/plots/hms_regression_current_%s.pdf' % target) as pdf:

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['run number'], eff_boil, yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Run Number')
    plt.ylabel('Boil Factor')
    plt.title('HMS Boil Factor vs Run Number')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)
    
    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    #plt.errorbar(all_current[:,0], corr_y[:,0], yerr=all_uncern_relyield[:,0], markersize=10.0, fmt='o', label="Corrected Data", color='black')    
    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2} = {3:0.2e}".format(s,dataDict[s]['momentum'],r'$\overline{\epsilon_{boil}}$',np.average(eff_boil)), color=color_list[i])
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(all_current, all_reg.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='purple', label='Weighted linear regression\n{0}={1:0.2e}\nm={2:0.2e}, b={3:0.2e}'.format(r'$\chi^2$',all_chi_sq,all_reg.params[1],all_reg.params[0]))
    plt.plot(all_current, all_reg_uw.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='violet', label='Unweighted linear regression')
    # calculate the upper and lower confidence intervals for the regression line
    conf_int = all_reg.conf_int() # 95% confidence level
    upper_bounds = conf_int[0][0] + conf_int[1][0]*np.sort(all_current[:,0]) # mx+b, upper
    lower_bounds = conf_int[0][1] + conf_int[1][1]*np.sort(all_current[:,0]) # mx+b, lower
    plt.fill_between(np.sort(all_current[:,0]), upper_bounds, lower_bounds, alpha=0.2)
    # print the slope, intercept, and chi-squared value
    print('\n\nSlope:', all_reg.params[1])
    print('Intercept:', all_reg.params[0])
    print('Chi-squared:', all_chi_sq,"\n\n")
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('HMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['y'][:,0], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2}={3:0.2e}".format(s,dataDict[s]['momentum'],r'$\chi^2$',dataDict[s]['chi_sq']), color=color_list[i])
        plt.plot(dataDict[s]['x'], dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x'])), linewidth=2.0, linestyle=style_list[i], color=color_list[i])
        # print the slope, intercept, and chi-squared value
        print('Slope:', dataDict[s]['reg'].params[1])
        print('Intercept:', dataDict[s]['reg'].params[0])
        print('Chi-squared:', dataDict[s]['chi_sq'])
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('HMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    slope, intercept = np.polyfit(all_expected_y, all_relyield, 1, w=1/all_uncern_relyield[:,0])
    ext_x = np.linspace(0.0,np.max(all_expected_y)+1,100)
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['expected_y'], dataDict[s]['y'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(ext_x, slope*ext_x+intercept, linewidth=2.0, linestyle=':', color='purple', label='Linear fit')
    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.xlim(0.9,1.1)
    plt.title('Rel. Yield vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        tmp_res = dataDict[s]['y'][:,0]-dataDict[s]['expected_y']
        plt.errorbar(dataDict[s]['expected_y'], tmp_res, fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])

    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Residuals')
    #plt.ylim(0.5,0.5)
    plt.xlim(0.9,1.1)
    plt.title('Residuals vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['yield'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Yield')
    plt.title('HMS Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], np.ones_like(dataDict[s]['x'][:,0])*dataDict[s]['momentum'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}".format(s), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Momentum')
    plt.title('HMS Momentum vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

settingList = ["10p6lh2l3","8p2lh2l1"]
momentumList = [-6.269, -5.745] # SHMS

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
        # Drop column if empty, prevents issues with singles
        data = data[data['SHMS_PS'].notnull()]
        # replace NaN with the mean of column
        data = data.fillna(data.mean())
        print(inp_f)
        print(data.keys())
        dataDict[s]['momentum'] = momentumList[i]
        dataDict[s]['current'] = data['current']
        dataDict[s]['run number'] = data['run number']
        dataDict[s]['rel_yield'] = data['yieldRel_SHMS_track']
        dataDict[s]['yield'] = data['yield_SHMS_track']
        dataDict[s]['yield_error'] = data['uncern_yieldRel_SHMS_track']
        # reshape the currents, yields, and yield errors into column vectors
        dataDict[s]['x'] = dataDict[s]["current"][:, np.newaxis]
        dataDict[s]['y'] = dataDict[s]["rel_yield"][:, np.newaxis]
        dataDict[s]['yerr'] = dataDict[s]["yield_error"][:, np.newaxis]

        # create a linear regression object and fit the data
        # perform unweighted least squares regression
        #dataDict[s]['reg'] = LinearRegression().fit(dataDict[s]['x'], dataDict[s]['y'])
        # perform weighted least squares regression
        dataDict[s]['reg'] = sm.WLS(dataDict[s]['y'], sm.add_constant(dataDict[s]['x']), weights=1.0/dataDict[s]['yerr']**2).fit()

        # calculate the chi-squared value
        dataDict[s]['expected_y'] = dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x']))
        dataDict[s]['chi_sq'] = np.sum(((np.array(dataDict[s]['y']) - np.array(dataDict[s]['expected_y']))/np.array(dataDict[s]['yerr']))**2)

        all_current = np.concatenate([all_current, data['current']])
        all_relyield = np.concatenate([all_relyield, data['yieldRel_SHMS_track']])
        all_uncern_relyield = np.concatenate([all_uncern_relyield, data['yieldRel_SHMS_track']*data['uncern_yieldRel_SHMS_track']])
        
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(0)

print(dataDict.keys())
print(dataDict.values())

################################################################################################################################################

all_current = all_current[:, np.newaxis]
all_relyield = all_relyield[:, np.newaxis]
all_uncern_relyield = all_uncern_relyield[:, np.newaxis]
# Least Squares Linear regression (unweighted)
all_reg_uw = sm.OLS(all_relyield, sm.add_constant(all_current)).fit()
# Least Squares Linear regression (weighted)
all_reg = sm.WLS(all_relyield, sm.add_constant(all_current), weights=1.0/all_uncern_relyield**2).fit()
all_expected_y = all_reg.predict(sm.add_constant(all_current))
residuals = all_relyield - all_expected_y
all_chi_sq = np.sum((residuals)**2 / np.array(all_uncern_relyield)**2)
#corr_y = all_relyield - residuals
corr_y = all_relyield

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

# Create a PDF file
with PdfPages(SCRIPTPATH+'/luminosity/OUTPUTS/plots/shms_regression_current_%s.pdf' % target) as pdf:

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['run number'], eff_boil, yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Run Number')
    plt.ylabel('Boil Factor')
    plt.title('SHMS Boil Factor vs Run Number')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)
    
    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    #plt.errorbar(all_current[:,0], corr_y[:,0], yerr=all_uncern_relyield[:,0], markersize=10.0, fmt='o', label="Corrected Data", color='black')    
    for i, s in enumerate(settingList):
        m0 = dataDict[s]['reg'].params[1]/dataDict[s]['reg'].params[0]
        eff_boil = 1 - m0*dataDict[s]['current']
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2} = {3:0.2e}".format(s,dataDict[s]['momentum'],r'$\overline{\epsilon_{boil}}$',np.average(eff_boil)), color=color_list[i])
        plt.errorbar(dataDict[s]['current'], dataDict[s]['corr_y'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(all_current, all_reg.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='purple', label='Weighted linear regression\n{0}={1:0.2e}\nm={2:0.2e}, b={3:0.2e}'.format(r'$\chi^2$',all_chi_sq,all_reg.params[1],all_reg.params[0]))
    plt.plot(all_current, all_reg_uw.predict(sm.add_constant(all_current)), linewidth=2.0, linestyle=':', color='violet', label='Unweighted linear regression')
    # calculate the upper and lower confidence intervals for the regression line
    conf_int = all_reg.conf_int() # 95% confidence level
    upper_bounds = conf_int[0][0] + conf_int[1][0]*np.sort(all_current[:,0]) # mx+b, upper
    lower_bounds = conf_int[0][1] + conf_int[1][1]*np.sort(all_current[:,0]) # mx+b, lower
    plt.fill_between(np.sort(all_current[:,0]), upper_bounds, lower_bounds, alpha=0.2)
    # print the slope, intercept, and chi-squared value
    print('\n\nSlope:', all_reg.params[1])
    print('Intercept:', all_reg.params[0])
    print('Chi-squared:', all_chi_sq,"\n\n")
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('SHMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['y'][:,0], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}\n{2}={3:0.2e}".format(s,dataDict[s]['momentum'],r'$\chi^2$',dataDict[s]['chi_sq']), color=color_list[i])
        plt.plot(dataDict[s]['x'], dataDict[s]['reg'].predict(sm.add_constant(dataDict[s]['x'])), linewidth=2.0, linestyle=style_list[i], color=color_list[i])
        # print the slope, intercept, and chi-squared value
        print('Slope:', dataDict[s]['reg'].params[1])
        print('Intercept:', dataDict[s]['reg'].params[0])
        print('Chi-squared:', dataDict[s]['chi_sq'])
    plt.xlabel('Current')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.title('SHMS Rel. Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    slope, intercept = np.polyfit(all_expected_y, all_relyield, 1, w=1/all_uncern_relyield[:,0])
    ext_x = np.linspace(0.0,np.max(all_expected_y)+1,100)
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['expected_y'], dataDict[s]['y'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.plot(ext_x, slope*ext_x+intercept, linewidth=2.0, linestyle=':', color='purple', label='Linear fit')
    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Rel. Yield')
    plt.ylim(0.9,1.1)
    plt.xlim(0.9,1.1)
    plt.title('Rel. Yield vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    for i, s in enumerate(settingList):
        tmp_res = dataDict[s]['y'][:,0]-dataDict[s]['expected_y']
        plt.errorbar(dataDict[s]['expected_y'], tmp_res, fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])

    plt.xlabel('Predicted Rel. Yield')
    plt.ylabel('Residuals')
    #plt.ylim(0.5,0.5)
    plt.xlim(0.9,1.1)
    plt.title('Residuals vs Predicted')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], dataDict[s]['yield'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}, P = {1}".format(s,dataDict[s]['momentum']), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Yield')
    plt.title('SHMS Yield vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(12,8))

    # plot the data with error bars and the regression line
    for i, s in enumerate(settingList):
        plt.errorbar(dataDict[s]['x'][:,0], np.ones_like(dataDict[s]['x'][:,0])*dataDict[s]['momentum'], yerr=dataDict[s]['yield_error'], fmt=fmt_list[i], label="{0}".format(s), color=color_list[i])
    plt.xlabel('Current')
    plt.ylabel('Momentum')
    plt.title('SHMS Momentum vs Current')
    plt.legend()

    pdf.savefig(fig)
    plt.close(fig)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
