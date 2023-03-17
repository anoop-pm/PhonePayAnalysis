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





#Indian_States= pd.read_csv(r'data/Longitude_Latitude_State_Table.csv')
colT1,colT2 = st.columns([2,8])
with colT2:
    st.title('PhonePe Pulse Data Analysis:signal_strength')




# INDIA MAP ANALYSIS BY State
st.write("### **:PURPLE[PhonePe Pulse India GEO]**")
c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022'))
with c2:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'))
year=int(Year)
quarter=int(Quarter)
Transaction_scatter_districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['Year'] == year ) & (Data_Map_Transaction_df['Quarter']==quarter) ].copy()
Transaction_Coropleth_States=Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
Transaction_scatter_districts.drop(Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],axis=0,inplace=True)
# Dynamic Scattergeo Data Generation
Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'], ascending=False)
Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False) 
Total_Amount=[]
for i in Transaction_scatter_districts['Total_Amount']:
    Total_Amount.append(i)
Scatter_Geo_Dataset['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Transaction_scatter_districts['Total_Transactions_count']:
    Total_Transaction.append(i)
Scatter_Geo_Dataset['Total_Transactions']=Total_Transaction
Scatter_Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
# Dynamic Coropleth
Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
Total_Amount=[]
for i in Transaction_Coropleth_States['Total_Amount']:
    Total_Amount.append(i)
Coropleth_Dataset['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Transaction_Coropleth_States['Total_Transactions_count']:
    Total_Transaction.append(i)
Coropleth_Dataset['Total_Transactions']=Total_Transaction
# -------------------------------------FIGURE1 INDIA MAP------------------------------------------------------------------

#scatter plotting the states codes
Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)
fig=px.scatter_geo(Indian_States,
                    lon=Indian_States['Longitude'],
                    lat=Indian_States['Latitude'],                                
                    text = Indian_States['code'], #It will display district names on map
                    hover_name="state", 
                    hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                    )
fig.update_traces(marker=dict(color="white" ,size=0.3))
fig.update_geos(fitbounds="locations", visible=False,)
    # scatter plotting districts
Scatter_Geo_Dataset['col']=Scatter_Geo_Dataset['Total_Transactions']
fig1=px.scatter_geo(Scatter_Geo_Dataset,
                    lon=Scatter_Geo_Dataset['Longitude'],
                    lat=Scatter_Geo_Dataset['Latitude'],
                    color=Scatter_Geo_Dataset['col'],
                    size=Scatter_Geo_Dataset['Total_Transactions'],     
                    #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                    hover_name="District", 
                    hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                    title='District',
                    size_max=22,)
fig1.update_traces(marker=dict(color="rgb(162, 2, 204)" ,line_width=1))    #rebeccapurple
#coropleth mapping india
fig_ch = px.choropleth(
                    Coropleth_Dataset,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',

                    color_continuous_scale='Reds',
                    color="Total_Transactions"
                    )
fig_ch.update_geos(fitbounds="locations", visible=False,)
#combining districts states and coropleth
fig_ch.add_trace( fig.data[0])
fig_ch.add_trace(fig1.data[0])

colT1,colT2 = st.columns([6,1])
with colT1:
    st.plotly_chart(fig_ch, use_container_width=True)

# -----------------------------------------------FIGURE2 States BARGRAPH------------------------------------------------------------------------

st.write("### **:PURPLE[PhonePe Pulse India Analysis]**")

Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
fig = px.bar(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter))

st.plotly_chart(fig, use_container_width=True)




# --------------------------------------------SCATTER INDIA ANALYSIS----------------------------------------------------------------

