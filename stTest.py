#import calendar
#from datetime import datetime
#from datetime import date
import datetime
#import numpy as np
#import matplotlib.pyplot as plt
#import pulp
import streamlit as st


#st.write(pulp.listSolvers())
#st.write(pulp.operating_system)

st.title("Optimisation of Plant Utilisation")
st.subheader('Selections')

st.sidebar.title('Plant Configuration')


# Plant Setup
# Machines available for production
machines = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']


mySelect = ['All']
mSelect = st.sidebar.radio('Machines',['All', 'Select'])
if mSelect == 'All':
   machSelect = machines
else:
   machSelect = st.sidebar.multiselect('Machines: ', machines)

# Standard Operating Hours per Day
stddayAvailHours = 24
st.sidebar.write("Available hours per day: "+ str(stddayAvailHours))

# Current Year used to create Production Calendar
year = [2021, 2022, 2023, 2024, 2025, 2026]
yearSelect = datetime.datetime.now().year
yearSelect = st.sidebar.selectbox("Year:", year)

# List of Month
monthlist= {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
monthSelect = st.sidebar.selectbox ("Month: ", [ m for m,k  in monthlist.items()])

shiftOptions = { '2x8': 16, '3x8': 24, '2x12': 24 }
shiftSelect = st.sidebar.selectbox ("Shift: ", [ m for m,k  in shiftOptions.items()])


st.write(str(machSelect))
st.write(str(yearSelect))
st.write(str(monthSelect))
st.write(str(shiftSelect))


for i in range(1, 10):
   cols = st.beta_column(4)
   cols[0] = st.write(f'{i}')
   cols[1] = st.write(f'{i}')
   cols[2] = st.write(f'{i}')
   cols[3] = st.write(f'{i}')
   


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




