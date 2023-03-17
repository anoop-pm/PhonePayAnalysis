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


#----------------------------------- TRANSACTIONS ANALYSIS ----------------------------------

st.write('# :White[TRANSACTIONS ANALYSIS ]')
tab1, tab2, tab3, tab4 = st.tabs([ "Year Top ANALYSIS".upper(),"STATE ANALYSIS".upper(), "Payment Mode Year ANALYSIS".upper(), "OVERALL ANALYSIS".upper()])
#==================================================T FIGURE1 STATE ANALYSIS=======================================================

#=============================================T FIGURE2 DISTRICTS ANALYSIS=============================================
with tab1:
    st.write('# :WHITE[Transaction OverAll ANALYSIS ]')

    fig = px.bar(Data_Top_Transaction_Table, x="State", y="Total_Amount", color="State",
                 animation_frame="Year", animation_group="District", range_y=[0, 100000000000])

    st.plotly_chart(fig, use_container_width=True)


with tab2:
    Data_Aggregated_Transaction=Data_Aggregated_Transaction_df.copy()
    Data_Aggregated_Transaction.drop(Data_Aggregated_Transaction.index[(Data_Aggregated_Transaction["State"] == "india")],axis=0,inplace=True)
    State_PaymentMode=Data_Aggregated_Transaction.copy()
    # st.write('### :green[State & PaymentMode]')
    col1, col2 ,col3= st.columns(3)
    with col1:
        mode = st.selectbox(
            'Please select the Mode',
            ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='a')

    with col2:
        Y = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020','2021','2022'),key='Fssssa')
    with col3:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3', '4'), key='qwe2aasa')

    Mode=mode
    Year = int(Y)
    Quarter2 = int(Quarter)

    df_filtered = Data_Aggregated_Transaction[(Data_Aggregated_Transaction['Year'] == Year)]
    df_filtered2= df_filtered[(df_filtered['Quarter'] == Quarter2)]
    df_filtered3 = df_filtered2[(df_filtered2['Payment_Mode'] == mode)]


    fig = px.bar(df_filtered3, x='State', y='Total_Transactions_count',color="Total_Transactions_count",
                 color_continuous_scale="Viridis")


    st.write('#### '+str(Year)  +"--"+ str(Quarter2))
    st.plotly_chart(fig,use_container_width=True)


#=============================================T FIGURE3 YEAR ANALYSIS===================================================
with tab3:
    st.write('### :white[PaymentMode and Year]')
    col1, col2= st.columns(2)
    with col1:
        Y = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020','2021','2022'),key='Fssss')
    with col2:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3', '4'), key='qwe2as')


    Year=int(Y)
    Quarter2=int(Quarter)

    df_filtered = Data_Aggregated_Transaction[(Data_Aggregated_Transaction['Year'] == Year)]
    df_filtered2= df_filtered[(df_filtered['Quarter'] == Quarter2)]

    fig = px.pie(df_filtered2, values='Total_Transactions_count', names='Payment_Mode', title='Total_Transactions_count')
    st.plotly_chart(fig, use_container_width=True)


#=============================================T FIGURE4 OVERALL ANALYSIS=============================================
with tab4:
    years=Data_Aggregated_Transaction.groupby('Year')
    years_List=Data_Aggregated_Transaction['Year'].unique()
    years_Table=years.sum()
    del years_Table['Quarter']
    years_Table['year']=years_List
    total_trans=years_Table['Total_Transactions_count'].sum() # this data is used in sidebar
    fig1 = px.pie(years_Table, values='Total_Transactions_count', names='year',color_discrete_sequence=px.colors.sequential.Viridis, title='TOTAL TRANSACTIONS (2018 TO 2022)')
    col1, col2= st.columns([0.65,0.35])
    with col1:
        # st.write('### :Wh[Drastical Increase in Transactions :rocket:]')
        st.plotly_chart(fig1)
    with col2:
        # st.write('#### :green[Year Wise Transaction Analysis in INDIA]')
        st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)



