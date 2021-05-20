import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import sqlite3
from sqlite3 import Error
import plotly.graph_objects as go

#connect database
try:
    conn = sqlite3.connect("Streamlit.db")
    print("Opened database successfully")
    
except Exception as e:
    print("Error during connection: ". str(e))

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# df_logs = conn.execute("SELECT * FROM Data")
sql = "SELECT * FROM Data_38"

st.set_page_config(layout="wide") #fills the whole webpage instead of centre column
header = st.beta_container()
dataset = st.beta_container() 

# refresh_bedno = st.beta_container() 
# frequency = st.beta_container() 
refresh_bedno, frequency = st.beta_columns(2)  # 2 by 2 grid layout
# average_visits = st.beta_container() 
# hfr_count = st.beta_container() 
average_visits, hfr_count = st.beta_columns(2) # 2 by 2 grid layout


#df_logs = pd.read_csv("posture_detection_logs.csv")

# calculating frequency of toilet use 
df_logs = pd.read_sql(sql, conn)
df_logs.columns = ["Bed Number", "Time Start","Time End","HFR_Count","MFR_Count"]
df_logs["Bed Number"] = df_logs["Bed Number"].astype(np.uint8)
df_logs["HFR_Count"] = df_logs["HFR_Count"].astype(np.uint8)
df_logs["MFR_Count"] = df_logs["MFR_Count"].astype(np.uint8)
df_logs["Time Start"] = pd.to_datetime(df_logs["Time Start"], unit='s') # change to datetime
df_logs["Time End"] = pd.to_datetime(df_logs["Time End"], unit='s') # change to datetime

df_frequency = df_logs

# df_frequency = conn.execute("SELECT bed_number as Bed_Number , DATE(TIMESTAMP_MILLIS(CAST(timestamp_start AS INT64))) AS Date FROM Data GROUP BY Date, Hour")
df_frequency = df_frequency.iloc[:, 0:2]
df_frequency["Date"] = df_frequency['Time Start'].dt.date # get date
df_frequency['Hour'] = df_frequency['Time Start'].dt.hour# get hour
df_frequency['Frequency'] = 1
df_frequency = df_frequency[["Date","Hour","Frequency"]]
df_hour_freq = df_frequency.groupby(["Date","Hour"],as_index=False).count() # group by time interval , count
df_hour_freq = df_hour_freq.groupby("Hour",as_index=False)["Frequency"].mean()  #mean number of times each patient uses the toilet each day
df_hour_freq.reset_index(inplace = True)
# df_hour_freq ["Date"]=df_hour_freq ["Date"].apply(lambda x: x.strftime("%d/%m/%Y")) #change to string for line graph

#calculating number of toilet visits per day 
df_average_visits = df_logs
df_average_visits = df_average_visits.iloc[:, 0:2]
df_average_visits["Time Start"] = pd.to_datetime(df_average_visits["Time Start"], unit='s') # change to datetime
df_average_visits["Date"] = df_average_visits['Time Start'].dt.date # get date
df_average_visits = df_average_visits.drop(columns = ["Time Start"])
df_average_visits['Frequency'] = 1
df_average_visits = df_average_visits.groupby(["Date","Bed Number"],as_index=False).count() #count the number of times each patient uses the toilet for each day
df_average_visits = df_average_visits.drop(columns = ["Date"])
df_average_visits = df_average_visits.groupby("Bed Number",as_index=False)["Frequency"].mean()  #mean number of times each patient uses the toilet each day
df_average_visits.sort_values("Frequency", inplace=True ,ascending=False,ignore_index=True)

#calculating patients by the HFR counts 
df_hfr_count = df_logs.groupby("Bed Number").sum()
df_hfr_count = df_hfr_count[["HFR_Count"]]
df_hfr_count.reset_index(inplace = True)
df_hfr_count.columns = ["Bed Number", "HFR Count"]
df_hfr_count.sort_values("HFR Count", inplace=True ,ascending=False,ignore_index=True)

with st.sidebar:
    bed_export = st.selectbox('Export Log from Bed Number',range(1,39))
    if st.button("Export"):
        now = datetime.datetime.now()
        timestamp_export = now.strftime("%d %m %Y %H%M")
        export_logs = df_logs[df_logs["Bed Number"] == bed_export]
        export_logs.to_csv('bed {0} fall risk log {1}.csv'.format(int(bed_export),timestamp_export),index=False)

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
    bed_refresh = st.selectbox('Insert a Bed Number',range(1,39))
    # st.write('The Bed Number Log that you would like to refresh is ', option)
    if st.button("Refresh"):
        refresh_command = "DELETE FROM Data_38 WHERE bed_number={0}".format(int(bed_refresh))
        execute_query(conn, refresh_command)
        # st.error("Refresh Bed Number {0}?".format(option))
        # if st.button("Yes"):
        #     command = "DELETE FROM Data_10 WHERE bed_number={0}".format(int(option))
        #     execute_query(conn, command)
            
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
    st.header("Average Frequency of Toilet Use")
    st.write("This graph shows the average number of patients who use the toilet at that hour.")
    st.write("Calculated by taking the starting timestamp.")
    # hist_hour_freq = fig = px.line(df_hour_freq, x='Hour', y='Frequency', color='Date') # plot line
    hist_hour_freq = fig = px.bar(df_hour_freq, x='Hour', y='Frequency') # plot histogram 
    st.plotly_chart(hist_hour_freq)


with average_visits: 
    st.header("Average Number of Toilet Visits Per Day")
    st.write("This table shows the average number times each patient goes to the toilet.")
    
    # st.write(df_average_visits) 
    hist_average_visits = fig = px.bar(df_average_visits, x='Bed Number', y='Frequency')
    hist_average_visits.add_trace(go.Scatter(x=df_average_visits['Bed Number'],y=[5]*38,showlegend = False))
    st.plotly_chart(hist_average_visits)
    
    # col1, col2 = st.beta_columns(2)
    # with col1:
    #     st.write(df_average_visits) 
    # with col2:
    #     hist_average_visits = fig = px.bar(df_average_visits, x='Bed Number', y='Frequency', color='Frequency')
    #     st.plotly_chart(hist_average_visits)

with hfr_count: 
    st.header("Patients By Their HFR Counts")
    st.write("This table shows the total number of times that a HFR position was detected in this patient since they were warded.")
    
    # st.write(df_hfr_count)
    
    # hist_hfr_count = fig = px.bar(df_hfr_count, x='Bed Number', y='HFR Count', color='HFR Count')
    hist_hfr_count = fig = px.bar(df_hfr_count, x='Bed Number', y='HFR Count')
    hist_hfr_count.add_trace(go.Scatter(x=df_hfr_count['Bed Number'],y=[10]*38,showlegend = False))
    st.plotly_chart(hist_hfr_count)
    # col1, col2 = st.beta_columns(2)
    # with col1:
    #     st.write(df_hfr_count)
    # with col2:
    #     hist_hfr_count = fig = px.bar(df_hfr_count, x='Bed Number', y='HFR Count', color='HFR Count')
    #     st.plotly_chart(hist_hfr_count)

conn.close()
