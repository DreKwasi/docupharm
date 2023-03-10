import streamlit as st

# from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_extras.switch_page_button import switch_page
from .db import create_patient, get_all_patients, update_patient
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from .validators import validate_patient


def view_details(intv_key=None):
    st.info("Select Patient to Edit (Headings Are Searchable)")
    error_placeholder = st.empty()

    placeholder = st.empty()
    form_holder = st.empty()
    patient_data = {}

    with st.spinner("Loading..."):
        with placeholder.expander("**All Patients Details**", expanded=True):
            df = get_all_patients()
            required_cols = df.columns.tolist()
            required_cols = [
                x for x in required_cols if x not in ["intervention_key", "key"]
            ]
            grid_df = df.loc[:, required_cols]

            gd = GridOptionsBuilder.from_dataframe(grid_df)
            gd.configure_pagination(
                enabled=True, paginationAutoPageSize=False, paginationPageSize=7
            )
            gd.configure_default_column(
                editable=False, groupable=True, min_column_width=1
            )
            gd.configure_selection(selection_mode="single", use_checkbox=True)
            gridoptions = gd.build()
            new_df = AgGrid(
                df,
                height=300,
                gridOptions=gridoptions,
                GridUpdateMode=GridUpdateMode.SELECTION_CHANGED,
                theme="balham",
                enable_enterprise_modules=False,
            )
    try:
        patient_data = new_df["selected_rows"][0]
    except IndexError:
        patient_data = {}

    if patient_data:
        with form_holder.form("Edit Details"):
            st.subheader(f"Edit Patient {patient_data['Patient ID']}'s Details")
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
                max_chars=10,
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
                value=0
                if patient_data["Weight (kg)"] == ""
                else patient_data["Weight (kg)"],
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
                key: value for key, value in details.items() if value != ""
            }
            with st.spinner("Updating User Details ..."):
                if validate_patient(details, error_placeholder, no_details=True):
                    update_patient(
                        filtered_details,
                        key=df["key"][df["Patient ID"] == patient_data["Patient ID"]],
                        intv_key=intv_key,
                    )
                    switch_page("my interventions")
                    

            st.experimental_rerun()


def record_details():

    # set_png_as_page_bg("assets/images/Black Man _ Woman Feeling Sick.png")
    error_placeholder = st.empty()

    update, add = st.columns([1, 1])
    placeholder = st.empty()

    if "intv_key" not in st.session_state or st.session_state["intv_key"] == "":
        st.warning("Complete An Intervention First")
        if st.button("Goto Intervention"):
            switch_page("my interventions")

    elif add.checkbox("Add New Patient"):
        with placeholder.container():
            col1, col2, x = st.columns([1, 1, 4])
            col1.markdown(":red[**Oops! I Couldn't Capture Patient's Details**]")
            with col2:
                if st.checkbox("No Details", label_visibility="collapsed"):
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
                max_chars=10,
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
                step=2,
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
                    "intervention_key": [st.session_state["intv_key"]],
                }
                if validate_patient(
                    details, no_details=st.session_state["disable"]
                ):
                    create_patient(details)
                else:
                    st.stop()
    elif update.checkbox("Update Existing Patient"):
        view_details(st.session_state["intv_key"])
