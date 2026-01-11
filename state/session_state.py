import streamlit as st

def init_state():
    if "year" not in st.session_state:
        st.session_state.year = 2025

    if "energy_filter" not in st.session_state:
        st.session_state.energy_filter = "Alle"


# Plots lesen nur: st.session_state.year