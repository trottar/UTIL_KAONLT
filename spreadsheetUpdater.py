#!/usr/bin/env python
#-*- coding: utf-8 -*-

import xlsxwriter

from PIL import ImageFont

##########################################
#############6.2 GeV######################
##########################################
kin6p2_setting1 = 'Q2=3.0|W=2.32|x=0.40'
kin6p2_center1 = '13.28'
kin6p2_center1_Values = (
    # current
    [70,
     # tPAC
     6,
     # tPACPrime, same as tPAC just sheet 2
     6,
     # qPAC
     0,
     # lambda evnt
     1703,
     # lambda evntPAC
     1550]
)
kin6p2DUM_center1 = '13.28'
kin6p2DUM_center1_Values = (
    # current
    [40,
     # tPAC
     0.4,
     # tPACPrime, same as tPAC just sheet 2
     0.4,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)
kin6p2_left1 = '16.28'
kin6p2_left1_Values = (
    # current
    [70,
     # tPAC
     6,
     # tPACPrime, same as tPAC just sheet 2
     6,
     # qPAC
     0,
     # lambda evnt
     1477,
     # lambda evntPAC
     1550]
)
kin6p2DUM_left1 = '16.28'
kin6p2DUM_left1_Values = (
    # current
    [40,
     # tPAC
     0.4,
     # tPACPrime, same as tPAC just sheet 2
     0.4,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)

##########################################
kin6p2_setting2 = 'Q2=2.115|W=2.95|x=0.21'
kin6p2_center2 = '5.90'
kin6p2_center2_Values = (
    # current
    [55,
     # tPAC
     21,
     # tPACPrime, same as tPAC just sheet 2
     21,
     # qPAC
     0,
     # lambda evnt
     579,
     # lambda evntPAC
     1750]
)
kin6p2DUM_center2 = '5.90'
kin6p2DUM_center2_Values = (
    # current
    [40,
     # tPAC
     1.1,
     # tPACPrime, same as tPAC just sheet 2
     1.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)
kin6p2_left2 = '8.48'
kin6p2_left2_Values = (
    # current
    [70,
     # tPAC
     15,
     # tPACPrime, same as tPAC just sheet 2
     15,
     # qPAC
     0,
     # lambda evnt
     723,
     # lambda evntPAC
     1165]
)
kin6p2DUM_left2 = '8.48'
kin6p2DUM_left2_Values = (
    # current
    [40,
     # tPAC
     1.5,
     # tPACPrime, same as tPAC just sheet 2
     1.5,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)

##########################################
#############8.2 GeV######################
##########################################
kin8p2_setting1 = 'Q2=4.4|W=2.74|x=0.40'
kin8p2_center1 = '10.00'
kin8p2_center1_Values = (
    # current
    [70,
     # tPAC
     16.3,
     # tPACPrime, same as tPAC just sheet 2
     16.3,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     2500]
)
kin8p2DUM_center1 = '10.00'
kin8p2DUM_center1_Values = (
    # current
    [40,
     # tPAC
     1.1,
     # tPACPrime, same as tPAC just sheet 2
     1.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)
kin8p2_left1 = '13.00'
kin8p2_left1_Values = (
    # current
    [70,
     # tPAC
     16.3,
     # tPACPrime, same as tPAC just sheet 2
     16.3,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     2250]
)
kin8p2DUM_left1 = '13.00'
kin8p2DUM_left1_Values = (
    # current
    [40,
     # tPAC
     1.1,
     # tPACPrime, same as tPAC just sheet 2
     1.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)

##########################################
kin8p2_setting2 = 'Q2=3.0|W=3.14|x=0.25'
kin8p2_center2 = '6.89'
kin8p2_center2_Values = (
    # current
    [70,
     # tPAC
     44.2,
     # tPACPrime, same as tPAC just sheet 2
     44.2,
     # qPAC
     0,

     # lambda evnt
     0,
     # lambda evntPAC
     9000]
)
kin8p2DUM_center2 = '6.89'
kin8p2DUM_center2_Values = (
    # current
    [40,
     # tPAC
     3.1,
     # tPACPrime, same as tPAC just sheet 2
     3.1,
     # qPAC
     0,

     # lambda evnt
     0,
     # lambda evntPAC
     0]
)
kin8p2_left2 = '9.89'
kin8p2_left2_Values = (
    # current
    [70,
     # tPAC
     44.2,
     # tPACPrime, same as tPAC just sheet 2
     44.2,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     6650]
)
kin8p2DUM_left2 = '9.89'
kin8p2DUM_left2_Values = (
    # current
    [40,
     # tPAC
     3.1,
     # tPACPrime, same as tPAC just sheet 2
     3.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)

##########################################
kin8p2_setting3 = 'Q2=5.5|W=3.02|x=0.40'
kin8p2_center3 = '5.90'
kin8p2_center3_Values = (
    # current
    [70,
     # tPAC
     44.1,
     # tPACPrime, same as tPAC just sheet 2
     44.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     580]
)
kin8p2DUM_center3 = '5.90'
kin8p2DUM_center3_Values = (
    # current
    [40,
     # tPAC
     3.1,
     # tPACPrime, same as tPAC just sheet 2
     3.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)
kin8p2_left3 = '8.48'
kin8p2_left3_Values = (
    # current
    [70,
     # tPAC
     44.1,
     # tPACPrime, same as tPAC just sheet 2
     44.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     580]
)
kin8p2DUM_left3 = '8.48'
kin8p2DUM_left3_Values = (
    # current
    [40,
     # tPAC
     3.1,
     # tPACPrime, same as tPAC just sheet 2
     3.1,
     # qPAC
     0,
     # lambda evnt
     0,
     # lambda evntPAC
     0]
)

wb = xlsxwriter.Workbook('test.xls')

# Add first sheet in spreadsheet
s1 = wb.add_worksheet('6.2 GeV Summary')

# Specify formatting
bold = wb.add_format({'bold': True})

# Set row and column size
s1.set_default_row(30)
s1.set_column(0,14,15)

# Merging first row to fit title
s1.merge_range('A1:M1','6.2 GeV KAON-LT Physics Setting',bold)

# write(column[row],'Name of cell',formatting)
s1.write('A2', 'Setting',bold)
s1.write('B2', 'BCM4A \nCharge (mC)',bold)
s1.write('C2', 't_run (sec)',bold)
s1.write('D2', 't_setting (sec)',bold)
s1.write('E2', 't_PAC \n(hr @ 100% eff)',bold)
s1.write('F2', 't_setting/t_PAC',bold)
s1.write('G2', 'Q_PAC',bold)
s1.write('H2', 'Q_actual (mC)',bold)
s1.write('I2', 'Q_actual/Q_PAC',bold)
s1.write('J2', 'Effective \nEfficiency (J/H)',bold)
# Delta: u'\u0394' (UTF-8)
s1.write('K2', 'K+%s \nrun plan events' % (u'\u0394'),bold)
s1.write('L2', 'K+%s \nactual events' % (u'\u0394'),bold)
s1.write('M2', 'K+%s \nactual/proposed' % (u'\u0394'),bold)
s1.write('N2', 'K+%s \nY_obs/Y_expect' % (u'\u0394'),bold)

# Add first sheet in spreadsheet
s2 = wb.add_worksheet('6.2 Gev|%s' % kin6p2_setting1)

# Set row and column size
s2.set_default_row(30)
s2.set_column(0,14,15)

# Merging first row to fit title
s2.merge_range('A1:M1','6.2 GeV KAON-LT Physics Setting',bold)

s2.write('A2', 'SHMS Angle',bold)
s2.write('B2', 'Run Number',bold)
s2.write('C2', 'BCM4A \nCharge (mC)',bold)
s2.write('D2', 't_run (sec)',bold)
s2.write('E2', 'Current (uA)',bold)
s2.write('F2', 't_setting (sec)',bold)
s2.write('G2', 't_PAC \n(hr @ 100% eff)',bold)
s2.write('H2', 't_setting/t_PAC',bold)
s2.write('I2', 'Q_PAC',bold)
s2.write('J2', 'Q_actual/Q_PAC',bold)
s2.write('K2', 'Effective \nEfficiency (J/H)',bold)

###############################################################################
# 6.2 GeV, Setting 1 ##########################################################
###############################################################################

s1.merge_range('A3:B3','%s' % kin6p2_setting1 ,bold)
s2.merge_range('A3:B3','%s' % kin6p2_setting1 ,bold)

l1 = 0
l2 = 0
curNum = 5
newData = ()

current = kin6p2_center1_Values[0]
tPAC= kin6p2_center1_Values[1]
tPACPrime = kin6p2_center1_Values[2]
qPAC = kin6p2_center1_Values[3]
evnt= kin6p2_center1_Values[4]
evntPAC = kin6p2_center1_Values[5]

s1.write('A4', '%s deg LH2' % kin6p2_center1)
s2.write('A4', '%s deg LH2' % kin6p2_center1)

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7871, 241.648],
    [7872, 234.072],
    [7873, 222.282],
    [7874, 276.079],
    [7875, 221.651],
    [7876, 231.678],
    [7877, 222.27],
)
tmpCurr = [current]
for value in (tmpCurr):
    s2.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2.write(row,col, runNum)
        s2.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2.write('B%s' % (end), 'Total',bold)
    s2.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2.write('E%s' % (end), current,bold)
    s2.write('G%s' % (end), tPAC,bold)
    s2.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 5+l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting1,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting1,end))
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write_formula('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting1,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin6p2DUM_left1_Values[0]
tPAC= kin6p2DUM_left1_Values[1]
tPACPrime = kin6p2DUM_left1_Values[2]
qPAC = kin6p2DUM_left1_Values[3]
evnt= kin6p2DUM_left1_Values[4]
evntPAC = kin6p2DUM_left1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7878, 10.921],
    [7879, 31.699],
    [7880, 31.699],
)
tmpCurr = [current]
for value in (tmpCurr):
    s2.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2.write(row,col, runNum)
        s2.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2.write('B%s' % (end), 'Total',bold)
    s2.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2.write('E%s' % (end), current,bold)
    s2.write('G%s' % (end), tPAC,bold)
    s2.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting1,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting1,end))
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting1,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################
# Next angle #############
##########################

curNum =1

current = kin6p2_left1_Values[0]
tPAC= kin6p2_left1_Values[1]
tPACPrime = kin6p2_left1_Values[2]
qPAC = kin6p2_left1_Values[3]
evnt= kin6p2_left1_Values[4]
evntPAC = kin6p2_left1_Values[5]

s1.write('A%s' % (l1), '%s deg LH2' % kin6p2_left1)
s2.write('A%s' % (l2), '%s deg LH2' % kin6p2_left1)


print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7882,209.19],
    [7883,257.17],
    [7884,243.51],
    [7885,267.2],
    [7886,266.44],
    [7887,301.65],
)
tmpCurr = [current]
for value in (tmpCurr):
    s2.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2.write(row,col, runNum)
        s2.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2.write('B%s' % (end), 'Total',bold)
    s2.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2.write('E%s' % (end), current,bold)
    s2.write('G%s' % (end), tPAC,bold)
    s2.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 1+l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting1,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting1,end))
    # s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,curNum+1)) Need work
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    # s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,curNum+1))
    s1.write('L%s' % (curNum), evnt)
    # s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,curNum+1))
    curNum += 1
