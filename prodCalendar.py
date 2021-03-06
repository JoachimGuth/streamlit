#pip install holidays

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import calendar
from datetime import datetime
from datetime import date
import holidays
import matplotlib.pyplot as plt
#%matplotlib inline

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

pd.set_option('display.max_rows', None)


# General - Common Data


machines = ['M1', 'M2', 'M3','M4', 'M5', 'M6', 'M7', 'M8']

machineOutputKgHour = {'M1': 15, 'M2': 25, 'M3': 30, 'M4': 30, 'M5': 35, 'M6': 40, 'M7': 55, 'M8': 80}

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

monthsDict = {'Jan': 1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10,'Nov':11, 'Dec':12}
monthsNameList = [n for n in monthsDict]
monthsNbrList = [ n for  n in monthsDict.values()]


shiftTypesDict = {'0x0': 0, '2x8': 16, '3x8': 24, '2x12': 24}
shiftTypesNameList = [s for s in shiftTypesDict]
shiftTypesHoursList = [n for n in shiftTypesDict.values()]
defaultShiftType = '3x8'

shiftConfigDict = {'wk.5d': 0, 'wksat.6d': 1, 'wkend.7d': 2, 'phwk.5d': 3, 'ph.all':4}
shiftConfigNameList = [t for t in shiftConfigDict]
shiftConfigNbrList = [c for c in shiftConfigDict.values()]
defaultConfig = 'wk.d5'

dayTypesDict = {'Wk':0, 'Sat':1, 'Sun': 2, 'PH': 3, 'PHSat': 4, 'PHSun': 5}
dayTypesNameList = [t for t in dayTypesDict]
dayTypesNbrList = [c for c in dayTypesDict.values()]

yrList = [cy for cy in range(date.today().year,date.today().year+5)]
currentYear = date.today().year


# Function - Determine nbr of days of a month for a particulat year
def nbrOfMonthDays(year, month):
    leap = 0
    if year % 400 == 0:
        leap = 1
    elif year % 100 == 0:
        leap = 0
    elif year % 4 == 0:
        leap = 1
    if month == 2: #Feb
        return 28 + leap
    #list = ['Jan','Mar','May','Jul','Aug','Oct','Dec']
    list = [1, 3, 5, 7, 8 , 10, 12]
    if month in list:
        return 31
    return 30

def isPubHoliday(year, month, day, country):
    if country == 'Singapore':
        for d in holidays.Singapore(years=year).items():
            # print(d[0].day,d[0].month, day, month)
            if d[0].month == month and d[0].day == day:
                return('True')
            if d[0].month > month:
                break
    return('False')

def getWeekDay(year,month, day):
    wkday = date(year, month, day).weekday()
    return(weekdays[wkday])

def getDayType(year, month, day, country):
    weekday = getWeekDay(year, month, day)
    dayType = 'Wk'
    if  weekday in ['Saturday'] and isPubHoliday(year, month, day, country) == 'True':
        dayType = 'PHSat'
    elif weekday in ['Sunday'] and isPubHoliday(year, month, day, country) == 'True':
        dayType = 'PHSun'
    elif weekday in ['Saturday'] and isPubHoliday(year, month, day, country) == 'False':
        dayType = 'Sat'
    elif weekday in ['Sunday'] and isPubHoliday(year, month, day, country) == 'False':
        dayType = 'Sun'
    elif isPubHoliday(year, month, day, country) == 'True':
        dayType = 'PH'
    else: 
        dayType = 'Wk'
    return(dayType)

# Set 0r Change ShiftType and ShftHrs of the shiftCalDF. ShiftConfig remains unchanged
def setShiftType(shiftCalDF, months ,machines, shifttype):
    for x in shiftCalDF.index: 
        if shiftCalDF.loc[x, "Month"] in months:
            if shifttCalDF.loc[x, "Machine"] in machines:
                if shiftCaldf.loc[x, "ShftHrs"] != 0:
                    shiftCalDF.loc[x, "ShiftType"] = shifttype
                    shiftCalDF.loc[x, "ShftHrs"] = shiftTypesDict[shifttype]
            
