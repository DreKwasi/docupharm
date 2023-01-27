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

page_util.delete_page("Home", "Add_My_Intervention")
page_util.delete_page("Home", "Add_My_Patient")

col1, col2, col3 = st.columns([1, 1, 1])

if col1.button("Add Patient"):
    page_util.add_page("Home", "Add_My_Patient")
    switch_page("add my patient")

with col3:
    if st.button("🏡 Go Home"):
        switch_page("home")


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:

        st.sidebar.subheader(f"""DocuPharm \n The #1 Impact Tracker for Pharmacists""")

        with st.sidebar.empty():
            st.session_state["authenticator"].logout("Logout", "main")



        patient_func.view_details()


    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
