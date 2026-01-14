import streamlit as st


def apply_compact_layout():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F1EFEF;
        }
        [data-testid="stContainer"] {
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #000000;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
        }
        [data-testid="stContainer"] > div {
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #000000;
            padding: 0.4rem;
        }
        [data-testid="stContainer"] * {
            color: #000000;
        }
        .drag-handle {
            cursor: move;
        }
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        h1, h2, h3 {
            margin-top: 0.4rem;
            margin-bottom: 0.2rem;
            color: #000000;
        }
        .element-container {
            margin-bottom: 0.4rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