endCur =  curNum
l1 = endCur+1
s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting1,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin6p2DUM_center1_Values[0]
tPAC= kin6p2DUM_center1_Values[1]
tPACPrime = kin6p2DUM_center1_Values[2]
qPAC = kin6p2DUM_center1_Values[3]
evnt= kin6p2DUM_center1_Values[4]
evntPAC = kin6p2DUM_center1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7881,55.62],
    [7888,71.48],
)
tmpCurr = [current]
for value in (tmpCurr):
    s2.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2.write(row,col, runNum)
        s2.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2.write('B%s' % (end), 'Total',bold)
    s2.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2.write('E%s' % (end), current,bold)
    s2.write('G%s' % (end), tPAC,bold)
    s2.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting1,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting1,end))
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting1,end))
    s1.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting1,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################

###############################################################################
# 6.2 GeV, Setting 2 ##########################################################
###############################################################################

s2a = wb.add_worksheet('6.2 Gev|%s' % kin6p2_setting2)

# Set row and column size
s2a.set_default_row(30)
s2a.set_column(0,14,15)

# Merging first row to fit title
s2a.merge_range('A1:M1','6.2 GeV KAON-LT Physics Setting',bold)

s2a.write('A2', 'SHMS Angle',bold)
s2a.write('B2', 'Run Number',bold)
s2a.write('C2', 'BCM4A \nCharge (mC)',bold)
s2a.write('D2', 't_run (sec)',bold)
s2a.write('E2', 'Current (uA)',bold)
s2a.write('F2', 't_setting (sec)',bold)
s2a.write('G2', 't_PAC \n(hr @ 100% eff)',bold)
s2a.write('H2', 't_setting/t_PAC',bold)
s2a.write('I2', 'Q_PAC',bold)
s2a.write('J2', 'Q_actual/Q_PAC',bold)
s2a.write('K2', 'Effective \nEfficiency (J/H)',bold)


