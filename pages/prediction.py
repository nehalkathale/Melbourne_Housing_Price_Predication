import pickle
import streamlit as st
import pandas as pd
import melbourneHousing as main
import tensorflow as tf
import datetime
st.markdown("<h1 style='text-align: center; color: #47039f;'>Melbourse Housing Price Prediction</h1><br>", unsafe_allow_html=True)

d = main.loadData()


def custom_loss_function(y_true, y_pred):
    y_diff = tf.abs(tf.math.log(1+y_true) - tf.math.log(1+y_pred))
    return tf.reduce_sum(tf.square(y_diff)) / tf.cast(tf.size(y_diff), tf.float32)


# Load the model
model = tf.keras.models.load_model('Model1.h5', custom_objects={
                                   'custom_loss_function': custom_loss_function})
model2 = tf.keras.models.load_model('Model2.h5', custom_objects={
                                    'custom_loss_function': custom_loss_function})

# Load mappings pickle
with open('mappings.pkl', 'rb') as f:
    mappings = pickle.load(f)


def format_numeric_label(label):
    return str(int(label))


sample_data = {
    'Suburb': st.selectbox('Suburb', mappings['Suburb']),
    'Rooms': st.slider('Rooms', 1, 8, 3),
    'Type': st.selectbox('Type', mappings['Type']),
    'SellerG': st.selectbox('SellerG', mappings['SellerG']),
    'Distance': st.slider('Distance', 0.0, 50.0, 10.0),
    'Bedroom2': st.slider('Bedroom2', 1, 20, 3),
    'Bathroom': st.slider('Bathroom', 1, 10, 2),
    'Car': st.slider('Car', 0, 10, 2),
    'Landsize': st.slider('Landsize', 0.0, 5000.0, 500.0),
    'BuildingArea': st.slider('BuildingArea', 0.0, 2000.0, 200.0),
    'YearBuilt': st.selectbox('YearBuilt', mappings['YearBuilt'], format_func=format_numeric_label),
    'CouncilArea': st.selectbox('CouncilArea', mappings['CouncilArea']),
    'Regionname': st.selectbox('Regionname', mappings['Regionname']),
}
data = pd.DataFrame(sample_data, index=[0])

categorical_cols = ['Suburb', 'Type', 'SellerG',
                    'Regionname', 'CouncilArea', 'Rooms', 'YearBuilt']

# Use mappings to convert categorical to numerical
for col in data.columns:
    if col in categorical_cols:
        data[col] = data[col].map(mappings[col])

pred1 = model.predict(data)
pred2 = model2.predict(data)

st.write('Predicted Price using Model 1: $', "{:,}".format(pred1[0][0]))
st.write('Predicted Price using Model 2: $', "{:,}".format(pred2[0][0]))
