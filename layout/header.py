import streamlit as st

def render_header():
    col1, col2, col3 = st.columns([2, 3, 1])

    with col1:
        st.markdown("### Energie Dashboard 2025")

    with col2:
        st.text_input(
            "Suche",
            placeholder="Landesverbrauch, Import, Export",
            label_visibility="collapsed",
        )

    with col3:
        st.selectbox("User", ["User"], label_visibility="collapsed")
