import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from helper_funcs.styles import read_html
from streamlit_extras.metric_cards import style_metric_cards
from helper_funcs.db import get_dashboard_data


def show_dashboard():
    # params = st.experimental_get_query_params()

    # if params and "refresh" not in st.session_state:
    #     switch_page(params["curr_page"][0])

    # st.experimental_set_query_params(curr_page="")

    st.subheader("My Impact")
    btncol1, btncol2 = st.columns([1, 2])

    with btncol1:
        if st.button("Add Intervention"):
            switch_page("my intervention")

    with btncol2:
        if st.button("Review My Day"):
            switch_page("my days")

    # components.html(
    #     read_html("styles/index.html"),
    #     height=0,
    #     width=0,
    # )
    df_patient, df_intv = get_dashboard_data(st.session_state["username"])
    if not df_patient.empty and not df_intv.empty:
        df_patient.merge(
            df_intv, how="inner", left_on="intervention_key", right_on="key"
        )

    patients = df_patient.shape[0]
    interventions = df_intv.shape[0]

    metric1Col1, metric1Col2 = st.columns([1, 1])

    metric1Col1.metric("**Interventions**", interventions)
    metric1Col2.metric("**Patients Impacted**", patients)
    # metric1Col3.metric("**Prescriptions Filled**", 30, "20%")
    style_metric_cards()

    st.write("####")

    if interventions > 0:
        group_df = df_intv.groupby(["pharmaceutical_care", "recorded_date"]).agg(
            Count=("recorded_date", "count")
        ).reset_index()

        fig = px.bar(group_df, x="recorded_date", y="Count", color="pharmaceutical_care")
        with fig.batch_update():
            fig.update_layout(coloraxis_showscale=False)
            fig.update_layout(
                title="Interventions Served",
            )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("You Have Not Served Any Interventions")