import streamlit as st
import streamlit_authenticator as st_auth
from .db import create_user


def register(credentials):
    with st.form("Get Started"):
        st.subheader("Get Started 🧾")
        st.write("Username (Email)")
        new_username = st.text_input(
            "Username (Email)",
            placeholder="Your Email will be used as your username",
            label_visibility="collapsed",
        )
        st.write("First Name")
        first_name = st.text_input(
            "First Name",
            placeholder="Enter your first name",
            label_visibility="collapsed",
        )
        st.write("Last Name")
        last_name = st.text_input(
            "Last Name",
            placeholder="Enter your last name",
            label_visibility="collapsed",
        )
        st.write("Password")
        password1 = st.text_input(
            "Password", type="password", label_visibility="collapsed"
        )
        st.write("Repeat Password")
        password2 = st.text_input(
            "Repeat Password", type="password", label_visibility="collapsed"
        )

        register = st.form_submit_button("Register")

    if register:
        if (
            len(new_username)
            and len(first_name)
            and len(last_name)
            and len(password1) > 0
        ):
            if new_username not in credentials["usernames"]:
                if password1 == password2:
                    if new_username in preauthorized_emails:
                        hashed_pw = st_auth.Hasher([password1])

                        details = {
                            "username": new_username,
                            "email": new_username,
                            "first_name": first_name,
                            "last_name": last_name,
                            "name": first_name + " " + last_name,
                            "password": hashed_pw.generate()[0],
                        }

                        create_user(details)
                        return True
                    else:
                        st.error("User not pre-authorized to register")
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Username/Email already taken")
        else:
            st.error("Please enter an email, username, name, and password")
