import streamlit as st
import streamlit.components.v1 as components


def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def read_html(file):
    with open(file) as f:
        return f.read()