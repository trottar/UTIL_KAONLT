#!/usr/bin/env python
#-*- coding: utf-8 -*-

import xlsxwriter

from PIL import ImageFont

wb = xlsxwriter.Workbook('test.ods')

# Add first sheet in spreadsheet
s1 = wb.add_worksheet('8.2 GeV Summary')

# Specify formatting
bold = wb.add_format({'bold': True})

# Set row and column size
s1.set_default_row(30)
s1.set_column(0,14,15)

# Merging first row to fit title
s1.merge_range('A1:M1','8.2 GeV KAON-LT Physics Setting',bold)

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

s1.write('A3', 'Q=4.4 W=2.40',bold)

s1.write('A4', '7.00deg LH2')

# Add first sheet in spreadsheet
s2 = wb.add_worksheet('4p4_8p2')

# Set row and column size
s2.set_default_row(30)
s2.set_column(0,14,15)

# Merging first row to fit title
s2.merge_range('A1:M1','8.2 GeV KAON-LT Physics Setting',bold)

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

s2.write('A3', 'Q=4.4 W=2.40',bold)

s2.write('A4', '7.00deg LH2')

l1 = 0
l2 = 0
newData = ()

current = 70
tPAC=40
tPACPrime = 5600
qPAC = 400
evnt=200
curNum = 5
evntPAC = 8000

print("Looking at current %s uA" % (current))
newData = (
    [6158,46],
    [6159,47],
    [6160,48],    
)
tmpCurr = [current]
for value in (tmpCurr):
    s2.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value),bold)
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2.write(row,col, runNum)
        s2.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2.write('A%s' % (end), 'Total',bold)
    s2.write_formula('C%s' % (end), '=SUM(C7:C%s)' % (end-1) ,bold)
    s2.write('E%s' % (end), current,bold)
    s2.write('G%s' % (end), tPAC,bold)
    s2.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = 5+l1
    s1.write('A%s' % (curNum), '@ %suA (mC)' % (value),bold)
    s1.write_formula('B%s' % (curNum), '=\'4p4_8p2\'!C%s' % (end))
    s1.write_formula('C%s' % (curNum), '=\'4p4_8p2\'!D%s' % (end))
    s1.write_formula('D%s' % (curNum), '=\'4p4_8p2\'!F%s' % (end))
    # s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,endCur)) Need work
    s1.write_formula('H%s' % (curNum), '=\'4p4_8p2\'!C%s' % (end))
    # s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,endCur))
    s1.write('L%s' % (curNum), evnt)
    # s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,endCur))
    s1.write_formula('N%s' % (curNum), '=M%s/I%s' % (curNum,curNum))
    curNum += 1
endCur =  curNum
l1 = endCur+1

s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,endCur))
s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,endCur))
s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,endCur))

s1.write('A%s' % (endCur), 'Total',bold)
s1.write('A%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (end,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), qPAC,bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (end,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (end,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)

current = 30
tPAC=40
tPACPrime = 5600
qPAC = 400
evnt=200
curNum = 0
evntPAC = 8000

print("Looking at current %s uA" % (current))
newData = (
    [6158,46],
    [6159,47],
    [6160,48],    
)
tmpCurr = [current]
for value in (tmpCurr):
    s2.write('A%s' % (curNum+l2), '@ %suA (mC)' % (value),bold)
    # Starts at 0 for rows and columns
    row = l2+curNum-1
    col = 1
    for runNum, BCM4A in (newData):
        s2.write(row,col, runNum)
        s2.write(row,col+1, BCM4A)
        row += 1
    end = row+1
    # Going back to sheet one so we can 'link' second sheet values
    s2.write('A%s' % (end), 'Total',bold)
    s2.write_formula('C%s' % (end), '=SUM(C7:C%s)' % (end-1) ,bold)
    s2.write('E%s' % (end), current,bold)
    s2.write('G%s' % (end), tPAC,bold)
    s2.write_formula('I%s' % (end),'=G%s*3600*0.000070*1000' % (end) ,bold)
    s2.write_formula('J%s' % (end), '=C%s/I%s' % (end,end),bold)
    l2 = end+1
    curNum = l1
    s1.write('A%s' % (curNum), '@ %suA (mC)' % (value),bold)
    s1.write_formula('B%s' % (curNum), '=\'4p4_8p2\'!C%s' % (end))
    s1.write_formula('C%s' % (curNum), '=\'4p4_8p2\'!D%s' % (end))
    s1.write_formula('D%s' % (curNum), '=\'4p4_8p2\'!F%s' % (end))
    # s1.write_formula('F%s' % (curNum), '=D%s/3600/E%s' % (curNum,curNum+1)) Need work
    s1.write_formula('H%s' % (curNum), '=\'4p4_8p2\'!C%s' % (end))
    # s1.write_formula('I%s' % (curNum), '=B%s/G%s' % (curNum,curNum+1))
    s1.write('L%s' % (curNum), evnt)
    # s1.write_formula('M%s' % (curNum), '=L%s/K%s' % (curNum,curNum+1))
    s1.write_formula('N%s' % (curNum), '=M%s/I%s' % (curNum,curNum))
    curNum += 1
endCur =  curNum
l1 = endCur+1
s1.write('A%s' % (endCur), 'Total',bold)
s1.write('A%s' % (endCur), 'Total',bold)
s1.write_formula('D%s' % (endCur), '=SUM(D%s:D%s)' % (end,endCur-1),bold)
s1.write('E%s' % (endCur), tPACPrime,bold)
s1.write_formula('F%s' % (endCur), 'D%s/3600/E%s' % (endCur,endCur),bold)
s1.write('G%s' % (endCur), qPAC,bold)
s1.write_formula('H%s' % (endCur), '=SUM(H%s:H%s)' % (end,endCur-1),bold)
s1.write_formula('I%s' % (endCur), '=H%s/G%s' % (endCur,endCur),bold)
s1.write('K%s' % (endCur), evntPAC,bold)
s1.write_formula('L%s' % (endCur), '=SUM(L%s:L%s)' % (end,endCur-1),bold)
s1.write_formula('M%s' % (endCur), '=L%s/K%s' % (endCur,endCur),bold)

wb.close()