l2=3
 
s1.merge_range('A%s:B%s' % (l1,l1),'%s' % kin6p2_setting2 ,bold)
s2a.merge_range('A%s:B%s' % (l2,l2),'%s' % kin6p2_setting2 ,bold)

curNum = 2
newData = ()

current = kin6p2_center2_Values[0]
tPAC= kin6p2_center2_Values[1]
tPACPrime = kin6p2_center2_Values[2]
qPAC = kin6p2_center2_Values[3]
evnt= kin6p2_center2_Values[4]
evntPAC = kin6p2_center2_Values[5]

s1.write('A%s' % (l1+1), '%s deg LH2' % kin6p2_center2)
s2a.write('A%s' % (l2+1), '%s deg LH2' % kin6p2_center2)

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7891,252.502],
    [7891,232.9],
    [7892,226.93],
    [7893,195.38],
    [7894,214.42],
    [7895,362.67],
    [7896,234.96],
    [7899,260.56],
    [7900,242.66],
    [7901,240.04],
    [7902,239.04],
    [7903,253.33],
    [7904,181.34],
    [7905,238.33],
    [7906,219.53],
    [7907,219.53],
    [7908,141.28],
)
tmpCurr = [current]
for value in (tmpCurr):
    s2a.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2a.write(row,col, runNum)
        s2a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2a.write('B%s' % (end), 'Total',bold)
    s2a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2a.write('E%s' % (end), current,bold)
    s2a.write('G%s' % (end), tPAC,bold)
    s2a.write_formula('I%s' % (end),'=G%s*3600*0.000055*1000' % (end) ,bold)
    s2a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 2+l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting2,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting2,end))
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting2,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin6p2DUM_left1_Values[0]
tPAC= kin6p2DUM_left1_Values[1]
tPACPrime = kin6p2DUM_left1_Values[2]
qPAC = kin6p2DUM_left1_Values[3]
evnt= kin6p2DUM_left1_Values[4]
evntPAC = kin6p2DUM_left1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7897,41.31],
    [7898,87.38],
)
tmpCurr = [current]
for value in (tmpCurr):
    s2a.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2a.write(row,col, runNum)
        s2a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2a.write('B%s' % (end), 'Total',bold)
    s2a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2a.write('E%s' % (end), current,bold)
    s2a.write('G%s' % (end), tPAC,bold)
    s2a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting2,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting2,end))
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting2,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################
# Next angle #############
##########################

