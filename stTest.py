import calendar
#from datetime import datetime
#from datetime import date
import datetime
#import numpy as np
#import matplotlib.pyplot as plt
#import pulp
import streamlit as st


#st.write(pulp.listSolvers())
#st.write(pulp.operating_system)

st.title("Plant Optimisation")

# Global Plant Paramters
# Machines available for production
machines = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

# Selectable Years
#years = [2021, 2022, 2023, 2024, 2025, 2026]
years = [datetime.datetime.now().year]

# List of Month
monthList= {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

# Standard Operating Hours per Day
stdDayAvailHours = 24


mainSelect = st.radio('Select: ', ['Shift Config', 'Demand Analysis', 'Optimisation'])

def shiftConfig():

   st.write("Initially all machines will be available for all month with default shift of 3x8 hours. Not selected machines and month will be set to not available for production, shift will be set to 0x0 hours.")
   st.sidebar.title('Shift Configuration')
   st.sidebar.write("Available hours per day: "+ str(stdDayAvailHours))

   # Select avaialble Machines - default: 'All'
   mSelect = 'All'
   machSelect = machines
   mSelect = st.sidebar.radio('Machines',['All', 'Select'])
   if mSelect == 'All':
      machSelect = machines
   else:
      machSelect = st.sidebar.multiselect('Machines:   ', machines)

   # Select year to configure Production Calendar; def = current
   yearSelect = datetime.datetime.now().year
   yearSelect = st.sidebar.selectbox("Year:  ", years)


   # Select Months - default = 'All'
   mthSelect = 'All'
   monthSelect = monthList
   mthSelect = st.sidebar.radio('Months',['All', 'Select'])
   if mthSelect == 'All':
      monthSelect = monthList
   else:
      monthSelect = st.sidebar.multiselect('Months: ', monthList)

   #monthSelect = st.sidebar.selectbox ("Month: ", [ m for m,k  in monthlist.items()])

   # Shift model selection
   shiftOptions = { '2x8': 16, '3x8': 24, '2x12': 24 }
   shiftSelect = st.sidebar.selectbox ("Shift: ", [ m for m,k  in shiftOptions.items()])

   # Display current selectin in main window
   st.write("Machines: ", str(machSelect))
   st.write("Year: ", str(yearSelect))
   st.write("Months: ", str(monthSelect))
   st.write("Shift Model: ", str(shiftSelect))


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



# Nbr of Days of a month in a particulat year
class DaysPerMonth(object):
   def numberOfDays(self, y, m):
      leap = 0
      if y % 400 == 0:
         leap = 1
      elif y % 100 == 0:
         leap = 0
      elif y % 4 == 0:
         leap = 1
      if m==2:
         return 28 + leap
      list = [1,3,5,7,8,10,12]
      if m in list:
         return 31
      return 30

# Instance of the Class Days per Month
dpm = DaysPerMonth()





