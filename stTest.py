

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
machines = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

# Selectable Years
years = [2021, 2022, 2023, 2024, 2025, 2026]
#years = [yr for yr in range(datetime.datetime.now().year,datetime.datetime.now().year+10)]

# List of Month
monthsDict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
monthsNbrList = [m for m in monthsDict.values()]
monthsNameList = [n for n in monthsDict.keys()]

# Standard Operating Hours per Day
stdDayAvailHours = 24

# Possible shift operating configurations
shiftOptionsDict = { '2x8': 16, '3x8': 24, '2x12': 24 }
shiftOptionsList = [s for s in shiftOptionsDict.keys()]

# End - General & common Paramters for plant and shift-calendar configuration
#############################################################################



############################## S T A R  T #######################################
# Initialize a Default ShifttCalendar for the  current year 
# Eachday of the year is initialised for all available machines with a 2*8 hour shift and 5 days a week work schedule configuration 'wk.5d'
shiftCal = pd.DataFrame()
shiftCal = initShiftCalendar(2021, monthsNbrList, machines, '2x8', 'Singapore')
################################ E N D ########################################


############################## S T A R  T #######################################
# Main Application Selection Loop
# Select Application 
st.sidebar.subheader('Main Menu')
mainSelect = st.sidebar.radio('Select: ', ['View Shift Calendar', 'ConfigureShift Calendar', 'Analyse Demand', 'Optimisw Plant Utilisation'])
################################ E N D ########################################



#######################################################################
# Application - View Shift Calendar
#######################################################################
def viewCalendar():
   st.header ('Shift Calendar')
   st.sidebar.subheader('View Shift Calendar')
  
   # Overview and Summaries
   shiftHoursSummary = st.sidebar.radio('Calendar View', ['Overview','Details']) 
   if shiftHoursSummary == 'Overview':
       typeselection = st.sidebar.radio('Type', ['ShiftHours','WorkDays']) 
       if typeselection == 'ShiftHours':
          st.subheader('Shift Hours')
          shdf = dispShiftHoursMonthMachine(shiftCal, monthsNameList, machines)
       elif typeselection == 'WorkDays':
          st.subheader('Working Days')
          shdf = dispShiftWorkdaysMonthMachine(shiftCal, monthsNameList, machines)
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
                                              
                                     

#######################################################################
# Application - Demand Analysis
########################################################################
def analyseDemand():
   st.sidebar.title('Demand Analysis')
   pass

#######################################################################
# Application - Machine Utilisattion
########################################################################
def optimiseUtilisation():
   st.sidebar.title('Optimisation')
   pass

#######################################################################
# Main Program Loop
########################################################################
if mainSelect == 'View Shift Calendar':
    viewCalendar()
elif mainSelect == 'Configure Shift Calendar':
   configureShift()
elif mainSelect == 'analyseDemand':
   analyseDemand()
elif mainSelect == 'optimiseUtilisation':
   optimiseUtilisation()
# End - Main Program Loop
########################################################################
    
    
    
    