st.write("### **:WHITE[PhonePe Pulse Total Usage data]**")
year=int(Year)
quarter=int(Quarter)
df_filtered = Data_Top_User_Table[(Data_Top_User_Table['Year'] == int(Year))]
df_filtered2 = df_filtered[(df_filtered['Quater'] == int(Quarter))]
Coropleth_Dataset = df_filtered2.sort_values(by=['Registered_Users_Count'])
fig = px.bar(Coropleth_Dataset, x='State', y='Registered_Users_Count', hover_data=['State', 'District'],color="State",height=800,title=str(year)+" Quarter-"+str(quarter))

st.plotly_chart(fig, use_container_width=True)


#----------------------------------- MOBILE PHONE ANALYSIS ----------------------------------


st.write('# :WHITE[MobilePhone DATA ANALYSIS ]')
tab1, tab2, tab3 = st.tabs(["STATE ANALYSIS","YEAR ANALYSIS","OVERALL ANALYSIS"])

with tab1 :
    st.write('### :WHITE[MobileBrands By State]')
    state = st.selectbox(
            'Please select the State',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal'),key='W')

    c1, c2 = st.columns(2)
    with c1:
        Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021', '2020', '2019', '2018'), key='y1h2kk')
    with c2:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3', '4'), key='qgwe24')
    df_filtered = Data_Aggregated_User_df[(Data_Aggregated_User_df['Year'] == int(Year))]
    df_filtered2 = df_filtered[(df_filtered['Quarter'] == int(Quarter))]

    df_filtered2s = df_filtered2[(df_filtered2['State'] == state)]

    fig = px.bar(df_filtered2s, x='Brand_Name', y='Registered_Users_Count',hover_data=['State', 'Brand_Name'],color="Brand_Name", title=str(Year) + " Quarter-" + str(Quarter))

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write('### :WHITE[MobileBrands usage year analysis]')
    c1, c2 = st.columns(2)
    with c1:
        Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021', '2020', '2019', '2018'), key='y1h2kksa')
    with c2:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3', '4'), key='qgwe24sa')
    df_filtered = Data_Aggregated_User_df[(Data_Aggregated_User_df['Year'] == int(Year))]
    df_filtered2 = df_filtered[(df_filtered['Quarter'] == int(Quarter))]
    fig = px.bar(df_filtered2, x='Brand_Name', y='Registered_Users_Count', hover_data=['State', 'Brand_Name'],
                 color="Brand_Name", title=str(Year) + " Quarter-" + str(Quarter))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.write('### :WHITE[Top Mobile Brands]')

    c1, c2 = st.columns(2)
    with c1:
        Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021', '2020', '2019', '2018'), key='y1h2kks')
    with c2:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3', '4'), key='qgwe24s')
    df_filtered = Data_Aggregated_User_df[(Data_Aggregated_User_df['Year'] == int(Year))]
    df_filtered2 = df_filtered[(df_filtered['Quarter'] == int(Quarter))]
    top_5_brands = df_filtered2.sort_values('Registered_Users_Count', ascending=False).head(5)[['Brand_Name', 'Registered_Users_Count']]

    c1, c2 = st.columns(2)
    with c1:
        st.write("Top 5 Brands")
        fig = px.pie(top_5_brands, values='Registered_Users_Count', names='Brand_Name')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.write("Brands OverAll Analysis")
        fig = px.pie(df_filtered2, values='Registered_Users_Count', names='Brand_Name')
        st.plotly_chart(fig, use_container_width=True)
    fig = go.Figure(data=[go.Table(header=dict(values=list(top_5_brands.columns)),
                                   cells=dict(values=[top_5_brands.Brand_Name, top_5_brands.Registered_Users_Count]))])
    st.plotly_chart(fig, use_container_width=True)



#----------------------------------- TRANSACTIONS ANALYSIS ----------------------------------

st.write('# :White[TRANSACTIONS ANALYSIS ]')
tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS", "YEAR ANALYSIS", "OVERALL ANALYSIS"])
#==================================================T FIGURE1 STATE ANALYSIS=======================================================
with tab1:
    Data_Aggregated_Transaction=Data_Aggregated_Transaction_df.copy()
    Data_Aggregated_Transaction.drop(Data_Aggregated_Transaction.index[(Data_Aggregated_Transaction["State"] == "india")],axis=0,inplace=True)
    State_PaymentMode=Data_Aggregated_Transaction.copy()
    # st.write('### :green[State & PaymentMode]')
    col1, col2= st.columns(2)
    with col1:
        mode = st.selectbox(
            'Please select the Mode',
            ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='a')
    with col2:
        state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='b')
    State= state
    Year_List=[2018,2019,2020,2021,2022]
    Mode=mode
    State_PaymentMode=State_PaymentMode.loc[(State_PaymentMode['State'] == State ) & (State_PaymentMode['Year'].isin(Year_List)) &
                            (State_PaymentMode['Payment_Mode']==Mode )]
    State_PaymentMode = State_PaymentMode.sort_values(by=['Year'])
    State_PaymentMode["Quarter"] = "Q"+State_PaymentMode['Quarter'].astype(str)
    State_PaymentMode["Year_Quarter"] = State_PaymentMode['Year'].astype(str) +"-"+ State_PaymentMode["Quarter"].astype(str)
    fig = px.bar(State_PaymentMode, x='Year_Quarter', y='Total_Transactions_count',color="Total_Transactions_count",
                 color_continuous_scale="Viridis")


    st.write('#### '+State.upper())
    st.plotly_chart(fig,use_container_width=True)
