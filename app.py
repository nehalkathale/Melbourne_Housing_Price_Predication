import streamlit as st
import base64
import pandas as pd
st.markdown("<h1 style='text-align: center; color: #47039f;'>Melbourse Housing</h1><br>", unsafe_allow_html=True)

def run():
    st.set_page_config(
    page_title="Melbourne Housing",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    )

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def loadData():
    data = pd.read_csv('melb_data.csv')
    return data


