import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
import datetime as dt
from streamlit_extras.mandatory_date_range import date_range_picker
from .db import read_products, create_intervention, read_interventions


def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = (
        """
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-repeat: no-repeat;
    background-size: contain;
    background-position: bottom right;
    }
    </style>
    """
        % bin_str
    )

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def return_care(x):
    return x


def record_intervention():
    # set_png_as_page_bg("assets/images/Black Man _ Woman Feeling Sick.png")

    intvs = read_interventions()

    placeholder = st.empty()

    with placeholder.container():
        st.markdown("#### Only 7-star Pharmacists Lead Interventions. Kudos!!")

        st.image(
            "assets/images/Black Man _ Woman Feeling Sick.png",
            width=300,
            use_column_width=True,
        )

        st.write("**When Did You Record This Intervention**")
        date = st.date_input("date", label_visibility="collapsed")

        st.write("**Select The Pharmaceutical Care**")
        pharma_care_type = st.selectbox(
            "Pharma Care Type", options=intvs.keys(), label_visibility="collapsed"
        )

        st.write("**Provide More Details**")
        pharma_care_details = st.multiselect(
            "Pharma Details",
            options=intvs[pharma_care_type]["reason"],
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
            options=intvs[pharma_care_type]["solution"],
            label_visibility="collapsed",
        )

        st.write("**Provide More Details**")
        intervention_details = st.text_area(
            "More Details", label_visibility="collapsed"
        )

        form_submit = st.button("Save and Continue")

    if form_submit:
        # details = {
        #     "recorded_date": date,
        #     "pharmaceutical_care": pharma_care_type,
        #     "pharmaceutical_care_details": pharma_care_details,
        #     "medications": medications,
        #     "intervention": intervention,
        #     "intervention_details": intervention_details,
        #     "pharmacist_details": st.session_state["username"],
        # }
        st.session_state["intv_key"] = ""
        switch_page("my patients")


def reset_button():
    st.session_state["p"] = False


def view_intervention():
    st.session_state["edit"] = False
    holder = st.empty()

    with holder.container():
        st.header("All Interventions Completed")
        date = date_range_picker(
            "Select a Date Range: ",
            default_start=dt.datetime.strptime("2023-01-01", "%Y-%m-%d"),
            min_date=dt.datetime.strptime("2023-01-01", "%Y-%m-%d"),
            max_date=dt.datetime.today(),
        )

        with st.expander("Ineffective Medicine"):
            st.markdown("")
            edit = st.checkbox("Edit Intervention", key="p")

    if edit:
        holder.empty()

        with st.form("Edit Intervention"):
            st.markdown("#### Kudos to more Insights!!")

            # st.image(
            #     "assets/images/Black Man _ Woman Feeling Sick.png",
            #     width=300,
            #     use_column_width=True,
            # )

            st.write("**When Did You Record This Intervention**")
            date = st.date_input("date", label_visibility="collapsed")

            st.write("**Select The Pharmaceutical Care**")
            pharma_care_type = st.selectbox(
                "Pharma Care Type", options=[], label_visibility="collapsed"
            )

            st.write("**Provide More Details**")
            pharma_care_details = st.multiselect(
                "Pharma Details", options=[], label_visibility="collapsed"
            )

            st.write("**Select Medications Involved**")
            medications = st.multiselect(
                "Medications", options=[], label_visibility="collapsed"
            )

            st.write("**What Was Your Intervention**")
            intervention = st.multiselect(
                "Intervention", options=[], label_visibility="collapsed"
            )

            st.write("**Provide More Details**")
            intervention_details = st.text_area(
                "More Details", label_visibility="collapsed"
            )
            # st.write(
            #     """<style>
            #          div.row-widget.stRadio > div{flex-direction:row;}
            #          </style>""",
            #     unsafe_allow_html=True,
            # )
            choice = st.radio(
                "Select Choice",
                options=[
                    "Save & Edit Corresponding Patient Information",
                    "Save & View All Interventions",
                ],
                label_visibility="collapsed",
            )

            if st.form_submit_button("Update Intervention"):
                if choice == "Save & Edit Corresponding Patient Information":
                    switch_page("patient details")
                elif choice == "Save & View All Interventions":
                    print(choice)
                    st.write(choice)
                    with st.balloons():
                        st.session_state["edit"] = False
                        st.experimental_rerun()
