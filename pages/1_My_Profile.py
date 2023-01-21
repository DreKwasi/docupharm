import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import profile_func
from helper_funcs.styles import read_html, load_css_file
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="auto",
    layout="centered",
)

load_css_file("styles/main.css")


with st.sidebar.empty():
    st.session_state["authenticator"].logout("Logout", "main")


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:
        if st.button(
            "🏡 Go Home",
            disabled=False
            if st.session_state["profile_header"] == "Profile Details"
            else True,
        ):
            switch_page("home")
        profile_func.show_profile()

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
