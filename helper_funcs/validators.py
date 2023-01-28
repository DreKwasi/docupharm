import streamlit as st


def validate_intervention(details):

    if details["pharmaceutical_care"]:
        if details["pharmaceutical_care_details"]:
            if details["medications"]:
                if details["intervention"]:
                    return True
                else:
                    st.error("Intervention Can Not Be Empty")
            else:
                st.error("Select At Least 1 Medication")
        else:
            st.error(
                "Give At least 1 Detail about the Pharmaceutical Care"
            )
    else:
        st.error("Select A Pharmaceutical Care")


def validate_patient(details, no_details=False):

    if not no_details:
        if details["patient_name"]:
            if details["phone_number"]:
                if details["gender"]:
                    return True
                else:
                    st.error("Indicate Patient's Gender")
            else:
                st.error("Indicate Patient's Phone Number")
        else:
            st.error("Patient Must Have A Name")

    if no_details:
        if details["gender"]:
            return True
        else:
            st.error("Indicate Patient's Gender")


# def validate_profile(details, error_placeholder):

#     if details["first_name"]:
#         if details["last_name"]:
#             if details["status"]:
#                 if details["reg_number"]:
#                     if (
#                         len(details["work_details"]["company"]) > 0
#                         and (details["work_details"]["location"]) > 0
#                         and (details["work_details"]["category"]) > 0
#                     ):
#                         return True
#                     else:
#                         error_placeholder.error("Indicate At Least One Work Detail")
#                 else:
#                     error_placeholder.error("Indicate Registration Number")
#             else:
#                 error_placeholder.error("Indicate Your Professional Status")
#         else:
#             error_placeholder.error("Please Input Your Last Name")
#     else:
#         error_placeholder.error("Please Input Your First Name")
