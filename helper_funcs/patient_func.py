import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_extras.switch_page_button import switch_page
import datetime as dt
from .db import create_patient, get_all_patients, update_patient
from streamlit_toggle import st_toggle_switch
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
import pandas as pd
from st_aggrid.grid_options_builder import GridOptionsBuilder


def record_details():

    # set_png_as_page_bg("assets/images/Black Man _ Woman Feeling Sick.png")

    placeholder = st.empty()

    with placeholder.container():
        col1, col2, x = st.columns([1, 1, 4])
        col1.markdown(":red[**Oops! I Couldn't Capture Patient's Details**]")
        with col2:
            if st_toggle_switch(
                active_color="#c98191", track_color="#06141a", label_after=True
            ):
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
        further_details = st.text_area("Further Details", label_visibility="collapsed")

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
    #       if st.button("Goto Intervention"):
    # switch_page("my intervention")


def view_details():
    st.info("Select the Checkbox of the Corresponding Patient to Edit")
    msg = st.empty()
    placeholder = st.empty()
    form_holder = st.empty()
    patient_data = {}

    with placeholder.container():
        st.subheader("All Patient Details")
        df = get_all_patients()
        required_cols = df.columns.tolist()
        required_cols = [x for x in required_cols if x not in ["intervention_key", "key"]]
        grid_df = df.loc[:, required_cols]

        gd = GridOptionsBuilder.from_dataframe(grid_df)
        gd.configure_pagination(
            enabled=True, paginationAutoPageSize=False, paginationPageSize=5
        )
        gd.configure_default_column(editable=False, groupable=True)
        gd.configure_selection(selection_mode="single", use_checkbox=True)
        gridoptions = gd.build()
        new_df = AgGrid(
            df,
            height=300,
            gridOptions=gridoptions,
            GridUpdateMode=GridUpdateMode.SELECTION_CHANGED,
            theme="material",
            enable_enterprise_modules=False,
        )
    try:
        patient_data = new_df["selected_rows"][0]
    except IndexError:
        patient_data = {}

    if patient_data:
        with form_holder.form("Edit Details"):
            st.subheader(f"Edit Details (Patient {patient_data['Patient ID']})")
            gender_options = ["M", "F", "Rather Not Say"]
            
            if patient_data["Gender"] != "":
                gender_options.remove(patient_data["Gender"])
                gender_options.insert(0, patient_data["Gender"])


            if patient_data["Gender"] == "M":
                st.image(
                    "assets/images/Black Man Feeling Sick.png",
                    width=300,
                    use_column_width=True,
                )
            elif patient_data["Gender"] == "F":
                st.image(
                    "assets/images/Black Woman Feeling Sick.jpg",
                    width=300,
                    use_column_width=True,
                )

            else:
                st.image(
                    "assets/images/Black Woman Feeling Sick.jpg",
                    width=300,
                    use_column_width=True,
                )
                
            st.write("**Full Name**")
            patient_name = st.text_input(
                "Full Name",
                value=patient_data["Patient Name"],
                label_visibility="collapsed",
            )

            st.write("**Phone Number**")
            phone_number = st.text_input(
                "phone_number",
                value=patient_data["Phone Number"],
                label_visibility="collapsed",
                max_chars=10
            )

            st.write("**Gender**")
            gender = st.selectbox(
                "Gender",
                options=gender_options,
                label_visibility="collapsed",
            )

            st.write("**Weight (kg)**")
            weight = st.number_input(
                "Weight",
                value=0 if patient_data["Weight (kg)"] == "" else patient_data["Weight (kg)"],
                label_visibility="collapsed",
            )

            st.write("**Any Further Details**")
            further_details = st.text_area(
                "Further Details",
                value=patient_data["Further Details"],
                label_visibility="collapsed",
            )

            submit = st.form_submit_button("Submit")

        if submit:
            form_holder.empty()
            placeholder.empty()
            details = {
                "patient_id": patient_data["Patient ID"],
                "patient_name": patient_name,
                "phone_number": phone_number,
                "gender": gender,
                "weight": weight,
                "further_details": further_details,
                "pharmacist": st.session_state["username"],
            }
            filtered_details = {
                key:value for key,value in details.items() if value != ""
            }
            with st.spinner("Updating User Details"):
                update_patient(
                    filtered_details,
                    key=df["key"][df["Patient ID"] == patient_data["Patient ID"]],
                )
            
            st.experimental_rerun()

    #     date = date_range_picker(
    #         "Select a Date Range: ",
    #         default_start=dt.datetime.strptime("2023-01-01", "%Y-%m-%d"),
    #         min_date=dt.datetime.strptime("2023-01-01", "%Y-%m-%d"),
    #         max_date=dt.datetime.today(),
    #     )

    # if edit:
    #     holder.empty()
    #     placeholder = st.empty()

    #     with placeholder.form("Record Intervention"):
    #
