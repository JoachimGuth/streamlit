

import calendar
from datetime import datetime
from datetime import date
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import pulp
import streamlit as st

st.set_page_config(layout= "wide", page_title ="Plant Utilisation",
                    initial_sidebar_state="collapsed",
                    page_icon="🔮")

from prodCalendar import initShiftCalendar


#st.write(pulp.listSolvers())
#st.write(pulp.operating_system)

st.title("Plant Optimisation")

# Global Plant Paramters
# Machines available for production
machines = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

# Selectable Years
years = [2021, 2022, 2023, 2024, 2025, 2026]
#years = [yr for yr in range(datetime.datetime.now().year,datetime.datetime.now().year+10)]

# List of Month
monthDict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
monthList = [m for m in monthDict.values()]

# Standard Operating Hours per Day
stdDayAvailHours = 24

# Possible shift operating configurations
shiftOptionsDict = { '2x8': 16, '3x8': 24, '2x12': 24 }
shiftOptionsList = [s for s in shiftOptionsDict.keys()]


# Select Application - default: Shift Configuration
mainSelect = 'Shift Config'
mainSelect = st.radio('Select: ', ['Shift Config', 'Demand Analysis', 'Optimisation'])


#Initialize ShifttCalendar for year 2021
# Eachday of the year is initialised for all available machines with a 2*8 hour shift and 5 days a week work schedule configuration 'wk.5d'
df = pd.DataFrame()
df = initShiftCalendar(2021, monthList , machines, '2x8', 'Singapore')
df




def displayShiftConfigData(machine,month):
   pass

def displayShiftConfigChart(machine,month):
   pass

def setOpHours(machine, month):
   pass


# Application - Shift Configuration

def shiftConfig():

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
   monthSelect = list(monthList)
   mthSelect = st.sidebar.radio('Months',['All', 'Select'])
   if mthSelect == 'All':
      monthSelect = list(monthList)
   else:
      monthSelect = st.sidebar.multiselect('Months: ', list(monthList))

   # Shift model selection
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
   moSelect = st.multiselect('Month:  ', list(monthList))
                                              
                                     
   


def demandAnalysis():
   st.sidebar.title('Demand Analysis')
   pass

def optimisation():
   st.sidebar.title('Optimisation')
   pass


# Main Program Loop
if mainSelect == 'Shift Config':
   shiftConfig()
elif mainSelect == 'Demand Analysis':
   demandAnalysis()
elif mainSelect == 'Optimisation':
   optimisation()



def table():
   for i in range(1, 10):
      c1, c2, c3, c4 = st.beta_columns(4)
      c1 = st.write(f'{i}')
      c2 = st.write(f'{i}')
      c3 = st.write(f'{i}')
      c4 = st.write(f'{i}')