# Set or change shift info for each day of a month for a given year ande a list of machines
def setShiftConfig (shiftCalDF, months, machines, shifttype, shiftconfig):
    for x in shiftCalDF.index: 
        if shiftCalDF.loc[x, "Month"] in months:
            if shiftCalDF.loc[x, "Machine"] in machines:
                if shiftconfig == "wk.5d": 
                    if shiftCalDF.loc[x, "DayType"] in ['Wk']:
                        shiftCalDF.loc[x, "ShiftType"] = shifttype
                        shiftCalDF.loc[x, "ShftHrs"] = shiftTypesDict[shifttype]
                        shiftCalDF.loc[x, "ShiftConfig"] = shiftconfig
                elif shiftconfig == "wksat.6d": 
                    if shiftCalDF.loc[x, "DayType"] in ['Wk', 'Sat']:
                        shiftCalDF.loc[x, "ShiftType"] = shifttype
                        shiftCalDF.loc[x, "ShftHrs"] = shiftTypesDict[shifttype]
                        shiftCalDF.loc[x, "ShiftConfig"] = shiftconfig
                elif shiftconfig == "wkend.7d": 
                    if shiftCalDF.loc[x, "DayType"] in ['Wk', 'Sat','Sun']:
                        shiftCalDF.loc[x, "ShiftType"] = shifttype
                        shiftCalDF.loc[x, "ShftHrs"] = shiftTypesDict[shifttype]
                        shiftCalDF.loc[x, "ShiftConfig"] = shiftconfig
                elif shiftconfig == "phwk.5d": 
                    if shiftCalDF.loc[x, "DayType"] in ['Wk', 'PH']:
                        shiftCalDF.loc[x, "ShiftType"] = shifttype
                        shiftCalDF.loc[x, "ShftHrs"] = shiftTypesDict[shifttype]
                        shiftCalDF.loc[x, "ShiftConfig"] = shiftconfig
                elif shiftconfig == "all.xd": 
                    if shiftCalDF.loc[x, "DayType"] in ['Wk', 'PH', 'Sat', 'Sun', 'PHSat','PHSun']:
                        shiftCalDF.loc[x, "ShiftType"] = shifttype
                        shiftCalDF.loc[x, "ShftHrs"] = shiftTypesDict[shifttype]
                        shiftCalDF.loc[x, "ShiftConfig"] = shiftconfig
    return(shiftCalDF)

# Initialises a shift calendar as pandas dataframe
# Each day for the specified year, months and mchines will be initialised with the nbr of the day, type of day, type of shift
# Shift Types and hours are set for workdays only, Public Holidays and Weekends  
def initShiftCalendar(year, months, machines, shiftType, country):
    shiftDays = []
    for ma in machines:
        for mo in months:
            noOfMthDays = nbrOfMonthDays(year,mo)
            for day in range (1, noOfMthDays+1):
                weekday = getWeekDay(year, mo, day)
                dayType = getDayType(year, mo, day, country)
                shiftConfig = 'Wk.5d'
                if dayType in ['Sat', 'PHSat','Sun', 'PHSun', 'PH']:
                    _shiftType = '0x0'
                else:
                    _shiftType = shiftType
                shftHrs = shiftTypesDict[_shiftType]
                if shftHrs == 0: 
                    workday = 0 
                else: 
                    workday = 1
                output = shftHrs * machineOutputKgHour[ma]
                shiftDays.append([year, mo, monthsNameList[mo-1], day, weekday, dayType, ma, _shiftType, shftHrs,output, workday, shiftConfig])
    shiftCalDF= pd.DataFrame(shiftDays, columns= ['Year', 'MthNbr', 'Month','Day', 'WeekDay','DayType', 'Machine','ShiftType',"ShftHrs",'Output','WorkDay', 'ShiftConfig'] ) 
    return (shiftCalDF)

def dispShftHrsMthMach(shiftCalDF, months, machines):
    smonths = sorted([monthsDict[m] for m in months])
    nmonths = [monthsNameList[m-1] for m in smonths]
    dfs = shiftCalDF [shiftCalDF['Machine'].isin(machines) & shiftCalDF['Month'].isin(months)]
    dfpiv = pd.pivot_table(dfs, index='Month', columns = 'Machine', values = 'ShftHrs', aggfunc = np.sum, margins=True)
    dfpiv = dfpiv.reindex(nmonths)
    return(dfpiv)

def dispShiftWorkdaysMthMach(shiftCalDF, months, machines):
    smonths = sorted([monthsDict[m] for m in months])
    nmonths = [monthsNameList[m-1] for m in smonths]
    dfs = shiftCalDF[shiftCalDF['Machine'].isin(machines) & shiftCalDF['Month'].isin(months)]
    dfpiv = pd.pivot_table(dfs, index='Month', columns = 'Machine', values = 'WorkDay', aggfunc = np.sum, margins=True)
    dfpiv = dfpiv.reindex(nmonths)
    return(dfpiv)

def dispOutputMthMach(shiftCalDF, months, machines):
    smonths = sorted(monthsDict[m] for m in months)
    nmonths = [monthsNameList[m-1] for m in smonths]
    dfs = shiftCalDF[shiftCalDF['Month'].isin(months) & shiftCalDF['Machine'].isin(machines)]
    dfpiv = pd.pivot_table(dfs, index = 'Month', columns = 'Machine', values = 'Output', aggfunc = np.sum, margins = True)
    dfpiv = dfpiv.reindex(nmonths)
    return(dfpiv)

def chartOutputMthMach(shiftCalDF, months, machines):
    dfs = shiftCalDF[shiftCalDF['Month'].isin(months) & shiftCalDF['Machine'].isin(machines)]
    dfs.plot(x="Day", y=['ShftHrs'], kind =  'bar')
    plt.show()
