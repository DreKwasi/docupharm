import streamlit as st

# import base64
from streamlit_extras.switch_page_button import switch_page
import datetime as dt
from streamlit_extras.mandatory_date_range import date_range_picker
from .db import (
    read_products,
    create_intervention,
    update_intervention,
    get_patient,
    update_patient,
    read_interventions,
    get_profile,
    get_all_intvs,
)
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from .validators import validate_intervention
from . import page_util
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = (
#         """
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-repeat: no-repeat;
#     background-position: top left;
#     }
#     </style>
#     """
#         % bin_str
#     )

#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return


# def return_care(x):
#     return x


def record_intervention():
    # set_png_as_page_bg("assets/images/Black Man _ Woman Feeling Sick.png")

    all_intvs = read_interventions()
    curr_profile = get_profile(st.session_state["username"])
    
    placeholder = st.empty()
    if len(curr_profile["work_details"]["company"]) > 0:
        with placeholder.container():
            st.markdown("#### Only 7-star Pharmacists Lead Interventions. Kudos!!")

            st.image(
                "assets/images/Black Man _ Woman Feeling Sick.png",
                width=300,
                use_column_width=True,
            )

            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("**Where Did You Record This Intervention?**")
                company = st.selectbox(
                    "Where did you record this?",
                    options=curr_profile["work_details"]["company"],
                    label_visibility="collapsed",
                )

            with col2:
                st.write("**When Did You Record This Intervention**")
                date = st.date_input("date", label_visibility="collapsed")

            st.write("**Select The Pharmaceutical Care**")
            pharma_care_type = st.selectbox(
                "Pharma Care Type", options=all_intvs.keys(), label_visibility="collapsed"
            )

            st.write("**Provide More Details**")
            pharma_care_details = st.multiselect(
                "Pharma Details",
                options=all_intvs[pharma_care_type]["reason"],
                label_visibility="collapsed",
            )

            st.write("**Select Medications Involved**")
            medications = st.multiselect(
                "Medications",
                options=read_products()["Products"].tolist(),
                label_visibility="collapsed",
            )

            st.write("**What Was Your Intervention**")
            intervention = st.multiselect(
                "Intervention",
                options=all_intvs[pharma_care_type]["solution"],
                label_visibility="collapsed",
            )

            st.write("**Provide More Details**")
            intervention_details = st.text_area(
                "More Details", label_visibility="collapsed"
            )
            if st.button("Save and Continue"):

                details = {
                    "intervention_id": "",
                    "recorded_date": date.strftime("%Y-%m-%d"),
                    "pharmaceutical_care": pharma_care_type,
                    "pharmaceutical_care_details": pharma_care_details,
                    "medications": medications,
                    "company": company,
                    "intervention": intervention,
                    "intervention_details": intervention_details if intervention != None else "None",
                    "pharmacist": st.session_state["username"],
                }
                if validate_intervention(details):
                    st.session_state["intv_key"] = create_intervention(
                        details, st.session_state["username"]
                    )
                    st.session_state["add_patient"] = True
                    page_util.add_page("Home", "Add_My_Patients")
                    
                    switch_page("add my patients")
            else:
                st.stop()
    else:
        st.error("Complete Your Profile First")
        if st.button("Complete My Profile"):
            switch_page("my profile")

def reset_button():
    st.session_state["p"] = False


def view_intervention():

    curr_profile = get_profile(st.session_state["username"])
    all_intvs = read_interventions()

    st.info("Select the Patient/Intervention to Edit (Headings are Searchable)")
    
    error_placeholder = st.empty()
    placeholder = st.empty()
    top_page = st.empty()
    form_holder = st.empty()

    with st.spinner("Loading..."):
        with placeholder.expander("**All Interventions**", expanded=True):

            # st.subheader("All Patient Details")
            df, intvs_list = get_all_intvs(st.session_state["username"])

            gd = GridOptionsBuilder.from_dataframe(df)
            gd.configure_pagination(
                enabled=True, paginationAutoPageSize=False, paginationPageSize=7
            )
            gd.configure_default_column(editable=False, groupable=True)
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
        intv_data = new_df["selected_rows"][0]
    except IndexError:
        intv_data = {}

    with top_page.empty():
        check1, check2 = st.columns([1, 1])

    if intv_data:
        filtered_intv = [
            x
            for x in intvs_list
            if x["intervention_id"] == intv_data["Intervention ID"]
        ][0]
        
        with check1:
            update_patient_details = st.checkbox(label="Update Patient's Details")
        
        if "patient_key" not in filtered_intv:
            with check2:
                add_patient_details = st.button(label="Forgot to Add A Patient?")

        if not update_patient_details:

            with form_holder.container():
                st.markdown("#### Missed Something? Update Your Intervention Here!!")

                st.image(
                    "assets/images/Black Man _ Woman Feeling Sick.png",
                    width=300,
                    use_column_width=True,
                )

                col1, col2 = st.columns([1, 1])
                comps = curr_profile["work_details"]["company"]
                comps.remove(filtered_intv["company"])
                comps.insert(0, filtered_intv["company"])

                with col1:
                    st.write("**Where Did You Record This Intervention?**")
                    company = st.selectbox(
                        "Where did you record this?",
                        options=comps,
                        label_visibility="collapsed",
                    )

                with col2:
                    st.write("**When Did You Record This Intervention**")
                    date = st.date_input("date", label_visibility="collapsed")

                pharma_care_list = list(all_intvs.keys())

                try:
                    pharma_care_list.remove(filtered_intv["pharmaceutical_care"])
                    pharma_care_list.insert(0, filtered_intv["pharmaceutical_care"])

                except ValueError:
                    pass

                st.write("**Select The Pharmaceutical Care**")
                pharma_care_type = st.selectbox(
                    "Pharma Care Type",
                    options=pharma_care_list,
                    label_visibility="collapsed",
                )

                st.write("**Provide More Details**")

                all_reasons = (
                    all_intvs[pharma_care_type]["reason"] if pharma_care_type else None
                )

                default_details = [
                    x
                    for x in filtered_intv["pharmaceutical_care_details"]
                    if x in all_reasons
                ]

                pharma_care_details = st.multiselect(
                    "Pharma Details",
                    options=all_reasons,
                    label_visibility="collapsed",
                    default=default_details if default_details != [] else None,
                )

                st.write("**Select Medications Involved**")
                medications = st.multiselect(
                    "Medications",
                    options=read_products()["Products"].tolist(),
                    label_visibility="collapsed",
                    default=filtered_intv["medications"]
                    if filtered_intv["medications"] != ""
                    else None,
                )

                st.write("**What Was Your Intervention**")

                all_solutions = (
                    all_intvs[pharma_care_type]["solution"]
                    if pharma_care_type
                    else None
                )

                default_solutions = [
                    x for x in filtered_intv["intervention"] if x in all_solutions
                ]

                intervention = st.multiselect(
                    "Intervention",
                    options=all_solutions,
                    label_visibility="collapsed",
                    default=default_solutions,
                )

                st.write("**Provide More Details**")
                intervention_details = st.text_area(
                    "More Details",
                    value=filtered_intv["intervention_details"] if "intervention_details" in filtered_intv else "",
                    label_visibility="collapsed",
                )

                if st.button("Update Intervention"):

                    details = {
                        "recorded_date": date.strftime("%Y-%m-%d"),
                        "pharmaceutical_care": pharma_care_type,
                        "pharmaceutical_care_details": pharma_care_details,
                        "medications": medications,
                        "company": company,
                        "intervention": intervention,
                        "details": intervention_details if intervention != None else "None",
                        "pharmacist": st.session_state["username"],
                    }
                    if validate_intervention(details, error_placeholder):
                        update_intervention(details, filtered_intv["key"])
                        st.experimental_rerun()
                    else:
                        st.stop()



        elif update_patient_details:
            try:
                patient_data = get_patient(filtered_intv["patient_key"])
            except KeyError:
                st.error("There is No Patient Attached to this Intervention")
                st.stop()

            with st.form("Edit Details"):

                st.subheader(f"Edit Patient {patient_data['patient_id']}'s Details")
                gender_options = ["M", "F", "Rather Not Say"]

                if patient_data["gender"] != "":
                    gender_options.remove(patient_data["gender"])
                    gender_options.insert(0, patient_data["gender"])

                if patient_data["gender"] == "M":
                    st.image(
                        "assets/images/Black Man Feeling Sick.png",
                        width=300,
                        use_column_width=True,
                    )
                elif patient_data["gender"] == "F":
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
                    value=patient_data["patient_name"],
                    label_visibility="collapsed",
                )

                st.write("**Phone Number**")
                phone_number = st.text_input(
                    "phone_number",
                    value=patient_data["phone_number"],
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
                    value=0 if patient_data["weight"] == "" else patient_data["weight"],
                    label_visibility="collapsed",
                )

                st.write("**Any Further Details**")
                further_details = st.text_area(
                    "Further Details",
                    value=patient_data["further_details"],
                    label_visibility="collapsed",
                )

                submit_patient = st.form_submit_button("Submit")

            if submit_patient:
                form_holder.empty()
                placeholder.empty()
                details = {
                    "patient_id": patient_data["patient_id"],
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
                with st.spinner("Updating User Details"):
                    update_patient(
                        filtered_details,
                        key=patient_data["key"],
                    )

                st.experimental_rerun()


        if "patient_key" not in filtered_intv:
            if add_patient_details:
                st.session_state["intv_key"] = filtered_intv['key']
                page_util.add_page("Home", "Add_My_Patients")
                
                switch_page("add my patients")


            