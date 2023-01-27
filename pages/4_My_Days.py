import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from helper_funcs.styles import load_css_file
from helper_funcs import db


st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="collapsed",
    layout="centered",
)

load_css_file("styles/main.css")

if st.button("🏡 Go Home"):
    switch_page("home")




if "authentication_status" in st.session_state or "username" in st.session_state:

    if db.check_profile(st.session_state['username']):
        st.header("Under Construction 👷")

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")

else:
    switch_page("home")