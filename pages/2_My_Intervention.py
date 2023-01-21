import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import intervention_func, db
from helper_funcs.styles import load_css_file



st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="expanded",
    layout="centered",
)

load_css_file("styles/main.css")

if st.button("🏡 Go Home"):
    switch_page("home")

selected = option_menu(
    menu_title="",
    options=["Add Intervention", "View & Update Interventions"],
    orientation="horizontal",
)


if "authentication_status" in st.session_state or "username" in st.session_state:


    if st.session_state["authentication_status"]:

        if db.check_profile(st.session_state["username"]):
            if selected == "Add Intervention":
                intervention_func.record_intervention()

            elif selected == "View & Update Interventions":
                intervention_func.view_intervention()
        else:
            switch_page("my profile")


        with st.sidebar.empty():
            st.session_state["authenticator"].logout("Logout", "main")

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
