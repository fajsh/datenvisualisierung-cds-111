import streamlit as st

def render_sidebar():
    st.sidebar.title("Filter")

    st.sidebar.selectbox(
        "Jahr",
        [2023, 2024, 2025],
        key="year"
    )

    st.sidebar.selectbox(
        "Energiequelle",
        ["Alle", "Hydraulisch", "Kernkraftwerk", "Photovoltaik"],
        key="energy_filter"
    )
