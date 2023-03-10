import streamlit as st
import streamlit_authenticator as st_auth
from helper_funcs import db, home_func, styles, page_util
import warnings
from streamlit_extras.switch_page_button import switch_page


warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="DocuPharm",
    page_icon="🦈",
    initial_sidebar_state="collapsed",
    layout="centered",
)

styles.load_css_file("styles/main.css")

user_creds = db.get_all_user_details()
cookie = st.secrets["cookie"]
creds = {"usernames": user_creds}
preauth = st.secrets["preauth"]

authenticator = st_auth.Authenticate(
    credentials=creds,
    cookie_name=cookie["name"],
    preauthorized=preauth["emails"],
    key=cookie["key"],
    cookie_expiry_days=cookie["expiry_days"],
)

placeholder = st.empty()



name, authentication_status, username = authenticator.login("Sign In", "main")

if authentication_status:
    page_util.delete_page("Home", "Register")
    page_util.add_page("Home", "My_Profile")
    page_util.add_page("Home", "My_Interventions")
    page_util.add_page("Home", "Add_My_Intervention")
    page_util.add_page("Home", "My_Patients")
    page_util.add_page("Home", "Add_My_Patient")
    page_util.add_page("Home", "My_Days")

    (
        st.session_state["name"],
        st.session_state["authentication_status"],
        st.session_state["username"],
    ) = (
        name,
        authentication_status,
        username,
    )

    st.session_state["authenticator"] = authenticator

    st.sidebar.subheader(
        """Welcome to DocuPharm \n The #1 Impact Tracker for Pharmacists"""
    )
    with st.sidebar.empty():
        authenticator.logout("Logout", "main")

    st.header(f'Hello,  {st.session_state["name"]} :grinning:')
    home_func.show_dashboard()

elif authentication_status == False:
    if st.button("Create An Account"):
        switch_page("Register")
    placeholder.header(
        """Welcome to DocuPharm 🎈🎈🎈 \n The #1 Impact Tracker for Pharmacists 👨‍⚕️👩‍⚕️"""
    )

    page_util.add_page("Home", "Register")
    page_util.delete_page("Home", "My_Profile")
    page_util.delete_page("Home", "My_Interventions")
    page_util.delete_page("Home", "Add_My_Intervention")
    page_util.delete_page("Home", "My_Patients")
    page_util.delete_page("Home", "Add_My_Patients")
    page_util.delete_page("Home", "My_Days")

    st.error("Username/password is incorrect")

elif authentication_status == None:
    if st.button("Create An Account"):
        switch_page("Register")
    placeholder.header(
        """Welcome to DocuPharm 🎈🎈🎈 \n The #1 Impact Tracker for Pharmacists 👨‍⚕️👩‍⚕️"""
    )

    page_util.add_page("Home", "Register")
    page_util.delete_page("Home", "My_Profile")
    page_util.delete_page("Home", "My_Interventions")
    page_util.delete_page("Home", "Add_My_Intervention")
    page_util.delete_page("Home", "My_Patients")
    page_util.delete_page("Home", "Add_My_Patients")
    page_util.delete_page("Home", "My_Days")

    st.warning("Please enter your username and password")