curNum =1
current = kin6p2_left2_Values[0]
tPAC= kin6p2_left2_Values[1]
tPACPrime = kin6p2_left2_Values[2]
qPAC = kin6p2_left2_Values[3]
evnt= kin6p2_left2_Values[4]
evntPAC = kin6p2_left2_Values[5]

s1.write('A%s' % (l1), '%s deg LH2' % kin6p2_left2)
s2a.write('A%s' % (l2), '%s deg LH2' % kin6p2_left2)


print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7909, 131.014],
    [7910, 55.047],
    [7911, 77.354],
    [7912, 28.683],
    [7913, 76.601],
    [7914, 117.79],
    [7915, 118.783],
    [7916, 135.726],
    [7917, 146.517],
    [7918, 27.966],
    [7919, 142.475],
    [7920, 116.507],
    [7921, 182.834],
    [7925, 170.95],
    [7926, 183.094],
    [7927, 143.944],
    [7928, 72.459],
    [7930, 13.966],
    [7931, 175.929],
    [7932, 171.455],
    [7933, 168.158],
    [7934, 176.0],
    [7935, 158.969],
    [7936, 151.628],
    [7937, 164.136],
    [7938, 143.332],

)
tmpCurr = [current]
for value in (tmpCurr):
    s2a.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2a.write(row,col, runNum)
        s2a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2a.write('B%s' % (end), 'Total',bold)
    s2a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2a.write('E%s' % (end), current,bold)
    s2a.write('G%s' % (end), tPAC,bold)
    s2a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 1+l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting2,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting2,end))
    # s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,curNum+1)) Need work
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    # s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,curNum+1))
    s1.write('L%s' % (curNum), evnt)
    # s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,curNum+1))
    curNum += 1
