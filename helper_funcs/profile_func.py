import streamlit as st
from .db import read_locations, update_user_profile
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.no_default_selectbox import selectbox



def show_profile():
    
    locs = read_locations()["locs"].tolist()

    st.subheader(st.session_state["profile_header"])
    placeholder = st.empty()
    
    with placeholder.container():

        st.write("**First Name**")
        first_name = st.text_input("First Name", label_visibility="collapsed")

        st.write("**Last Name**")
        last_name = st.text_input("Last Name", label_visibility="collapsed")

        st.write("**Gender**")
        gender = st.selectbox(
            "Gender", options=["M", "F", "Rather Not Say"], label_visibility="collapsed"
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
            "Registration Number", value=9999, label_visibility="collapsed",
            help="Input Number Only"
        )

        st.write("**Company**")
        company1 = st.text_input("Company", label_visibility="collapsed")

        st.write("**Location (Town)**")
        location = selectbox(
            "Location",
            options=locs,
            label_visibility="collapsed",
        )

        st.write("**Category**")
        category = st.selectbox(
            "Category",
            options=["Hospital", "Community Pharmacy"],
            label_visibility="collapsed",
        )
        submit = st.button("Update Profile")

    if submit:
        with st.spinner("Updating Profile"):
            details = {
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "status": status,
                "reg_number": reg_number,
                "company1": company1,
                "location": location,
                "category": category
            }
            update_user_profile(details, st.session_state['username'])
            switch_page("home")
