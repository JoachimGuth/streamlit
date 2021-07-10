

import calendar
from datetime import datetime
from datetime import date
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import pulp
import streamlit as st


from prodCalendar import initShiftCalendar
from prodCalendar import dispShiftHoursMonthMachine
from prodCalendar import dispShiftWorkdaysMonthMachine

pd.set_option('display.max_rows', None)

#st.write(pulp.listSolvers())
#st.write(pulp.operating_system)

#st.title("Plant Optimisation")

st.set_page_config(layout= "wide", page_title ="Plant Utilisation",
                    #initial_sidebar_state="collapsed",#
                    page_icon="🔮")


#######################################################################
# General & common Paramters for plant and shift-calendar configuration
#######################################################################
# Machines available for production
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

shiftConfigDict = {'wk.5d': 0, 'wksat.6d': 1, 'wkend.7d': 2, 'phwk.5d': 3, 'ph.all':4}
shiftConfigNameList = [t for t in shiftTypesDict]
shiftTypesNbrList = [c for c in shiftTypesDict.values()]

dayTypesDict = {'Wk':0, 'Sat':1, 'Sun': 2, 'PH': 3, 'PHSat': 4, 'PHSun': 5}
dayTypesNameList = [t for t in dayTypesDict]
dayTypesNbrList = [c for c in dayTypesDict.values()]

# End - General & common Paramters for plant and shift-calendar configuration
################################ E N D ##########################################



############################## S T A R  T #######################################
# Initialize a Default ShifttCalendar for the  current year 
# Eachday of the year is initialised for all available machines with a 2*8 hour shift and 5 days a week work schedule configuration 'wk.5d'
shiftCal = pd.DataFrame()
shiftCal = initShiftCalendar(2021, monthsNbrList, machines, '2x8', 'Singapore')
################################ E N D ##########################################


############################## S T A R  T #######################################
# Main Application Selection Loop
# Select Application 
st.sidebar.subheader('Main Menu')
mainSelect = st.sidebar.radio('Select: ', ['View Shift Calendar', 'Configure Shift Calendar', 'Analyse Demand', 'Optimise Plant Utilisation'])
################################ E N D ##########################################


############################## S T A R  T #######################################
# Application - View Shift Calendar
#################################################################################
def viewCalendar():
   st.header ('Shift Calendar')
   st.sidebar.subheader('View Shift Calendar')
  
   # Overview and Summaries
   shiftHoursSummary = st.sidebar.radio('Calendar View', ['Overview','Details']) 
   if shiftHoursSummary == 'Overview':
       typeselection = st.sidebar.radio('Type', ['ShiftHours','WorkDays', 'Ouput']) 
       if typeselection == 'ShiftHours':
          st.subheader('Shift Hours')
          shdf = dispShftHrsMonthMachine(shiftCal, monthsNameList, machines)
       elif typeselection == 'WorkDays':
          st.subheader('Working Days')
          shdf = dispShiftWorkdaysMonthMachine(shiftCal, monthsNameList, machines)
       elif typeselection == 'Output':
          st.subheader('Production Output in kg/mth')
          shdf = dispShiftOuttputMthMach(shiftCal, monthsNameList, machines)
       st.dataframe(shdf)
   else:
   # Select one Month
      monthSelect = st.sidebar.radio('Select Month', monthsNameList)   
      machineSelect = st.sidebar.radio('Select Machine', machines)
      df = shiftCal[(shiftCal.Month == monthSelect) & (shiftCal.Machine == machineSelect)]
      st.write(monthSelect, machineSelect)
      st.dataframe(df[['Day', 'WeekDay', 'DayType', 'ShiftType','ShiftHours']])
  
 #End viewCalendar   
    

#######################################################################
# Application - Shift Configuration
#######################################################################
def configureShift():

   st.write("Initially all machines will be available for production for all month with default shift of 3x8 hours. In standard shift offering, public holidays and weekends are considered as non operating days. You can change the shift offering for certain machines and months for a certain year by selecting respectively. Not selected machines and month will be left unchanged in terms of shift offering.")
   
   st.sidebar.title('Shift Configuration')
   st.sidebar.write("Available hours per day: "+ str(stdDayAvailHours))

   # Select avaialble Machines - default: 'All'
   mSelect = 'All'
   machSelect = machines
   mSelect = st.sidebar.radio('Machines',['All', 'Select'])
   if mSelect == 'All':
      machSelect = machines
   else:
      machSelect = st.sidebar.multiselect('Machines:', machines)
      machSelect = list(machSelect)

   # Select year to configure Production Calendar; def = current
   yearSelect = datetime.datetime.now().year
   yearSelect = st.sidebar.selectbox("Year:", years)

   # Select Months - default = 'All'
   mthSelect = 'All'
   monthSelect = list(monthsNameList)
   mthSelect = st.sidebar.radio('Months',['All', 'Select'])
   if mthSelect == 'All':
      monthSelect = list(monthsNameList)
   else:
      monthSelect = st.sidebar.multiselect('Months: ', list(monthsNameList))

   # Shift Type selection
   shiftSelect = st.sidebar.selectbox("Shift: ", list(shiftOptionsList))

   # Display current selection and ishift configuration in the main window
   
   # Display currrent selection
   st.write("Machines: ", str(machSelect))
   st.write("Year: ", str(yearSelect))
   st.write("Months: ", str(monthSelect))
   st.write("Shift Model: ", str(shiftSelect))
   
   # Display shift config
   maSelect = 'All'
   maSelect = st.multiselect('Machines: ', machines)
   moSelect = date.today().month
   moSelect = st.multiselect('Month:  ', list(monthsNameList))
################################ E N D ##########################################
                                              
                                     

#################################################################################
# Application - Demand Analysis
#################################################################################
def analyseDemand():
   st.sidebar.title('Demand Analysis')
   pass
################################ E N D ##########################################

#################################################################################
# Application - Machine Utilisattion
#################################################################################
def optimiseUtilisation():
   st.sidebar.title('Optimisation')
   pass
################################ E N D ##########################################


#######################################################################
# Main Program Loop
################################################################################
if mainSelect == 'View Shift Calendar':
    viewCalendar()
elif mainSelect == 'Configure Shift Calendar':
   configureShift()
elif mainSelect == 'Analyse Demand':
   analyseDemand()
elif mainSelect == 'Optimise Plant Utilisation':
   optimiseUtilisation()
# End - Main Program Loop
################################ E N D ##########################################
    
    
    
    
