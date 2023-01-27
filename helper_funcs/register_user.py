import streamlit as st
import streamlit_authenticator as st_auth
from .db import create_user, read_locations
from streamlit_extras.no_default_selectbox import selectbox
import re



# Define a function for
# for validating an Email
def check(email):
    
    # Make a regular expression
    # for validating an Email
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def register(credentials):
    locs = read_locations()["locs"].tolist()

    with st.form("Get Started"):
        st.subheader("Get Started 🧾")
        st.write("Username (Email)")
        new_username = st.text_input(
            "Username (Email)",
            placeholder="Your Email will be used as your username",
            label_visibility="collapsed",
        )
        fcol, lcol = st.columns([1, 1])

        with fcol:
            st.write("First Name")
            first_name = st.text_input(
                "First Name",
                placeholder="Enter your first name",
                label_visibility="collapsed",
            )

        with lcol:
            st.write("Last Name")
            last_name = st.text_input(
                "Last Name",
                placeholder="Enter your last name",
                label_visibility="collapsed",
            )

        pw1, pw2 = st.columns([1, 1])

        with pw1:
            st.write("Password")
            password1 = st.text_input(
                "Password", type="password", label_visibility="collapsed"
            )
        with pw2:
            st.write("Repeat Password")
            password2 = st.text_input(
                "Repeat Password", type="password", label_visibility="collapsed"
            )

        ncol1, ncol2 = st.columns([1, 1])

        with ncol1:
            st.write("**Gender**")
            gender = st.selectbox(
                "Gender",
                options=["M", "F", "Rather Not Say"],
                label_visibility="collapsed",
            )

        with ncol2:
            st.write("**Career Status**")
            status = st.selectbox(
                "status",
                options=[
                    "Student Intern",
                    "Intern Pharmacist/House Officer",
                    "Pharmacist (B. Pharm)",
                    "Pharmacist (PharmD)",
                ],
                label_visibility="collapsed",
            )

        st.write("**Registration Number (PA/HPA)**")
        reg_number = st.number_input(
            "Registration Number",
            value=9999,
            label_visibility="collapsed",
        )

        st.markdown("###")
        st.write("**Add Place(s) of Work**")

        for row in range(2):
            st.markdown("######")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.write(f"Company {row +1}")
                st.text_input(
                    f"Company {row}",
                    label_visibility="collapsed",
                    key=f"Company {row}",
                )

            with col2:
                st.write(f"Town {row +1}")
                selectbox(
                    f"Location {row}",
                    options=locs,
                    label_visibility="collapsed",
                    key=f"Location {row}",
                )

            with col3:
                st.write(f"Category {row +1}")
                st.selectbox(
                    f"Category {row}",
                    options=["", "Hospital", "Community"],
                    label_visibility="collapsed",
                    key=f"Category {row}",
                )

        register = st.form_submit_button("Register")

    if register:
        work_details = {}
        rows = [x for x in range(2) if st.session_state[f"Company {x}"] != ""]

        work_details["company"] = [st.session_state[f"Company {x}"] for x in rows]
        work_details["location"] = [st.session_state[f"Location {x}"] for x in rows]
        work_details["category"] = [st.session_state[f"Category {x}"] for x in rows]
        if (
            len(new_username)
            and len(first_name)
            and len(last_name)
            and len(password1)
            and len(work_details["company"])
            and len(work_details["location"])
            and len(work_details["category"]) > 0
        ):
            if new_username not in credentials["usernames"] and check(new_username):
                if password1 == password2:
                    hashed_pw = st_auth.Hasher([password1])

                    details = {
                        "username": new_username,
                        "email": new_username,
                        "profile": {
                            "first_name": first_name,
                            "last_name": last_name,
                            "gender": gender,
                            "status": status,
                            "reg_number": reg_number,
                            "work_details": work_details,
                        },
                        "name": first_name + " " + last_name,
                        "password": hashed_pw.generate()[0],
                    }

                    create_user(details)
                    return True
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Username can only be a valid Email Address")
        else:
            st.error("Please enter an email, username, name, password and work details")
