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

    st.sidebar.markdown("---")
    st.sidebar.subheader("Layout")
    st.sidebar.slider(
        "Container-Groesse",
        min_value=0.6,
        max_value=1.2,
        value=0.9,
        step=0.05,
        key="plot_scale",
        help="Skaliert die Hoehe und Breite der Plot-Container.",
    )
