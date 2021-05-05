import streamlit as st
import pandas as pd 

header = st.beta_container()
dataset = st.beta_container() 
# ward_layout, frequency = st.beta_columns(2) 
# average_visits, hfr_count = st.beta_columns(2) 
ward_layout = st.beta_container() 
frequency = st.beta_container() 
average_visits = st.beta_container() 
hfr_count = st.beta_container() 

logs = pd.read_csv("posture_detection_logs.csv")

#calculating frequency of toilet use 
df_frequency = pd.DataFrame(columns = ["Time", "Frequency"])

#calculating number of toilet visits per day 
df_average_visits = logs.groupby("bed_number").count()
df_average_visits = df_average_visits.iloc[:, 0:1]
df_average_visits.reset_index(inplace = True)
df_average_visits.columns = ["Bed Number", "Frequency"]

#calculating patients by the HFR counts 
df_hfr_count = pd.DataFrame(columns = ["Bed Number", "HFR Count"])


with header: 
    st.title("Ward 37's HFR Patients")
    st.text("Creating the dashboard with fake data")

with dataset: 
    st.title("The Dataset")
    st.text("These are the logs for HFR patients.")
    st.write(logs)

with ward_layout: 
    st.title("Ward 37's Layout")
    st.text("This is the layout of Ward 37.")
    st.image("ward_layout.png")

with frequency: 
    st.title("Frequency of Toilet Use")
    st.text("This bar graph shows the average number of patients who use the toilet at that hour.")
    st.write(df_frequency)

with average_visits: 
    st.title("Average Number of Toilet Visits Per Day")
    st.text("This table shows the average number times each patient goes to the toilet.")
    st.write(df_average_visits)

with hfr_count: 
    st.title("Patients By Their HFR Counts")
    st.text("This table shows the total number of times that a HFR position was detected in this patient since they were warded.")
    st.write(df_hfr_count)