endCur =  curNum
l1 = endCur+1
s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting2,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin6p2DUM_center1_Values[0]
tPAC= kin6p2DUM_center1_Values[1]
tPACPrime = kin6p2DUM_center1_Values[2]
qPAC = kin6p2DUM_center1_Values[3]
evnt= kin6p2DUM_center1_Values[4]
evntPAC = kin6p2DUM_center1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [7922, 23.781],
    [7923, 198.331],
    [7924, 100.607],
    
)
tmpCurr = [current]
for value in (tmpCurr):
    s2a.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2a.write(row,col, runNum)
        s2a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2a.write('B%s' % (end), 'Total',bold)
    s2a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s2a.write('E%s' % (end), current,bold)
    s2a.write('G%s' % (end), tPAC,bold)
    s2a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s1.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s1.write_formula('B%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write_formula('C%s' % (curNum), '=\'6.2 Gev|%s\'!D%s' % (kin6p2_setting2,end))
    s1.write_formula('D%s' % (curNum), '=\'6.2 Gev|%s\'!F%s' % (kin6p2_setting2,end))
    s1.write_formula('H%s' % (curNum), '=\'6.2 Gev|%s\'!C%s' % (kin6p2_setting2,end))
    s1.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s1.write('B%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), '=\'6.2 Gev|%s\'!I%s' % (kin6p2_setting2,end),bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s1.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################

################################################################################################################################################################################################################################################################################################

# Add first sheet in spreadsheet
s3 = wb.add_worksheet('8.2 GeV Summary')

# Specify formatting
bold = wb.add_format({'bold': True})

# Set row and column size
s3.set_default_row(30)
s3.set_column(0,14,15)

# Merging first row to fit title
s3.merge_range('A1:M1','8.2 GeV KAON-LT Physics Setting',bold)

# write(column[row],'Name of cell',formatting)
s3.write('A2', 'Setting',bold)
s3.write('B2', 'BCM4A \nCharge (mC)',bold)
s3.write('C2', 't_run (sec)',bold)
s3.write('D2', 't_setting (sec)',bold)
s3.write('E2', 't_PAC \n(hr @ 100% eff)',bold)
s3.write('F2', 't_setting/t_PAC',bold)
s3.write('G2', 'Q_PAC',bold)
s3.write('H2', 'Q_actual (mC)',bold)
s3.write('I2', 'Q_actual/Q_PAC',bold)
s3.write('J2', 'Effective \nEfficiency (J/H)',bold)
# Delta: u'\u0394' (UTF-8)
s3.write('K2', 'K+%s \nrun plan events' % (u'\u0394'),bold)
s3.write('L2', 'K+%s \nactual events' % (u'\u0394'),bold)
s3.write('M2', 'K+%s \nactual/proposed' % (u'\u0394'),bold)
s3.write('N2', 'K+%s \nY_obs/Y_expect' % (u'\u0394'),bold)

# Add first sheet in spreadsheet
s4 = wb.add_worksheet('8.2 Gev|%s' % kin8p2_setting1)

# Set row and column size
s4.set_default_row(30)
s4.set_column(0,14,15)

# Merging first row to fit title
s4.merge_range('A1:M1','8.2 GeV KAON-LT Physics Setting',bold)

s4.write('A2', 'SHMS Angle',bold)
s4.write('B2', 'Run Number',bold)
s4.write('C2', 'BCM4A \nCharge (mC)',bold)
s4.write('D2', 't_run (sec)',bold)
s4.write('E2', 'Current (uA)',bold)
s4.write('F2', 't_setting (sec)',bold)
s4.write('G2', 't_PAC \n(hr @ 100% eff)',bold)
s4.write('H2', 't_setting/t_PAC',bold)
s4.write('I2', 'Q_PAC',bold)
s4.write('J2', 'Q_actual/Q_PAC',bold)
s4.write('K2', 'Effective \nEfficiency (J/H)',bold)

###############################################################################
# 8.2 GeV, Setting 1 ##########################################################
###############################################################################

s3.merge_range('A3:B3','%s' % kin8p2_setting1 ,bold)
s4.merge_range('A3:B3','%s' % kin8p2_setting1 ,bold)

l1 = 0
l2 = 0
curNum = 5
newData = ()

current = kin8p2_center1_Values[0]
tPAC= kin8p2_center1_Values[1]
tPACPrime = kin8p2_center1_Values[2]
qPAC = kin8p2_center1_Values[3]
evnt= kin8p2_center1_Values[4]
evntPAC = kin8p2_center1_Values[5]

s3.write('A4', '%s deg LH2' % kin8p2_center1)
s4.write('A4', '%s deg LH2' % kin8p2_center1)

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4.write(row,col, runNum)
        s4.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4.write('B%s' % (end), 'Total',bold)
    s4.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4.write('E%s' % (end), current,bold)
    s4.write('G%s' % (end), tPAC,bold)
    s4.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 5+l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting1,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting1,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting1,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin8p2DUM_left1_Values[0]
tPAC= kin8p2DUM_left1_Values[1]
tPACPrime = kin8p2DUM_left1_Values[2]
qPAC = kin8p2DUM_left1_Values[3]
evnt= kin8p2DUM_left1_Values[4]
evntPAC = kin8p2DUM_left1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4.write(row,col, runNum)
        s4.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4.write('B%s' % (end), 'Total',bold)
    s4.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4.write('E%s' % (end), current,bold)
    s4.write('G%s' % (end), tPAC,bold)
    s4.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting1,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting1,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting1,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################
# Next angle #############
##########################

curNum =1
current = kin8p2_left1_Values[0]
tPAC= kin8p2_left1_Values[1]
tPACPrime = kin8p2_left1_Values[2]
qPAC = kin8p2_left1_Values[3]
evnt= kin8p2_left1_Values[4]
evntPAC = kin8p2_left1_Values[5]

s3.write('A%s' % (l1), '%s deg LH2' % kin8p2_left1)
s4.write('A%s' % (l2), '%s deg LH2' % kin8p2_left1)


print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4.write(row,col, runNum)
        s4.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4.write('B%s' % (end), 'Total',bold)
    s4.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4.write('E%s' % (end), current,bold)
    s4.write('G%s' % (end), tPAC,bold)
    s4.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 1+l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting1,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting1,end))
    # s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,curNum+1)) Need work
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    # s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,curNum+1))
    s3.write('L%s' % (curNum), evnt)
    # s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,curNum+1))
    curNum += 1
