import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
# import mysql.connector 
# from mysql.connector import errorcode

st.set_page_config(layout="wide") #fills the whole webpage instead of centre column
header = st.beta_container()
dataset = st.beta_container() 

# refresh_bedno = st.beta_container() 
# frequency = st.beta_container() 
refresh_bedno, frequency = st.beta_columns(2)  # 2 by 2 grid layout
# average_visits = st.beta_container() 
# hfr_count = st.beta_container() 
average_visits, hfr_count = st.beta_columns(2) # 2 by 2 grid layout


df_logs = pd.read_csv("posture_detection_logs.csv")

# calculating frequency of toilet use 
df_frequency = df_logs
df_frequency = df_frequency.iloc[:, 0:2]
df_frequency.columns = ["Bed Number", "Time Start"]
df_frequency["Time Start"] = pd.to_datetime(df_frequency["Time Start"], unit='s') # change to datetime
df_frequency["Date"] = df_frequency['Time Start'].dt.date # get date
df_frequency['Hour'] = df_frequency['Time Start'].dt.hour# get hour
df_frequency['Frequency'] = 1
df_frequency = df_frequency[["Date","Hour","Frequency"]]
df_hour_freq = df_frequency.groupby(["Date","Hour"],as_index=False).count() # group by time interval , count
df_hour_freq.reset_index(inplace = True)
df_hour_freq ["Date"]=df_hour_freq ["Date"].apply(lambda x: x.strftime("%d/%m/%Y")) #change to string for line graph

#calculating number of toilet visits per day 
df_average_visits = df_logs
df_average_visits = df_average_visits.iloc[:, 0:2]
df_average_visits.columns = ["Bed Number", "Time Start"]
df_average_visits["Time Start"] = pd.to_datetime(df_average_visits["Time Start"], unit='s') # change to datetime
df_average_visits["Date"] = df_average_visits['Time Start'].dt.date # get date
df_average_visits = df_average_visits.drop(columns = ["Time Start"])
df_average_visits['Frequency'] = 1
df_average_visits = df_average_visits.groupby(["Date","Bed Number"],as_index=False).count() #count the number of times each patient uses the toilet for each day
df_average_visits = df_average_visits.drop(columns = ["Date"])
df_average_visits = df_average_visits.groupby("Bed Number",as_index=False)["Frequency"].mean()  #mean number of times each patient uses the toilet each day
df_average_visits.sort_values("Frequency", inplace=True ,ascending=False,ignore_index=True)

#calculating patients by the HFR counts 
df_hfr_count = df_logs.groupby("bed_number").sum()
df_hfr_count = df_hfr_count[["hfr_count"]]
df_hfr_count.reset_index(inplace = True)
df_hfr_count.columns = ["Bed Number", "HFR Count"]
df_hfr_count.sort_values("HFR Count", inplace=True ,ascending=False,ignore_index=True)


with header: 
    st.title("Ward 37's HFR Patients")
    st.write("Creating the dashboard with fake data")

# with dataset: 
#     st.header("The Dataset")
#     st.write("These are the logs for HFR patients.")
#     st.write(df_logs)

with refresh_bedno: 
    st.header("Refresh Bed Number Log") 
    st.write("This is the layout of Ward 37.")
    st.image("ward_layout.png")
    option = st.selectbox(
    'Insert a Bed Number',
    range(1,39))
    st.write('The Bed Number Log that you would like to refresh is ', option)
# if we want to use numeric inputs
    # number = st.number_input('Insert a Bed Number',step = 1, min_value = 1, max_value = 38)
    # st.write('The Bed Number Log that you would like to refresh is ', number)

# if we want to have different buttons (but for now not compatible with the 2 by 2 grid layout)
    # st.write("These are the buttons to refresh the logs for the specific bed numbers.")
      # for i in range(1, 10): #change such that only 38 beds
    #     col1,col2,col3,col4 = st.beta_columns(4)
    #     with col1:
    #         if st.button("Bed "+f"{i}"):
    #             st.write(" ") #insert function: refer you to refresh page,and refresh log 
    #     with col2:
    #         if st.button("Bed "+f"{i+10}"):
    #             st.write(" ") #insert function: refer you to refresh page,and refresh log 
    #     with col3:
    #         if st.button("Bed "+f"{i+20}"):
    #             st.write(" ") #insert function: refer you to refresh page,and refresh log 
    #     with col4:
    #         if st.button("Bed "+f"{i+30}"):
    #             st.write(" ") #insert function: refer you to refresh page,and refresh log 
    # with st.sidebar:
    #     st.write("This is the layout of Ward 37.")
    #     st.image("ward_layout.png")
    
with frequency: 
    st.header("Frequency of Toilet Use")
    st.write("This graph shows the total number of patients who use the toilet at that hour.")
    st.write("Calculated by taking the starting timestamp.")
    hist_hour_freq = fig = px.line(df_hour_freq, x='Hour', y='Frequency', color='Date') # plot histogram 
    st.plotly_chart(hist_hour_freq)


with average_visits: 
    st.header("Average Number of Toilet Visits Per Day")
    st.write("This table shows the average number times each patient goes to the toilet.")
    st.write(df_average_visits) 
    
    # hist_average_visits = fig = px.bar(df_average_visits, x='Bed Number', y='Frequency', color='Bed Number')
    # st.plotly_chart(hist_average_visits)

with hfr_count: 
    st.header("Patients By Their HFR Counts")
    st.write("This table shows the total number of times that a HFR position was detected in this patient since they were warded.")
    st.write(df_hfr_count)


