import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import profile_func
from helper_funcs.styles import load_css_file


st.set_page_config(
    page_title="Form",
    page_icon="📋",
    initial_sidebar_state="auto",
    layout="centered",
)

if "intv_key" in st.session_state:
    del st.session_state["intv_key"]

# st.session_state['refresh'] = 0
# st.experimental_set_query_params(curr_page="my profile")
load_css_file("styles/main.css")


if "authentication_status" in st.session_state or "username" in st.session_state:

    if st.session_state["authentication_status"]:
        
        st.sidebar.subheader(
            f"""DocuPharm \n The #1 Impact Tracker for Pharmacists"""
        )

        with st.sidebar.empty():
            st.session_state["authenticator"].logout("Logout", "main")


        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🏡 Go Home", disabled=False):
                switch_page("home")

        profile_func.update_profile()
        

    elif st.session_state["authentication_status"] == False:
        switch_page("home")

    elif st.session_state["authentication_status"] == None:
        switch_page("home")


else:
    switch_page("home")
