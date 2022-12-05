import app as main
import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

st.markdown("<h1 style='text-align: center; color: #47039f;'>Melbourse Housing Insights</h1><br>", unsafe_allow_html=True)
st.markdown("---")

data = main.loadData()
st.markdown("<h3 style='text-align: center; color: #47039f;'>Number of Houses by Types and Region</h1><br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    # Number of houses according to types
    houseTypes = data['Type'].value_counts().rename_axis('Type').reset_index(name='Number of Houses')
    pieChart = alt.Chart(houseTypes).mark_arc(innerRadius=50,color="purpleredView").encode(
    theta=alt.Theta(field="Number of Houses", type="quantitative"),
    color=alt.Color(field="Type", type="nominal",scale=alt.Scale(scheme='plasma')),
        tooltip=['Number of Houses:Q']
    ).properties(
        width=300,
        height=500,
        title="Number of Houses by Types"
    )
    st.write(pieChart)
        #Number of houses by regions
with col2:
    with st.container():
        region = data['Regionname'].value_counts().rename_axis('Regionname').reset_index(name='Number of Houses')
        barchart = alt.Chart(region).mark_bar().encode(
        x=alt.X("Regionname",sort='-y'),
        y=alt.Y("Number of Houses"),
        tooltip=['Number of Houses:Q'],
        color=alt.Color(field="Number of Houses",type="nominal",scale=alt.Scale(scheme='plasma'),sort= "descending")
        ).properties(
            width=500,
            height=500,
            title="Number of Houses by Regions"
        )
        st.write(barchart)
st.markdown("---")

st.markdown("<h3 style='text-align: center; color: #47039f;'>Mean Price by Month and Suburb</h1><br>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    with st.container():
        lineChart = data.copy()
        lineChart['Date'] =  pd.to_datetime(lineChart['Date'])
        lineChart['Year'] =  pd.to_datetime(lineChart['Date']).dt.strftime('%Y-%m')
        lineChart=lineChart.set_index('Year')
        average_house_value_year = lineChart["Price"].groupby([lineChart.index]).mean().round(2).rename_axis('Year').reset_index(name='Mean Price')
        lineChartC = alt.Chart(average_house_value_year).mark_area(color="plasma",line=True).encode(
            x='Year',
            y='Mean Price',
            tooltip=['Mean Price:Q'],
            color=alt.Color('Mean Price:Q',scale=alt.Scale(scheme='plasma'))
        ).properties(
            width=500,
            height=500,
            title = "Mean Price by Month and Year"
        )
        st.write(lineChartC)
with col4:
    with st.container():
        top_10 = data.copy()
        top_10 = top_10.set_index('Suburb')
        top_10new = top_10["Price"].groupby([top_10.index]).mean().round(2).rename_axis('Suburb').reset_index(name='Price')
        top10Chart = alt.Chart(
            top_10new,
        ).mark_bar().encode(
            x=alt.X('Suburb:N', sort='-y'),
            y=alt.Y('Price:Q'),
            color=alt.Color('Price:Q',scale=alt.Scale(scheme='plasma'),sort= "descending"),
            tooltip=['Price:Q']
        ).transform_window(
            rank='rank(Suburb)',
            sort=[alt.SortField('Suburb', order='ascending')]
        ).transform_filter(
            (alt.datum.rank < 10)
        ).properties(
            width=500,
            height=500,
            title = "Mean Price by Suburb"
        )
        st.write(top10Chart)
st.markdown("---")

with st.container():
    st.markdown("<h3 style='text-align: center; color: #47039f;'>Factors affecting Price</h1><br>", unsafe_allow_html=True)
    base = alt.Chart().mark_point().encode(
    color='Price:Q').properties(
        width=200,
        height=200,
    ).interactive()
    chart = alt.vconcat(data=data)
    for y_encoding in ['Price:Q']:
        row = alt.hconcat()
        for x_encoding in ['Rooms:Q', 'Bedroom2:Q','Car:Q']:
            row |= base.encode(x=x_encoding, y=y_encoding,tooltip=['Price:Q'],color=alt.Color('Price:Q',scale=alt.Scale(scheme='plasma'),sort= "descending"),)
        chart &= row
    st.write(chart)
    base2 = alt.Chart().mark_point().encode(
    color='Price:Q').properties(
        width=200,
        height=200,
    ).interactive()
    chart = alt.vconcat(data=data)
    for y_encoding in ['Price:Q']:
        row = alt.hconcat()
        for x_encoding in ['Distance:Q','BuildingArea:Q','Type:N']:
            row |= base.encode(x=x_encoding, y=y_encoding,tooltip=['Price:Q'],color=alt.Color('Price:Q',scale=alt.Scale(scheme='plasma'),sort= "descending"),)
        chart &= row
    st.write(chart)
st.markdown("---")

with st.container():
    st.markdown("<h3 style='text-align: center; color: #47039f;'>Heat Map</h1><br>", unsafe_allow_html=True)
    corr_matrix = data.corr()
    fig = px.imshow(corr_matrix)
    st.write(fig)

