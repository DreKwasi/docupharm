import streamlit as st
import streamlit_authenticator as st_auth
from streamlit_option_menu import option_menu
from helper_funcs import db, home_func, styles, register_user
from streamlit_extras.switch_page_button import switch_page
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
msg_holder = st.empty()


with placeholder.container():
    options = ["Sign In", "Sign Up"]
    selected = option_menu(menu_title="", options=options, orientation="horizontal")

    st.header("Welcome to DocuPharm 🎈🎈🎈")
    st.subheader("The #1 Impact Tracker for Pharmacists 👨‍⚕️👩‍⚕️")

    if "success_message" in st.session_state:
        st.success(st.session_state["success_message"])

if selected == "Sign In":
    # if "refresh" in st.session_state:
    #     del st.session_state["refresh"]

    name, authentication_status, username = authenticator.login("Sign In", "main")

    if authentication_status:
        (
            st.session_state["name"],
            st.session_state["authentication_status"],
            st.session_state["username"],
        ) = (
            name,
            authentication_status,
            username,
        )
        placeholder.empty()

        if "success_message" in st.session_state:
            del st.session_state["success_message"]

        st.session_state["authenticator"] = authenticator

        st.sidebar.subheader(
            """Welcome to DocuPharm \n The #1 Impact Tracker for Pharmacists"""
        )
        with st.sidebar.empty():
            authenticator.logout("Logout", "main")

        st.header(f'Hello,  {st.session_state["name"]} :grinning:')
        home_func.show_dashboard()

    elif authentication_status == False:
        st.error("Username/password is incorrect")

    elif authentication_status == None:
        st.warning("Please enter your username and password")

elif selected == "Sign Up":
    msg_holder.empty()
    if "success_message" in st.session_state:
        del st.session_state["success_message"]

    if register_user.register(creds):
        st.session_state[
            "success_message"
        ] = "User registered successfully. Please Log In"

        switch_page("my days")