endCur =  curNum
l1 = endCur+1
s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting1,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin8p2DUM_center1_Values[0]
tPAC= kin8p2DUM_center1_Values[1]
tPACPrime = kin8p2DUM_center1_Values[2]
qPAC = kin8p2DUM_center1_Values[3]
evnt= kin8p2DUM_center1_Values[4]
evntPAC = kin8p2DUM_center1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4.write(row,col, runNum)
        s4.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4.write('B%s' % (end), 'Total',bold)
    s4.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4.write('E%s' % (end), current,bold)
    s4.write('G%s' % (end), tPAC,bold)
    s4.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting1,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting1,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting1,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting1,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################

###############################################################################
# 8.2 GeV, Setting 2 ##########################################################
###############################################################################

s4a = wb.add_worksheet('8.2 Gev|%s' % kin8p2_setting2)

# Set row and column size
s4a.set_default_row(30)
s4a.set_column(0,14,15)

# Merging first row to fit title
s4a.merge_range('A1:M1','8.2 GeV KAON-LT Physics Setting',bold)

s4a.write('A2', 'SHMS Angle',bold)
s4a.write('B2', 'Run Number',bold)
s4a.write('C2', 'BCM4A \nCharge (mC)',bold)
s4a.write('D2', 't_run (sec)',bold)
s4a.write('E2', 'Current (uA)',bold)
s4a.write('F2', 't_setting (sec)',bold)
s4a.write('G2', 't_PAC \n(hr @ 100% eff)',bold)
s4a.write('H2', 't_setting/t_PAC',bold)
s4a.write('I2', 'Q_PAC',bold)
s4a.write('J2', 'Q_actual/Q_PAC',bold)
s4a.write('K2', 'Effective \nEfficiency (J/H)',bold)

l2=3

s3.merge_range('A%s:B%s' % (l1,l1),'%s' % kin8p2_setting2 ,bold)
s4a.merge_range('A%s:B%s' % (l2,l2),'%s' % kin8p2_setting2 ,bold)

curNum = 2
newData = ()

current = kin8p2_center2_Values[0]
tPAC= kin8p2_center2_Values[1]
tPACPrime = kin8p2_center2_Values[2]
qPAC = kin8p2_center2_Values[3]
evnt= kin8p2_center2_Values[4]
evntPAC = kin8p2_center2_Values[5]

