import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import intervention_func, page_util
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


col1, col2 = st.columns([2, 1])
if col1.button("View All Interventions"):
    switch_page("my interventions")
    
if col2.button("🏡 Go Home"):
    switch_page("home")


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:
        st.sidebar.subheader(f"""DocuPharm \n The #1 Impact Tracker for Pharmacists""")

        with st.sidebar.empty():
            st.session_state["authenticator"].logout("Logout", "main")

        intervention_func.record_intervention()

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
