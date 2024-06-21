#docker run -it -v "$(pwd):/home/app" -p 4000:4000 jedha/streamlit-fs-image
#docker run -it -v "$(pwd):/home/app" -p 4000:4000 jedha/streamlit-fs-image bash
#docker build . -t NAME_DOCKER
# docker run -it -p 4000:80 -v "$(pwd):/home/app" -e PORT:80 NAME_DOCKER bash

#http://localhost:4000

import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np



DATA_URL = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'

@st.cache_data
def load_data(): 
    data = pd.read_excel(DATA_URL)
    return data

data = load_data()
print('state: ',data['state'].value_counts())

st.markdown("""
    Bienvenue sur ce tableau de bord streamlit du `Projet Get Around`. Nos <a href=DATA_URL style="text-decoration: none;">données</a>
    illustrent quelques statistiques et visualisations de données. A l'aide de cet un outil permet de suivre et comprendre les données des locations de voitures réalisé par
    <a href="https://github.com/2nzi" style="text-decoration: none;">@2nzi</a> sur github.
""", unsafe_allow_html=True)



if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)   


data = data.drop(['time_delta_with_previous_rental_in_minutes','previous_ended_rental_id'],axis=1)

st.subheader("Part des différents types de location")
st.markdown("""
    Deux types de locations existe. Connect & Mobile.
""", unsafe_allow_html=True)

fig = px.pie(data, values='car_id',names='checkin_type')
# fig = go.Figure(data=[go.Pie(labels=data['checkin_type'], values=data['car_id'])])
st.plotly_chart(fig)    



st.subheader("Repartition des locations annulées dans chaque type de commande")
fig = px.histogram(data,x='checkin_type',color='state')
st.plotly_chart(fig)    


col = 'delay_at_checkout_in_minutes'
col_med = data[col].median()
col_std = data[col].std()
lower_bound = col_med - 2 * col_std
upper_bound = col_med + 2 * col_std
print(col_med,lower_bound,upper_bound)
data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
print('state: ',data['state'].value_counts())
#utiliser Q1-1.5IQR et Q3+1.5IQR

if st.checkbox('Show on Late',value=True):
    mini = 0
    df = data[data['delay_at_checkout_in_minutes']>mini]
    title_late = 'Late cars'

else:
    df = data
    title_late = 'All cars'
    mini = int(df['delay_at_checkout_in_minutes'].min())


st.subheader(title_late)
trsh = int(df['delay_at_checkout_in_minutes'].max()) #make the max chossable !
seuil = st.slider("Choose the minute threshold!", mini, int(df['delay_at_checkout_in_minutes'].max()), int(trsh*0.1))
# seuil = st.slider("Choose the minute threshold!", 0, trsh, int(trsh*0.1))

fig_px = px.histogram(df, color='checkin_type', x='delay_at_checkout_in_minutes')
fig = go.Figure(fig_px)

x=seuil
fig.add_shape(
    type="line",
    x0=x, x1=x, y0=0, y1=1,
    line=dict(color="Green", width=2, dash="dash"),
    xref='x', yref='paper'
)

fig.add_shape(
    type="rect",
    x0=mini, x1=x, y0=0, y1=1,
    fillcolor="Green",
    opacity=0.2,
    line_width=0,
    xref='x', yref='paper'
)

fig.update_layout(
    title="",
    xaxis_title="Delay at Checkout in Minutes",
    yaxis_title="Count"
)

st.plotly_chart(fig)  
col1, col2 = st.columns(2)

move_upper_mask = df['delay_at_checkout_in_minutes']<seuil
lower_mask = df['delay_at_checkout_in_minutes']>mini
global_mask = move_upper_mask & lower_mask
col1.metric("Number of rent", len(df[global_mask]))

part_of_rent = 100*len(df[move_upper_mask]) / len(df)
col2.metric("Part of rent", f'{part_of_rent:.2f}%')

# col2.metric("Part of rent", f'{100*len(df[df['delay_at_checkout_in_minutes']<seuil])/len(df['delay_at_checkout_in_minutes']):.2f}%')


#IDEE:
# pouvoir choisir l'id d'une voiture spécifiquement





# day_data = data[data['dateRep']== start_time]



# st.subheader("Analyse par pays")

# country = st.selectbox("Select a country you want to see sales", data["countriesAndTerritories"].sort_values().unique())




# st.write("Current growth rate")

# country_data = data[data["countriesAndTerritories"]==country]

# from random import randrange
# current_day = randrange(len(country_data))
# # current_day = int(len(country_data)/2) #take random value

# # st.write(country_data.iloc[current_day]['dateRep'])
# # st.write(country_data.iloc[current_day]['cases'])
# # st.write(country_data.iloc[current_day-1]['cases'])


# ratio = np.round((country_data.iloc[current_day]['cases'] - country_data.iloc[current_day-1]['cases'])/country_data.iloc[current_day]['cases'],2)
# ratio2 = np.round((country_data.iloc[current_day]['cases'] - country_data.iloc[current_day-2]['cases'])/country_data.iloc[current_day-1]['cases'],2)
# diff_ratio = np.round(ratio-ratio2,2)
# st.metric(label="",value = ratio, delta = diff_ratio)
# # st.write(f'{ratio:.2f}')


# #### Create two columns
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader('Cas positifs cases')
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=data_date["dateRep"], y=data_date["cases"], mode='lines',name='new cases', line=dict(color='blue')))
#     fig.add_trace(go.Scatter(x=data_date["dateRep"], y=data_date["Rolcases"], mode='lines',name='Rolling 7-day Mean',line=dict(color='red')))

#     st.plotly_chart(fig)

# with col2:
#     st.subheader('Cas de décès')
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(x=data_date["dateRep"], y=data_date["deaths"], mode='lines',name='new cases', line=dict(color='blue')))
#     fig2.add_trace(go.Scatter(x=data_date["dateRep"], y=data_date["Roldeaths"], mode='lines',name='Rolling 7-day Mean',line=dict(color='red')))

#     st.plotly_chart(fig2)

            

