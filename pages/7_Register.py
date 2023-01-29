import streamlit as st
import streamlit_authenticator as st_auth
from streamlit_extras.switch_page_button import switch_page
from helper_funcs import db, styles, register_user

import warnings

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
    
st.header("""Welcome to DocuPharm 🎈🎈🎈 \n The #1 Impact Tracker for Pharmacists 👨‍⚕️👩‍⚕️""")
if st.button("Sign In"):
    switch_page("home")
if register_user.register(creds):
    placeholder.success("User registered successfully. Please Log In")
