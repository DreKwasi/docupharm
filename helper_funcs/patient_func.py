import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_extras.switch_page_button import switch_page
import datetime as dt
from .db import create_patient


def record_details():

    # set_png_as_page_bg("assets/images/Black Man _ Woman Feeling Sick.png")

    placeholder = st.empty()

    with placeholder.container():
        col1, col2, x = st.columns([1, 1, 4])
        col1.markdown(":red[**Oops! I Couldn't Capture The Patient's Details**]")
        if col2.checkbox("No Details", label_visibility="collapsed"):
            st.session_state["disable"] = True
        else:
            st.session_state["disable"] = False

        st.markdown("#### Capture Your Patient's Details To Follow Up On Them.")

        st.image(
            "assets/images/Black Man Feeling Sick.png",
            width=300,
            use_column_width=True,
        )

        st.write("**Full Name**")
        patient_name = st.text_input(
            "Full Name",
            label_visibility="collapsed",
            disabled=st.session_state["disable"],
        )

        st.write("**Phone Number**")
        phone_number = st.text_input(
            "phone_number",
            label_visibility="collapsed",
            disabled=st.session_state["disable"],
        )

        st.write("**Gender**")
        gender = st.selectbox(
            "Gender",
            options=["M", "F", "Rather Not Say"],
            label_visibility="collapsed",
        )

        st.write("**Weight (kg)**")
        weight = st.number_input(
            "Weight",
            label_visibility="collapsed",
            disabled=st.session_state["disable"],
        )

        st.write("**Any Further Details**")
        further_details = st.text_area(
            "Further Details", label_visibility="collapsed"
        )

        submit = st.button("Save")

    if submit:
        details = {
            "patient_name": patient_name,
            "phone_number": phone_number,
            "gender": gender,
            "weight": weight,
            "further_details": further_details,
            "pharmacist": st.session_state["username"],
            "intervention_key": st.session_state["intv_key"],
        }
        create_patient(details)
        st.session_state["intv_key"] = ""
        switch_page("home")

    # if "intv_key" not in st.session_state or st.session_state["intv_key"] == "":
    #     placeholder.empty()
    #     st.warning("Complete An Intervention First")


def view_details():
    holder = st.empty()
    
    with holder.container():
        st.header("All Patient Details")
        date = date_range_picker(
            "Select a Date Range: ",
            default_start=dt.datetime.strptime("2023-01-01", "%Y-%m-%d"),
            min_date=dt.datetime.strptime("2023-01-01", "%Y-%m-%d"),
            max_date=dt.datetime.today(),
        )
        search_box = st.selectbox(
            "Search for Patient Name", options=["All", "Joel Anaman"]
        )

        with st.expander("Mr. Joel Anaman"):
            st.markdown("Too Morch Money")
            edit = st.button("Edit Details", key="editBtn")
            # dict = {"anaman": "key"}

    if edit:
        holder.empty()
        placeholder = st.empty()

        with placeholder.form("Record Intervention"):
            st.markdown("#### Be Up to Date With Your Patients.")

            st.image(
                "assets/images/Black Man Feeling Sick.png",
                width=300,
                use_column_width=True,
            )

            st.write("**Record Date**")
            date = st.date_input("", label_visibility="collapsed")

            st.write("**Full Name**")
            patient_name = st.text_input("Full Name", label_visibility="collapsed")

            st.write("**Phone Number**")
            phone_number = st.text_input("phone_number", label_visibility="collapsed")

            st.write("**Gender**")
            gender = st.selectbox(
                "Gender",
                options=["M", "F", "Rather Not Say"],
                label_visibility="collapsed",
            )

            st.write("**Weight (kg)**")
            intervention = st.number_input("Weight", label_visibility="collapsed")

            st.write("**Any Further Details**")
            intervention_details = st.text_area(
                "Further Details", label_visibility="collapsed"
            )

            form_submit = st.form_submit_button("Submit")

            if form_submit:
                st.balloons()
                # st.experimental_rerun()
