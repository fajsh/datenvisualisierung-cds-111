import streamlit as st

def render_header():
    col1, col2, col3 = st.columns(3)

    col1.metric("Stromproduktion", "192 GWh", "+3%")
    col2.metric("Import", "39 GWh", "-5%")
    col3.metric("Strompreis", "95 CHF/MWh", "+2%")