#=============================================T FIGURE2 DISTRICTS ANALYSIS=============================================
with tab2:
    col1, col2, col3= st.columns(3)
    with col1:
        Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022'),key='y1')
    with col2:
        state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='dk')
    with col3:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qwe')
    districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['State'] == state ) & (Data_Map_Transaction_df['Year']==int(Year))
                                          & (Data_Map_Transaction_df['Quarter']==int(Quarter))]
    l=len(districts)
    fig = px.bar(districts, x='Place_Name', y='Total_Transactions_count',color="Total_Transactions_count",
                 color_continuous_scale="Viridis")
    # colT1,colT2 = st.columns([7,3])
    # with colT1:
    st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
    st.plotly_chart(fig,use_container_width=True)

#=============================================T FIGURE3 YEAR ANALYSIS===================================================
with tab3:
    #st.write('### :green[PaymentMode and Year]')
    col1, col2= st.columns(2)
    with col1:
        M = st.selectbox(
            'Please select the Mode',
            ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='Dss')
    with col2:
        Y = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020','2021','2022'),key='Fss')
    Year_PaymentMode=Data_Aggregated_Transaction.copy()
    Year=int(Y)
    Mode=M
    Year_PaymentMode=Year_PaymentMode.loc[(Year_PaymentMode['Year']==Year) &
                            (Year_PaymentMode['Payment_Mode']==Mode )]
    States_List=Year_PaymentMode['State'].unique()
    State_groupby_YP=Year_PaymentMode.groupby('State')
    Year_PaymentMode_Table=State_groupby_YP.sum()
    Year_PaymentMode_Table['states']=States_List
    del Year_PaymentMode_Table['Quarter'] # ylgnbu', 'ylorbr', 'ylorrd teal
    del Year_PaymentMode_Table['Year']
    Year_PaymentMode_Table = Year_PaymentMode_Table.sort_values(by=['Total_Transactions_count'])
    fig2= px.bar(Year_PaymentMode_Table, x='states', y='Total_Transactions_count',color="Total_Transactions_count",
                color_continuous_scale="Viridis",)
    # colT1,colT2 = st.columns([7,3])
    # with colT1:
    st.write('#### '+str(Year)+' DATA ANALYSIS')
    st.plotly_chart(fig2,use_container_width=True)

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


st.write('# :WHITE[Transaction OverAll ANALYSIS ]')

fig= px.bar(Data_Top_Transaction_Table, x="State", y="Total_Amount", color="State",
  animation_frame="Year", animation_group="District", range_y=[0,100000000000])


