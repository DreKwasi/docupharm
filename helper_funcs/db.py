from deta import Deta
import streamlit as st
import pandas as pd
import json

st.experimental_memo
def read_products():
    df = pd.read_csv("assets/data/products.csv")

    return df


st.experimental_memo
def read_locations():
    df = pd.read_csv("assets/data/locations.csv")

    return df

st.experimental_memo
def read_interventions():
    with open("assets/data/interventions.json") as f:
        return json.load(f)

# Initialize Deta Object with Project Key
deta_cred = st.secrets["db_credentials"]
deta = Deta(deta_cred["deta_key"])
users = deta.Base("users")
interventions = deta.Base("interventions")
patients = deta.Base("patients")



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

    first_key = list(new_username.keys())[0]
    insert_user = new_username[first_key]
    insert_user["username"] = first_key
    insert_user["profile"] = {}
    users.insert(insert_user)


def update_user_profile(details, username):
    users = deta.Base("users")
    user_key = users.fetch({"username": username}).items[0]["key"]
    users.update({"profile": details}, key=user_key)
    

# Redirect to Complete Profile when User is Logged in for the First Time
def check_profile(username):
    users = deta.Base("users")
    user_profile = users.fetch({"username": username}).items[0]["profile"]
    if bool(user_profile):
        st.session_state["profile_header"] = "Profile Details"
        return True
    else:
        st.session_state["profile_header"] = "Complete Your Profile"
        return False


def create_intervention(details):
    intervention_dict = interventions.insert(details)
    return intervention_dict['key']
    
def create_patient(details):
    patients.insert(details)