s3.write('A%s' % (l1+1), '%s deg LH2' % kin8p2_center2)
s4a.write('A%s' % (l2+1), '%s deg LH2' % kin8p2_center2)

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4a.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4a.write(row,col, runNum)
        s4a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4a.write('B%s' % (end), 'Total',bold)
    s4a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4a.write('E%s' % (end), current,bold)
    s4a.write('G%s' % (end), tPAC,bold)
    s4a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 2+l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting2,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting2,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting2,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin8p2DUM_left1_Values[0]
tPAC= kin8p2DUM_left1_Values[1]
tPACPrime = kin8p2DUM_left1_Values[2]
qPAC = kin8p2DUM_left1_Values[3]
evnt= kin8p2DUM_left1_Values[4]
evntPAC = kin8p2DUM_left1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4a.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4a.write(row,col, runNum)
        s4a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4a.write('B%s' % (end), 'Total',bold)
    s4a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4a.write('E%s' % (end), current,bold)
    s4a.write('G%s' % (end), tPAC,bold)
    s4a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting2,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting2,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting2,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################
# Next angle #############
##########################

curNum =1
current = kin8p2_left2_Values[0]
tPAC= kin8p2_left2_Values[1]
tPACPrime = kin8p2_left2_Values[2]
qPAC = kin8p2_left2_Values[3]
evnt= kin8p2_left2_Values[4]
evntPAC = kin8p2_left2_Values[5]

s3.write('A%s' % (l1), '%s deg LH2' % kin8p2_left2)
s4a.write('A%s' % (l2), '%s deg LH2' % kin8p2_left2)


print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4a.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4a.write(row,col, runNum)
        s4a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4a.write('B%s' % (end), 'Total',bold)
    s4a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4a.write('E%s' % (end), current,bold)
    s4a.write('G%s' % (end), tPAC,bold)
    s4a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 1+l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting2,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting2,end))
    # s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,curNum+1)) Need work
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    # s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,curNum+1))
    s3.write('L%s' % (curNum), evnt)
    # s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,curNum+1))
    curNum += 1
endCur =  curNum
l1 = endCur+1
s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting2,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin8p2DUM_center1_Values[0]
tPAC= kin8p2DUM_center1_Values[1]
tPACPrime = kin8p2DUM_center1_Values[2]
qPAC = kin8p2DUM_center1_Values[3]
evnt= kin8p2DUM_center1_Values[4]
evntPAC = kin8p2DUM_center1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4a.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4a.write(row,col, runNum)
        s4a.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4a.write('B%s' % (end), 'Total',bold)
    s4a.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4a.write('E%s' % (end), current,bold)
    s4a.write('G%s' % (end), tPAC,bold)
    s4a.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4a.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting2,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting2,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting2,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting2,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################

###############################################################################
# 8.2 GeV, Setting 3 ##########################################################
###############################################################################

s4b = wb.add_worksheet('8.2 Gev|%s' % kin8p2_setting3)

# Set row and column size
s4b.set_default_row(30)
s4b.set_column(0,14,15)

# Merging first row to fit title
s4b.merge_range('A1:M1','8.2 GeV KAON-LT Physics Setting',bold)

s4b.write('A2', 'SHMS Angle',bold)
s4b.write('B2', 'Run Number',bold)
s4b.write('C2', 'BCM4A \nCharge (mC)',bold)
s4b.write('D2', 't_run (sec)',bold)
s4b.write('E2', 'Current (uA)',bold)
s4b.write('F2', 't_setting (sec)',bold)
s4b.write('G2', 't_PAC \n(hr @ 100% eff)',bold)
s4b.write('H2', 't_setting/t_PAC',bold)
s4b.write('I2', 'Q_PAC',bold)
s4b.write('J2', 'Q_actual/Q_PAC',bold)
s4b.write('K2', 'Effective \nEfficiency (J/H)',bold)

l2=3

s3.merge_range('A%s:B%s' % (l1,l1),'%s' % kin8p2_setting3 ,bold)
s4b.merge_range('A%s:B%s' % (l2,l2),'%s' % kin8p2_setting3 ,bold)

curNum = 2
newData = ()

current = kin8p2_center3_Values[0]
tPAC= kin8p2_center3_Values[1]
tPACPrime = kin8p2_center3_Values[2]
qPAC = kin8p2_center3_Values[3]
evnt= kin8p2_center3_Values[4]
evntPAC = kin8p2_center3_Values[5]

