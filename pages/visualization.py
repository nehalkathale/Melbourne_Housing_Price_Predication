import streamlit as st
import pandas as pd
import melbourneHousing as main
data = main.loadData()
with st.sidebar:
    Suburblist = data.Suburb.unique().tolist()
    numberOfBedrooms = data.Bedroom2.unique()
    suburbList = st.selectbox('Select Suburb',(Suburblist))
    bedroomList = st.selectbox('Select Bedroom',(numberOfBedrooms))