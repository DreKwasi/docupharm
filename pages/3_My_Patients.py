import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import patient_func, styles, db


st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="collapsed",
    layout="centered",
)

styles.load_css_file("styles/main.css")

# col1, col2 = st.columns([1, 1])

# with col1:
if st.button("🏡 Go Home"):
    switch_page("home")

# with col2:
#     if st.button("Refresh"):
#         st.experimental_rerun()
#         st.ex

selected = option_menu(
    menu_title="",
    options=["Add Patient Details", "View & Update Patient Details"],
    orientation="horizontal",
)


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:

        if db.check_profile(st.session_state["username"]):
            if selected == "Add Patient Details":
                patient_func.record_details()

            elif selected == "View & Update Patient Details":
                patient_func.view_details()
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
