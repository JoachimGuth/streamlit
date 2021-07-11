

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
from prodCalendar import dispShftHrsMthMach
from prodCalendar import dispShiftWorkdaysMthMach
from prodCalendar import dispOutputMthMach

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
defaultShiftType = '3x8'

shiftConfigDict = {'wk.5d': 0, 'wksat.6d': 1, 'wkend.7d': 2, 'phwk.5d': 3, 'ph.all':4}
shiftConfigNameList = [t for t in shiftConfigDict]
shiftConfigNbrList = [c for c in shiftConfigDict.values()]
defaultShiftConfig = 'wk.d5'

dayTypesDict = {'Wk':0, 'Sat':1, 'Sun': 2, 'PH': 3, 'PHSat': 4, 'PHSun': 5}
dayTypesNameList = [t for t in dayTypesDict]
dayTypesNbrList = [c for c in dayTypesDict.values()]

yrList = [cy for cy in range(date.today().year,date.today().year+5)]
currentYear = date.today().year

# End - General & common Paramters for plant and shift-calendar configuration
################################ E N D ##########################################



################ I N I T   S H I F T   C A L ####################################
# Initialize a Default ShifttCalendar for the  current year 
# Eachday of the year is initialised for all available machines with a 2*8 hour shift and 5 days a week work schedule configuration 'wk.5d'
shiftCal = pd.DataFrame()
yearSelect = currentYear
machSelect = machines
monthSelectName = monthsNameList
monthSelectNbr = monthsNbrList
shiftTypeSelect = defaultShiftType
shiftConfigSelect = defaultShiftConfig
shiftCal = initShiftCalendar(yearSelect, monthSelectNbr, machSelect, shiftTypeSelect, 'Singapore')

################################ E N D ##########################################


######################   M A I N   L O O P  #####################################
# Main Application Selection Loop
# Select Application 
st.sidebar.subheader('Main Menu')
mainSelect = st.sidebar.radio('Select: ', ['View Shift Calendar', 'Configure Shift Calendar', 'Analyse Demand', 'Optimise Plant Utilisation'])
################################ E N D ##########################################


#######################  V I E W  S H I F T  C A L  #############################
# Application - View Shift Calendar
#################################################################################
def viewCalendar():
   st.header ('Shift Calendar')
   st.sidebar.subheader('View Shift Calendar')
  
   # Overview and Summaries
   selection = st.sidebar.radio('Calendar View', ['Settings','Overview','Details']) 
   if selection == 'Settings':
         st.subheader('Current Shift Settings')
    
         # Display current selection and shift configuration in the main window
         st.write("Machines: ", str(machSelect))
         st.write("Year: ", str(yearSelect))
         st.write("Months: ", str(monthSelectName))
         st.write("Shift Hours: ", str(shiftTypeSelect))
         st.write("Shift Days: ", str(shiftConfigSelect))
         
         st.subheader('Initial Shift Configuration')
         st.write("Initially the Shift Calendar is configured for each day of the current year and for all available Machines. \
                   By default only work days are available for production. The default shift is 3 x 8 hours. ")
         st.write('Available Years: ', str(yrList))
         st.write("Available Machines: ", str(machines))
         st.write('Available Months: ', str(monthsNameList))
         st.write("Available Shift Hours: ", str(shiftTypesNameList))
         st.write("Available Shift Days: ", str(shiftConfigNameList))
        
   elif selection == 'Overview':
       typeselection = st.sidebar.radio('Type', ['Operating Hours','WorkDays', 'Output']) 
       if typeselection == 'Operating Hours':
          st.subheader('Operating Hours')
          shdf = dispShftHrsMthMach(shiftCal, monthsNameList, machines)
          st.dataframe(shdf)
       elif typeselection == 'WorkDays':
          st.subheader('Working Days')
          shdf = dispShiftWorkdaysMthMach(shiftCal, monthsNameList, machines)
          st.dataframe(shdf)
       elif typeselection == 'Output':
          st.subheader('Production Output in kg/mth')
          shdf = dispOutputMthMach(shiftCal, monthsNameList, machines)
          st.dataframe(shdf)
    elif selection == 'Details':
       # Select by Month and Machine
       st.subheader('Daily Shift Calendar by Month and Machine')
       monthSelect = st.sidebar.radio('Select Month', monthsNameList)   
       machineSelect = st.sidebar.radio('Select Machine', machines)
       df = shiftCal[(shiftCal.Month == monthSelect) & (shiftCal.Machine == machineSelect)]
       st.write('Month: ', monthSelect, '   Machine:  ', machineSelect)
       st.dataframe(df[['Day', 'WeekDay', 'DayType', 'ShiftType','ShftHrs']])
  
# End viewCalendar   
################################ E N D ##########################################



###################  S H I F T  C O N F I G U R A T I O N  ######################
# Application - Shift Configuration
#################################################################################
def configureShift():
   st.header('Configure Shift Calendar')
   
   st.subheader('Current Shift Settings')
   yearSelect = yearSelect
   # Display current selection and shift configuration in the main window
   #st.write("Machines: ", str(machSelect))
   st.write("Year: ", str(yearSelect))
   st.write("Months: ", str(monthSelectName))
   st.write("Shift Hours: ", str(shiftTypeSelect))
   st.write("Shift Days: ", str(shiftConfigSelect))
    
    
   st.sidebar.subheader('Configure Shift Calendar')
   machSelect = list(machines)
   monthSelect = list(monthsNameList)
   yearSelect = currentYear
   shiftTypeSelect = defaultShiftType
   shiftConfigSelect = defaultShiftConfig
    
   # Select avaialble Machines - default: 'All'
   mselect = 'All'
   mSelect = st.sidebar.radio('Machines',['All', 'Machines'])
   if mSelect == 'All':
      machSelect = list(machines)
   elif mSelect == 'Machines':
      machSelect = st.sidebar.multiselect('Machines:', machines)
      machSelect = list(machSelect)
      
   # Select year to configure Production Calendar; def = current
   yearSelect = date.today().year
   yearSelect = st.sidebar.selectbox("Year:", yrList)
  
   # Select Months - default = 'All'
   mthSelect = 'All'
   mthSelect = st.sidebar.radio('Months',['All', 'Months'])
   if mthSelect == 'All':
      monthSelect = list(monthsNameList)
   elif mthSelect == 'Months':
      monthSelect = st.sidebar.multiselect('Months: ', list(monthsNameList))

   # Select Shift Type
   shiftTypesSelect = st.sidebar.selectbox("Shift Type: ", list(shiftTypesNameList))
    
   # Select Shoft Configuration
   shiftConfigSelect = st.sidebar.selectbox("Shift Config: ", list(shiftConfigNameList))

   # Display current selection and shift configuration in the main window
   st.write("Machines: ", str(machSelect))
   st.write("Year: ", str(yearSelect))
   st.write("Months: ", str(monthSelect))
   st.write("Shift Hours: ", str(shiftTypeSelect))
   st.write("Shift Days: ", str(shiftConfigSelect))
   
   

################################ E N D ##########################################
                                              
                                     

#################################################################################
# Application - Demand Analysis
#################################################################################
def analyseDemand():
   st.header('This part is under development')
   st.sidebar.title('Demand Analysis')
   pass
################################ E N D ##########################################

#################################################################################
# Application - Machine Utilisattion
#################################################################################
def optimiseUtilisation():
   st.header('This part is under development')
   st.sidebar.title('Optimisation')
   pass
################################ E N D ##########################################


#################################################################################
# Main Program Loop
#################################################################################
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
    
    
    
    