s3.write('A%s' % (l1+1), '%s deg LH2' % kin8p2_center3)
s4b.write('A%s' % (l2+1), '%s deg LH2' % kin8p2_center3)

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4b.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4b.write(row,col, runNum)
        s4b.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4b.write('B%s' % (end), 'Total',bold)
    s4b.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4b.write('E%s' % (end), current,bold)
    s4b.write('G%s' % (end), tPAC,bold)
    s4b.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4b.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 2+l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting3,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting3,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting3,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin8p2DUM_left1_Values[0]
tPAC= kin8p2DUM_left1_Values[1]
tPACPrime = kin8p2DUM_left1_Values[2]
qPAC = kin8p2DUM_left1_Values[3]
evnt= kin8p2DUM_left1_Values[4]
evntPAC = kin8p2DUM_left1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4b.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4b.write(row,col, runNum)
        s4b.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4b.write('B%s' % (end), 'Total',bold)
    s4b.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4b.write('E%s' % (end), current,bold)
    s4b.write('G%s' % (end), tPAC,bold)
    s4b.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4b.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting3,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting3,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting3,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################
# Next angle #############
##########################

curNum =1
current = kin8p2_left3_Values[0]
tPAC= kin8p2_left3_Values[1]
tPACPrime = kin8p2_left3_Values[2]
qPAC = kin8p2_left3_Values[3]
evnt= kin8p2_left3_Values[4]
evntPAC = kin8p2_left3_Values[5]

s3.write('A%s' % (l1), '%s deg LH2' % kin8p2_left3)
s4b.write('A%s' % (l2), '%s deg LH2' % kin8p2_left3)


print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4b.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4b.write(row,col, runNum)
        s4b.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4b.write('B%s' % (end), 'Total',bold)
    s4b.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4b.write('E%s' % (end), current,bold)
    s4b.write('G%s' % (end), tPAC,bold)
    s4b.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4b.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 1+l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), '@ %suA (mC)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting3,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting3,end))
    # s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,curNum+1)) Need work
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    # s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,curNum+1))
    s3.write('L%s' % (curNum), evnt)
    # s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,curNum+1))
    curNum += 1
endCur =  curNum
l1 = endCur+1
s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting3,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

######################################################################################################

curNum =0

current = kin8p2DUM_center1_Values[0]
tPAC= kin8p2DUM_center1_Values[1]
tPACPrime = kin8p2DUM_center1_Values[2]
qPAC = kin8p2DUM_center1_Values[3]
evnt= kin8p2DUM_center1_Values[4]
evntPAC = kin8p2DUM_center1_Values[5]

print("Looking at current %s uA" % (current))
# [RunNum,charge]
newData = (
    [0,0],
)
tmpCurr = [current]
for value in (tmpCurr):
    s4b.write('A%s' % (curNum+l2), 'DUMMY (%suA)' % (value))
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s4b.write(row,col, runNum)
        s4b.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s4b.write('B%s' % (end), 'Total',bold)
    s4b.write_formula('C%s' % (end), '=SUM(C%s:C%s)' % (curNum+l2,end-1) ,bold)
    s4b.write('E%s' % (end), current,bold)
    s4b.write('G%s' % (end), tPAC,bold)
    s4b.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s4b.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    print("%s" % curNum)
    s3.write('A%s' % (curNum), 'DUMMY (%suA)' % (value))
    s3.write_formula('B%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write_formula('C%s' % (curNum), '=\'8.2 Gev|%s\'!D%s' % (kin8p2_setting3,end))
    s3.write_formula('D%s' % (curNum), '=\'8.2 Gev|%s\'!F%s' % (kin8p2_setting3,end))
    s3.write_formula('H%s' % (curNum), '=\'8.2 Gev|%s\'!C%s' % (kin8p2_setting3,end))
    s3.write('L%s' % (curNum), evnt)
    curNum += 1
endCur =  curNum
l1 = endCur+1

s3.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum-1,endCur-1))
s3.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,qPAC))
s3.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,evntPAC))

s3.write('B%s' % (endCur), 'Total',bold)
s3.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (curNum-1,endCur-1),bold)
s3.write('E%s' % (endCur), tPACPrime,bold)
s3.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s3.write('G%s' % (endCur), '=\'8.2 Gev|%s\'!I%s' % (kin8p2_setting3,end),bold)
s3.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s3.write('K%s' % (endCur), evntPAC,bold)
s3.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (curNum-1,endCur-1),bold)
s3.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)
s3.write_formula('N%s' % (endCur), '=M%s/I%s' % (endCur,endCur),bold)

####################################################################################################

wb.close()
