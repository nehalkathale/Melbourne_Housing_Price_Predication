import streamlit as st
import pandas as pd
import app as main
import altair as alt
import plotly.express as px

data = main.loadData() 
st.markdown("<h1 style='text-align: center; color: #47039f;'>Melbourse Housing Visualization</h1><br>", unsafe_allow_html=True)

#Display map and Prices
url_geojson = 'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/melbourne.geojson'
data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='features',type='json'))
dataSet = data.groupby('Suburb',as_index=False).sum()
# chart object
geoChart = alt.Chart(data_geojson_remote).mark_geoshape(
).project(
    type='identity', reflectY=True
).transform_lookup(
    lookup='properties.name',
    from_=alt.LookupData(dataSet, 'Suburb', ['Suburb','Price'])).encode(
    tooltip=['Price:Q','Suburb:N'],color=alt.Color('Price:Q',scale=alt.Scale(scheme='plasma'),sort= "descending")).properties(
    width=600,
    height=400,
)
geoChart
st.markdown("---")

#Display price distribution for selected suburb according to building area and Rooms
Suburblist = data.Suburb.unique().tolist()
suburbList = st.selectbox('Select Suburb',Suburblist,0)
dfList = data.copy()
dfList['Date'] =  pd.to_datetime(dfList['Date'])
dfList['year'] = dfList['Date'].dt.year
dfList = dfList[dfList['Suburb']==suburbList]
fig = px.scatter(dfList,x="Landsize",y="Rooms",color="Price",size='Price')
fig.update_layout(width=800)
st.write(fig)
st.markdown("---")


#Display bar chart for price according to Bedroom and Bath room According to Suburb
numberOfBedrooms = data.Bedroom2.unique()
numberOfBathRooms = data.Bathroom.unique()
numberOfBedroomsSlider = st.slider("Number of Bedrooms",int(numberOfBedrooms.min()),int(numberOfBedrooms.max()),int(numberOfBedrooms.min()))
numberOfBathRoomsSlider = st.slider("Number of BathRooms",int(numberOfBathRooms.min()),int(numberOfBathRooms.max()),int(numberOfBathRooms.min()))
dfListRoom = data.query("Bedroom2 == @numberOfBedroomsSlider & Bathroom == @numberOfBathRoomsSlider")
fig2 = px.line(dfListRoom, x="Suburb", y="Price", title='Price According to Bedroom and Bath room According to Suburb')
fig2.update_layout(width=800)
st.write(fig2)
st.markdown("---")