st.plotly_chart(fig, use_container_width=True)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ USER ANALYSIS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

st.write('# :WHITE[USERS DATA ANALYSIS ]')
tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS","YEAR ANALYSIS","OVERALL ANALYSIS"])

# =================================================U STATE ANALYSIS ========================================================
with tab1:
    st.write('### :WHITE[State & Userbase]')
    state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='Ws')
    app_opening=Data_Aggregated_User_Summary_df.groupby(['State','Year'])
    a_state=app_opening.sum()
    la=Data_Aggregated_User_Summary_df['State'] +"-"+ Data_Aggregated_User_Summary_df["Year"].astype(str)
    a_state["state_year"] = la.unique()
    sta=a_state["state_year"].str[:-5]
    a_state["state"] = sta
    sout=a_state.loc[(a_state['state'] == state) ]
    ta=sout['AppOpenings'].sum()
    tr=sout['Registered_Users'].sum()
    sout['AppOpenings']=sout['AppOpenings'].mul(100/ta)
    sout['Registered_Users']=sout['Registered_Users'].mul(100/tr).copy()
    fig = go.Figure(data=[
        go.Bar(name='AppOpenings %', y=sout['AppOpenings'], x=sout['state_year'], marker={'color': '#006152'}),
        go.Bar(name='Registered Users %', y=sout['Registered_Users'], x=sout['state_year'],marker={'color': '#00fbff'})
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    # colT1,colT2 = st.columns([7,3])
    # with colT1:
    st.write("#### ",state.upper())
    st.plotly_chart(fig, use_container_width=True, height=200)

# ==================================================U DISTRICT ANALYSIS ====================================================
with tab2:
    col1, col2, col3= st.columns(3)
    with col1:
        Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021','2020','2019','2018'),key='y12')
    with col2:
        state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='dk2')
    with col3:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qwe2')

    districts=Data_Map_User_Table.loc[(Data_Map_User_Table['State'] == state ) & (Data_Map_User_Table['Year']==int(Year))
                                          & (Data_Map_User_Table['Quarter']==int(Quarter))]
    l=len(districts)
    fig = px.bar(districts, x='Place_Name', y='App_Openings',color="App_Openings",
                 color_continuous_scale="blues")

    if l:
        st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.write('#### NO DISTRICTS DATA AVAILABLE FOR '+state.upper())


# ==================================================U YEAR ANALYSIS ========================================================
with tab3:
    st.write('### :WHITE[TOP User Count by State and District] ')
    col1, col2= st.columns(2)
    with col1:
        state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='Z')
    with col2:
        Y = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020','2021','2022'),key='X')
    y=int(Y)
    s=state

    df_filtered = Data_Top_User_Table[(Data_Aggregated_User_df['Year'] == y)]
    df_filtered3 = df_filtered[(df_filtered['State'] == state)]
    fig = px.bar(df_filtered3, x='District', y='Registered_Users_Count',
                 color="District", title=str(y))
    st.plotly_chart(fig, use_container_width=True)



