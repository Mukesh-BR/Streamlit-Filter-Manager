import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered", page_title="Data Editor")
st.title("Alpharoc Filter Manager")


show = st.button("Jump into the application!")
if show:
    switch_page("meta table viewer")
