import streamlit as st
from .db import read_locations, update_user_profile, get_profile
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox
from .validators import validate_profile

def validate(details):
    work_details = details["work_details"]

    if (
        work_details["category"]
        and work_details["company"]
        and work_details["location"]
    ):
        if details["first_name"] and details["last_name"]:
            return True
        else:
            st.error("First and Last Name Cannot Be Empty")
    else:
        st.error("Kindly Indicate Your Work Details")


def show_profile():
    locs = read_locations()["locs"].tolist()

    error_placehoder = st.empty()
    st.subheader("Profile Details")
    placeholder = st.empty()

    with placeholder.container():
        with st.form("Profile Form"):

            st.write("**First Name**")
            first_name = st.text_input("First Name", label_visibility="collapsed")

            st.write("**Last Name**")
            last_name = st.text_input("Last Name", label_visibility="collapsed")

            st.write("**Gender**")
            gender = st.selectbox(
                "Gender",
                options=["M", "F", "Rather Not Say"],
                label_visibility="collapsed",
            )

            st.write("**Status**")
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

            for row in range(3):
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

            submit = st.form_submit_button("Update Profile")

    if submit:
        with st.spinner("Updating Profile"):
            work_details = {}
            rows = [x for x in range(3) if st.session_state[f"Company {x}"] != ""]

            work_details["company"] = [st.session_state[f"Company {x}"] for x in rows]
            work_details["location"] = [st.session_state[f"Location {x}"] for x in rows]
            work_details["category"] = [st.session_state[f"Category {x}"] for x in rows]

            details = {
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "status": status,
                "reg_number": reg_number,
                "work_details": work_details,
            }
            if validate(details):
                update_user_profile(details, st.session_state["username"])
                switch_page("home")

    else:
        st.stop()


def update_profile():
    locs = read_locations()["locs"].tolist()
    curr_profile = get_profile(st.session_state["username"])
    status_list = [
        "Student Intern",
        "Intern Pharmacist/House Officer",
        "Pharmacist (B. Pharm)",
        "Pharmacist (PharmD)",
    ]
    status_list.remove(curr_profile["status"])
    status_list.insert(0, curr_profile["status"])

    gender_list = ["M", "F", "Rather Not Say"]
    gender_list.remove(curr_profile["gender"])
    gender_list.insert(0, curr_profile["gender"])

    st.subheader('Profile Details')
    placeholder = st.empty()

    with placeholder.container():
        with st.form("Profile Form"):

            st.write("**First Name**")
            first_name = st.text_input(
                "First Name",
                value=curr_profile["first_name"],
                label_visibility="collapsed",
            )

            st.write("**Last Name**")
            last_name = st.text_input(
                "Last Name",
                value=curr_profile["last_name"],
                label_visibility="collapsed",
            )

            st.write("**Gender**")
            gender = st.selectbox(
                "Gender",
                options=gender_list,
                label_visibility="collapsed",
            )

            st.write("**Status**")
            status = st.selectbox(
                "status",
                options=status_list,
                label_visibility="collapsed",
            )

            st.write("**Registration Number (PA/HPA)**")
            reg_number = st.number_input(
                "Registration Number",
                value=9999
                if curr_profile["reg_number"] == ""
                else int(curr_profile["reg_number"]),
                label_visibility="collapsed",
            )

            st.markdown("###")
            st.write("**Add Place(s) of Work**")

            work_num = len(curr_profile["work_details"]["company"])
            for row in range(work_num):
                st.markdown("######")

                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    st.write(f"Company {row +1}")
                    st.text_input(
                        f"Company {row}",
                        label_visibility="collapsed",
                        value=curr_profile["work_details"]["company"][row],
                        key=f"Company {row}",
                    )

                with col2:
                    st.write(f"Town {row +1}")
                    selectbox(
                        f"Location {row +1}",
                        no_selection_label=curr_profile["work_details"]["location"][
                            row
                        ],
                        options=locs,
                        label_visibility="collapsed",
                        key=f"Location {row}",
                    )

                with col3:
                    st.write(f"Category {row +1}")
                    cat = ["", "Hospital", "Community"]
                    cat.remove(curr_profile["work_details"]["category"][row])
                    cat.insert(0, curr_profile["work_details"]["category"][row])
                    st.selectbox(
                        f"Category {row}",
                        options=cat,
                        label_visibility="collapsed",
                        key=f"Category {row}",
                    )

            for row in range(work_num, (4 - work_num) + 1):
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

            submit = st.form_submit_button("Update Profile")

    if submit:
        with st.spinner("Updating Profile"):
            work_details = {}
            rows = [x for x in range(3) if st.session_state[f"Company {x}"] != ""]

            work_details["company"] = [st.session_state[f"Company {x}"] for x in rows]
            work_details["location"] = [st.session_state[f"Location {x}"] for x in rows]
            work_details["category"] = [st.session_state[f"Category {x}"] for x in rows]

            details = {
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "status": status,
                "reg_number": reg_number,
                "work_details": work_details,
            }
            update_user_profile(details, st.session_state["username"])
            switch_page("home")

    else:
        st.stop()
