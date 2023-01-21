import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from helper_funcs.styles import read_html


def show_dashboard():

    st.subheader("My Impact")
    btncol1, btncol2 = st.columns([1, 2])
    with btncol1:

        if st.button("Add Intervention"):
            switch_page("my intervention")
    with btncol2:
        if st.button("Review My Day"):
            switch_page("my days")

    components.html(
        read_html("styles/index.html"),
        height=0,
        width=0,
    )

    metric1Col1, metric1Col2 = st.columns([1, 1])
    metric2Col1, metric2Col2 = st.columns([3, 1])

    metric1Col1.metric("**Interventions**", 40, "50%")
    metric1Col2.metric("**Patients Impacted**", 4, "-90%")
    metric2Col1.metric("**Prescriptions Filled**", 30, "20%")
    metric2Col2.metric("**Revenue Led**", "GHS100", "-80%")

    st.write("####")

    data_canada = px.data.gapminder()
    fig = px.bar(data_canada, x="year", y="pop")
    with fig.batch_update():
        fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(
            title="Interventions Served",
        )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
