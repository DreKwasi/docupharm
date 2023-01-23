import streamlit as st
import streamlit_authenticator as st_auth
from streamlit_option_menu import option_menu
from helper_funcs import db, home_func, styles
from streamlit_extras.switch_page_button import switch_page

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


if st.session_state["username"]:
    if  db.check_profile(st.session_state["username"]):
        st.sidebar.subheader(
            """Welcome to DocuPharm \n The #1 Impact Tracker for Pharmacists"""
        )

        st.header(f'Hello,  {st.session_state["name"]} :grinning:')
        st.session_state["authenticator"] = authenticator
        with st.sidebar.empty():
                authenticator.logout("Logout", "main")
        
        home_func.show_dashboard()
        
    else:
        switch_page("my profile")

else:
    with placeholder.container():
        options = ["Sign In", "Sign Up"]
        selected = option_menu(menu_title="", options=options, orientation="horizontal")
        st.header("Welcome to DocuPharm 🎈🎈🎈")
        st.subheader("The #1 Impact Tracker for Pharmacists 👨‍⚕️👩‍⚕️")

        if "success_message" in st.session_state:
            st.success(st.session_state["success_message"])


    if selected == "Sign In":
        if "refresh" in st.session_state:
            del st.session_state["refresh"]
            
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

            st.session_state["authenticator"] = authenticator

            with st.sidebar.empty():
                authenticator.logout("Logout", "main")
                
            placeholder.empty()
            if st.session_state["username"] and db.check_profile(
                st.session_state["username"]
            ):

                st.sidebar.subheader(
                    """Welcome to DocuPharm \n The #1 Impact Tracker for Pharmacists"""
                )

                st.header(f'Hello,  {st.session_state["name"]} :grinning:')
                home_func.show_dashboard()
                
            else:
                switch_page("my profile")

        elif authentication_status == False:
            st.error("Username/password is incorrect")

        elif authentication_status == None:
            st.warning("Please enter your username and password")

    elif selected == "Sign Up":
        try:
            if authenticator.register_user("Get Started 🧾", preauthorization=False):
                db.create_user(
                    usernames=creds["usernames"],
                )
                st.session_state[
                    "success_message"
                ] = "User registered successfully. Please Log In"
                switch_page("my profile")
        except Exception as e:
            st.error(e)
