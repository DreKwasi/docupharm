from deta import Deta
import streamlit as st
import pandas as pd
import json
from streamlit_extras.switch_page_button import switch_page


st.cache


def read_products():
    df = pd.read_csv("assets/data/products.csv")

    return df


st.cache


def read_locations():
    df = pd.read_csv("assets/data/locations.csv")

    return df


st.cache


def read_interventions():
    with open("assets/data/interventions.json") as f:
        return json.load(f)


# Initialize Deta Object with Project Key
deta_cred = st.secrets["db_credentials"]
deta = Deta(deta_cred["deta_key"])
users = deta.Base("users")


def get_all_user_details():
    users = deta.Base("users")
    usernames = {}
    all_users_obj = users.fetch()  # Get All Users (Rows)
    all_users = all_users_obj.items

    # Wrangling structure for Authentication
    for user in all_users:
        usernames[user["username"]] = user
    return usernames


def create_user(details):
    users = deta.Base("users")
    users.insert(details)


def update_user_profile(details, username):
    users = deta.Base("users")
    user_key = users.fetch({"username": username}).items[0]["key"]
    users.update({"profile": details}, key=user_key)


def get_profile(username):
    users = deta.Base("users")
    user_items = users.fetch({"username": username}).items
    return user_items[0]["profile"]


# Redirect to Complete Profile when User is Logged in for the First Time
def check_profile(username):
    try:
        users = deta.Base("users")
        user_profile = users.fetch({"username": username}).items[0]["profile"]
        if bool(user_profile):
            st.session_state["profile_header"] = "Profile Details"
            return True
        else:
            st.session_state["profile_header"] = "Complete Your Profile"
            return False
    except Exception:
        return False


def create_intervention(details, username):
    interventions = deta.Base("interventions")
    num_intvs = interventions.fetch({"pharmacist": username}).count
    details["intervention_id"] = f"{num_intvs + 1}"

    intervention_dict = interventions.insert(details)
    return intervention_dict["key"]


def update_intervention(details, key):
    interventions = deta.Base("interventions")
    interventions.update(details, key=key)


def create_patient(details):
    if "intervention_key" in details and details["intervention_key"] != "":
        print()
        patients = deta.Base("patients")

        # insert into interventions as well
        intvs = deta.Base("interventions")

        patient_intv = intvs.fetch({"key": details["intervention_key"][0]}).items[0]

        num_patients = patients.fetch({"pharmacist": details["pharmacist"]}).count
        details["patient_id"] = f"{num_patients + 1}"
        patients = patients.insert(details)

        patient_intv["patient"] = f"{patients['patient_name']}"
        patient_intv["patient_key"] = f"{patients['key']}"

        del patient_intv["key"]

        intvs.update(patient_intv, key=details["intervention_key"][0])

        st.session_state["intv_key"] = ""
        switch_page("my interventions")
    else:
        st.error("Kindly Add An Intervention for this Patient")
        if st.button("Add Intervention"):
            switch_page("my interventions")


def update_patient(details, key, intv_key=None):
    if type(key) != str:
        key = key.values[0]

    patients = deta.Base("patients")

    if intv_key != None:

        if intv_key != "":

            details["intervention_key"] = patients.util.append(intv_key)
            patients.update(details, key=key)

            # insert into interventions as well
            intvs = deta.Base("interventions")

            patient_intv = intvs.fetch({"key": intv_key}).items[0]

            del patient_intv["key"]

            patient_intv["patient"] = f"{details['patient_name']}"
            patient_intv["patient_key"] = key

            intvs.update(patient_intv, key=intv_key)

            st.session_state["intv_key"] = ""
            switch_page("my intervention")
        else:
            st.error("Kindly Add An Intervention for this Patient")
            if st.button("Add Intervention"):
                switch_page("my intervention")

    else:
        patients.update(details, key=key)


def get_patient(patient_key):
    patients = deta.Base("patients")
    patient = patients.get(key=patient_key)
    return patient


def get_all_patients():
    patients = deta.Base("patients")
    all_patients = patients.fetch({"pharmacist": st.session_state["username"]}).items

    df = pd.DataFrame(all_patients)

    renamed = {
        "patient_name": "Patient Name",
        "phone_number": "Phone Number",
        "gender": "Gender",
        "weight": "Weight (kg)",
        "further_details": "Further Details",
        "patient_id": "Patient ID",
    }
    order = [
        "Patient ID",
        "Patient Name",
        "Gender",
        "Phone Number",
        "Weight (kg)",
        "Further Details",
        "key",
        "intervention_key",
    ]
    df.rename(columns=renamed, inplace=True)
    ordered_df = df.reindex(columns=order, copy=True)

    ordered_df.fillna("None", inplace=True)

    return ordered_df


def get_all_intvs(username):
    intvs = deta.Base("interventions")
    user_intvs = intvs.fetch({"pharmacist": username}).items
    patients = deta.Base("patients")

    final_list = []
    for intv in user_intvs:
        try:
            intv["patient_name"] = patients.get(key=intv["patient_key"])["patient_name"]
        except KeyError:
            intv["patient_name"] = "No Patient"
        final_list.append(intv)

    new_names = {
        "company": "Company",
        "intervention": "Intervention(s)",
        "intervention_id": "Intervention ID",
        "pharmaceutical_care": "Pharmaceutical Care",
        "patient_name": "Patient Name",
        "recorded_date": "Recorded Date",
    }

    df = pd.DataFrame(final_list)
    df.rename(columns=new_names, inplace=True)
    df = df.reindex(
        columns=[
            "Recorded Date",
            "Patient Name",
            "Intervention ID",
            "Pharmaceutical Care",
            "Intervention(s)",
            "Company",
        ]
    )

    df.fillna("None", inplace=True)
    df.replace("", "None", inplace=True)
    return df, final_list


def get_dashboard_data(username):
    intvs = deta.Base("interventions")
    patients = deta.Base("patients")
    final_list = patients.fetch({"pharmacist": username}).items
    patients_list = [
        {
            "intervention_key": val,
            "further_details": i["further_details"],
            "gender": i["gender"],
            "key": i["key"],
            "patient_id": i["patient_id"],
            "patient_name": i["patient_name"],
            "pharmacist": i["pharmacist"],
            "phone_number": i["phone_number"],
            "weight": i["weight"],
        }
        for i in final_list
        for key, value in i.items()
        if key == "intervention_key" and value
        for val in value
    ]

    df_patient = pd.DataFrame(patients_list)
    df_intv = pd.DataFrame(intvs.fetch({"pharmacist": username}).items)

    return df_patient, df_intv
