import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
import pymysql

import plotly.graph_objects as go
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")
st. set_page_config(layout="wide")

username='root'
password='root'


# CONNECTED TO (AWS)Amazon-Web-Services ----> (RDS)Relational-Database-Service
conn=pymysql.connect(
    host='localhost',
    user=username,
    password=password
)

# USING PhonepeDB I HAVE CREATED IN DATABASE-INSTANCE OF RDS
mycursor=conn.cursor()
sql='''USE PhonepeDB'''
mycursor.execute(sql)

# RETRIEVING DATA FROM CLOUD DATABASE
query = 'select * from Longitude_Latitude_State_Table'
Indian_States = pd.read_sql(query, con = conn)

# DATASETS
Data_Aggregated_Transaction_df= pd.read_csv(r'data/Data_Aggregated_Transaction_Table.csv')
Data_Aggregated_User_Summary_df= pd.read_csv(r'data/Data_Aggregated_User_Summary_Table.csv')
Data_Aggregated_User_df= pd.read_csv(r'data/Data_Aggregated_User_Table.csv')
Scatter_Geo_Dataset =  pd.read_csv(r'data/Data_Map_Districts_Longitude_Latitude.csv')
Coropleth_Dataset =  pd.read_csv(r'data/Data_Map_IndiaStates_TU.csv')
Data_Map_Transaction_df = pd.read_csv(r'data/Data_Map_Transaction_Table.csv')
Data_Map_User_Table= pd.read_csv(r'data/Data_Map_User_Table.csv')
Data_Top_User_Table= pd.read_csv(r'data/Data_TOP_User_Table.csv')
Data_Top_Transaction_Table= pd.read_csv(r'data/Data_TOP_Transaction_Table.csv')


# Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
# Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
# Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
# Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
# Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)

st.write('# :White[INDIAN STATE YEAR ANALYSIS ]')
fig64 = px.scatter(Indian_States, x="Registered_Users", y="Year_Quarter",
                 size="Registered_Users", color="Total_Amount", hover_name="state",
                 log_x=True, size_max=80)

st.plotly_chart(fig64,use_container_width=True)

c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021','2020','2019','2018'),key='y1h2k')
with c2:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qgwe2')


year=int(Year)
quarter=int(Quarter)

Coropleth_Dataset = Data_Top_User_Table.sort_values(by=['Registered_Users_Count'])
fig = px.bar(Coropleth_Dataset, x='State', y='Registered_Users_Count', hover_data=['State', 'District'],color="State",height=1200,title=str(year)+" Quarter-"+str(quarter))

st.plotly_chart(fig, use_container_width=True)