# ===================================================User OVERALL ANALYSIS ====================================================
    with tab4:
        years=Data_Aggregated_User_Summary_df.groupby('Year')
        years_List=Data_Aggregated_User_Summary_df['Year'].unique()
        years_Table=years.sum()
        del years_Table['Quarter']
        years_Table['year']=years_List
        total_trans=years_Table['Registered_Users'].sum() # this data is used in sidebar    
        fig1 = px.pie(years_Table, values='Registered_Users', names='year',color_discrete_sequence=px.colors.sequential.RdBu, title='TOTAL REGISTERED USERS (2018 TO 2022)')
        col1, col2= st.columns([0.7,0.3])
        with col1:
            #st.write('### :PURPLE[Drastical Increase in Transactions :rocket:]')
            labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
                "Rest of World"]

            # Create subplots: use 'domain' type for Pie subplot
            fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
            fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['Registered_Users'], name="REGISTERED USERS"),
                        1, 1)
            fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['AppOpenings'], name="APP OPENINGS"),
                        1, 2)

            # Use `hole` to create a donut-like pie chart
            fig.update_traces(hole=.6, hoverinfo="label+percent+name")

            fig.update_layout(
                title_text="USERS DATA (2018 TO 2022)",
                # Add annotations in the center of the donut pies.
                annotations=[dict(text='USERS', x=0.18, y=0.5, font_size=20, showarrow=False),
                            dict(text='APP', x=0.82, y=0.5, font_size=20, showarrow=False)])
            # st.plotly_chart(fig1)
            st.plotly_chart(fig)
        with col2:  
            # st.write('#### :PURPLE[Year Wise Transaction Analysis in INDIA]')
            st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)


st.write('# :WHITE[User OverAll Count  ]')

fig= px.bar(Data_Top_User_Table, x="State", y="Registered_Users_Count", color="State",
  animation_frame="Year", animation_group="District", range_y=[0,5000000])


st.plotly_chart(fig, use_container_width=True)

st.write('# TOP 3 STATES DATA')
c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021','2020','2019','2018'),key='y1h2k')
with c2:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qgwe2')
Data_Map_User_df=Data_Aggregated_User_Summary_df.copy()
top_states=Data_Map_User_df.loc[(Data_Map_User_df['Year'] == int(Year)) & (Data_Map_User_df['Quarter'] ==int(Quarter))]
top_states_r = top_states.sort_values(by=['Registered_Users'], ascending=False)
top_states_a = top_states.sort_values(by=['AppOpenings'], ascending=False)

top_states_T=Data_Aggregated_Transaction_df.loc[(Data_Aggregated_Transaction_df['Year'] == int(Year)) & (Data_Aggregated_Transaction_df['Quarter'] ==int(Quarter))]
topst=top_states_T.groupby('State')
x=topst.sum().sort_values(by=['Total_Transactions_count'], ascending=False)
y=topst.sum().sort_values(by=['Total_Amount'], ascending=False)
col1, col2, col3, col4= st.columns([2.5,2.5,2.5,2.5])
with col1:
    rt=top_states_r[1:4]
    st.markdown("#### :WHITE[Registered Users :bust_in_silhouette:]")
    st.markdown(rt[[ 'State','Registered_Users']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
with col2:
    at=top_states_a[1:4]
    st.markdown("#### :WHITE[PhonePeApp Openings:iphone:]")
    st.markdown(at[['State','AppOpenings']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
with col3:
    st.markdown("#### :WHITE[Total Transactions:currency_exchange:]")
    st.write(x[['Total_Transactions_count']][1:4])
with col4:
    st.markdown("#### :WHITE[Total Amount :dollar:]")
    st.write(y['Total_Amount'][1:4])


st.markdown("")
st.write('#### :White[Summary Transaction Analysis in INDIA]')


df_filteredtop = Data_Top_Transaction_Table[(Data_Top_User_Table['Year'] == int(Year))]
df_filteredtop2 = df_filteredtop[(df_filteredtop['Quater'] == int(Quarter))]


fig = px.scatter(df_filteredtop2, x="State", y="Transaction_count", color="District",
                 size='Total_Amount',title=str(Year)+" Quarter-"+str(Quarter))
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True,height=800)
df_filtered = Data_Top_User_Table[(Data_Top_User_Table['Year'] == int(Year))]
df_filtered2 = df_filtered[(df_filtered['Quater'] == int(Quarter))]

st.write('#### :White[Summary User Analysis in INDIA]')
fig = px.scatter(df_filtered2, x="State", y="Registered_Users_Count", color="District",
                 size='Registered_Users_Count',title=str(Year)+" Quarter-"+str(Quarter))
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True,height=800)
