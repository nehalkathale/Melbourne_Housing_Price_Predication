import streamlit as st
import base64
import pandas as pd

def run():
    st.set_page_config(
    page_title="Melbourne Housing",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.title("Melbourne Housing Price Visualization and Prediction")
bin_str = get_base64_of_bin_file('Home.jpeg')
page_bg_img = '''
<style>
body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
}
</style>
''' % bin_str
st.markdown(page_bg_img, unsafe_allow_html=True)

def loadData():
    data = pd.read_csv('melb_data.csv')
    return data
