

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
from prodCalendar import chartOutputMthMach

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
defaultMach = machines[0]

machineOutputKgHour = {'M1': 15, 'M2': 25, 'M3': 30, 'M4': 30, 'M5': 35, 'M6': 40, 'M7': 55, 'M8': 80}

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

monthsDict = {'Jan': 1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10,'Nov':11, 'Dec':12}
monthsNameList = [n for n in monthsDict]
monthsNbrList = [ n for  n in monthsDict.values()]
defaultMonthName = monthsNameList[0]
defaultMonthNbr = monthsNbrList[0]

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

# Init selectr opttions
yearSelect = currentYear
machSelect = machines
monthSelectName = monthsNameList
monthSelectNbr = monthsNbrList
shiftTypeSelect = defaultShiftType
shiftConfigSelect = defaultShiftConfig

# Init Shift Calendar
shiftCal = pd.DataFrame()
shiftCal = initShiftCalendar(yearSelect, monthsNbrList, machines, shiftTypeSelect, 'Singapore')
################################ E N D ##########################################



######################   M A I N   L O O P  #####################################
# Main Application Selection Loop
# Select Application 
st.sidebar.subheader('Main Menu')
mainSelect = st.sidebar.radio('Select: ', ['View Shift Calendar', 'Configure Shift Calendar', 'Analyse Demand', 'Optimise Plant Utilisation'])
################################ E N D ##########################################



#######################  V I E W  S H I F T  C A L  #############################
#################################################################################
def viewCalendar():
  st.header ('Shift Calendar')
  st.sidebar.subheader('View Shift Calendar')

  # Overview and Summaries
  selection = st.sidebar.radio('Calendar View', ['Settings','Overview','Details', 'Charts']) 
  if selection == 'Settings':
      st.subheader('Current Shift Settings')
      # Display current selection and shift configuration in the main window
      st.write("Machines: ", str(defaultMach))
      st.write("Year: ", str(currentYear))
      st.write("Months: ", str(defaultMonthName))
      st.write("Shift Hours: ", str(shiftTypeSelect))
      st.write("Shift Days: ", str(shiftConfigSelect))

      st.subheader('Initial Shift Configuration')
      st.write("Initially the Shift Calendar is configured for each day of the current year and for all available Machines. By default only work days are available for production. The default shift is 3 x 8 hours. ")
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
      st.subheader('Daily Shift Details by Month and Machine')
      monthSelect = st.sidebar.radio('Select Month', monthsNameList)   
      machSelect = st.sidebar.radio('Select Machine', machines)
      df = shiftCal[(shiftCal['Month'] == monthSelect) & (shiftCal['Machine'] == machSelect)]
      st.write('Month: ', monthSelect, '   Machine:  ', machSelect)
      st.dataframe(df[['Day', 'WeekDay', 'DayType', 'ShiftType','ShftHrs']])
  elif selection == 'Charts':
      st.subheader('Daily Shift Details by Month and Machine')
      monthSelect = st.sidebar.radio('Select Month', monthsNameList)   
      machSelect = st.sidebar.radio('Select Machine', machines)
      st.write('Month: ', monthSelect, '   Machine:  ', machSelect)
      df = shiftCal[(shiftCal['Month'].isin([monthSelect])) & (shiftCal['Machine'].isin([machSelect]))]
      #st.dataframe(df)
      dff= df[['Month', 'Machine','Day','WorkDay', 'ShftHrs', 'Output']]
      #st.dataframe(dff)
      dfs = dff.set_index('Day')
      #st.dataframe(dfs)
      #st.bar_chart(dfs)
      st.bar_chart(dfs['ShftHrs'])
      st.bar_chart(dfs['Output'])
      
      selcal = shiftCal[['Month', 'Machine', 'WorkDay','ShftHrs', 'Output']]
      scal = selcal.groupby(["Month"])["Output"].sum().reset_index()
      st.dataframe(scal)
      #st.bar_chart(scal)
      st.bar_chart(scal['Output'])
      scal = selcal.groupby(["Month"])["ShftHrs"].sum().reset_index()
      st.bar_chart(scal['ShftHrs'])
      scal = selcal.groupby(["Machine"])["ShftHrs"].sum().reset_index('Machine')
      st.bar_chart(scal['ShftHrs'])
      
     
################################ E N D ##########################################



###################  S H I F T  C O N F I G U R A T I O N  ######################
#################################################################################
def configureShift(masel,mosel, ysel, sTSelect, sCSelect ):
   machSelect = masel
   monthSelectName  = mosel
   yearSelect = ysel
   shiftTypeSelect = sTSelect
   shiftConfigSelect = sCSelect
   st.header('Configure Shift Calendar')
   st.subheader('Current Shift Settings')
   # #### need to change to table overview
   st.write("Machines: ", str(machSelect))
   st.write("Year: ", str(yearSelect))
   st.write("Months: ", str(monthSelectName))
   st.write("Shift Hours: ", str(shiftTypeSelect))
   st.write("Shift Days: ", str(shiftConfigSelect))

   st.sidebar.subheader('Configure Shift Calendar')
   # Select avaialble Machines - default: 'All'
   select = st.sidebar.radio('Machines',['All', 'Machines'])
   if select == 'All':
      machSelect = list(machines)
   elif select == 'Machines':
      machSelect = st.sidebar.multiselect('Machines:', machines)
      machSelect = list(machSelect)

   # Select year to configure Production Calendar; def = current
   yearSelect = st.sidebar.selectbox("Year:", yrList)

   # Select Months - default = 'All'
   select = st.sidebar.radio('Months',['All', 'Months'])
   if select == 'All':
      monthSelect = list(monthsNameList)
   elif select == 'Months':
      monthSelect = st.sidebar.multiselect('Months: ', list(monthsNameList))

   # Select Shift Type
   shiftTypesSelect = st.sidebar.selectbox("Shift Type: ", list(shiftTypesNameList))

   # Select Shoft Configuration
   shiftConfigSelect = st.sidebar.selectbox("Shift Config: ", list(shiftConfigNameList))

   # Display current selection and shift configuration in the main window
   st.subheader('New Selections')
   st.write("Machines: ", str(machSelect))
   st.write("Year: ", str(yearSelect))
   st.write("Months: ", str(monthSelect))
   st.write("Shift Hours: ", str(shiftTypesSelect))
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
   configureShift(machSelect, monthSelectName, yearSelect, shiftTypeSelect, shiftConfigSelect)
elif mainSelect == 'Analyse Demand':
   analyseDemand()
elif mainSelect == 'Optimise Plant Utilisation':
   optimiseUtilisation()
# End - Main Program Loop
################################ E N D ##########################################
    
    
    
    
