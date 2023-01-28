import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import patient_func, styles, page_util
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="collapsed",
    layout="centered",
)


# st.session_state['refresh'] = 0
# st.experimental_set_query_params(curr_page="my patients")

styles.load_css_file("styles/main.css")

col1, col2 = st.columns([2, 1])

if col1.button("View All Patients"):
    switch_page("my patients")

if col2.button("🏡 Go Home"):
    switch_page("home")


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:

        st.sidebar.subheader(f"""DocuPharm \n The #1 Impact Tracker for Pharmacists""")

        with st.sidebar.empty():
            st.session_state["authenticator"].logout("Logout", "main")

        patient_func.record_details()

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
