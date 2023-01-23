from deta import Deta
import streamlit as st
import pandas as pd
import json

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


def create_user(usernames):
    users = deta.Base("users")
    previous_users = users.fetch().items
    previous_usernames = [x["username"] for x in previous_users]

    new_username = {
        key: value for key, value in usernames.items() if key not in previous_usernames
    }

    first_key = next(iter(new_username))
    insert_user = new_username[first_key]
    insert_user["username"] = first_key
    insert_user["profile"] = {}
    users.insert(insert_user)


def update_user_profile(details, username):
    users = deta.Base("users")
    user_key = users.fetch({"username": username}).items[0]["key"]
    users.update({"profile": details}, key=user_key)


def get_profile(username):
    users = deta.Base("users")
    user_items = users.fetch({"username": username}).items
    return user_items[0]['profile']

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

def create_intervention(details):
    interventions = deta.Base("interventions")
    intervention_dict = interventions.insert(details)
    return intervention_dict["key"]


def create_patient(details):
    patients = deta.Base("patients")
    num_patients = patients.fetch({"pharmacist": "drekwasi"}).count
    details["patient_id"] = {num_patients + 1}
    patients.insert(details)


def update_patient(details, key):
    key = key.values[0]
    patients = deta.Base("patients")
    patients.update(details, key=key)

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
