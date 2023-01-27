import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import intervention_func, db
from helper_funcs.styles import load_css_file
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="collapsed",
    layout="centered",
)


# st.session_state["refresh"] = "not refresh"
# st.experimental_set_query_params(curr_page="my intervention")

load_css_file("styles/main.css")


col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏡 Go Home"):
        switch_page("home")

selected = option_menu(
    menu_title="",
    options=["Add Intervention", "All Interventions"],
    orientation="horizontal",
    default_index=0,
)


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:

        st.sidebar.subheader(f"""DocuPharm \n The #1 Impact Tracker for Pharmacists""")

        with st.sidebar.empty():
            st.session_state["authenticator"].logout("Logout", "main")

        if selected == "Add Intervention":
            intervention_func.record_intervention()

        elif selected == "All Interventions":
            intervention_func.view_intervention()

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
