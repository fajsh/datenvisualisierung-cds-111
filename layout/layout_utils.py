import streamlit as st


def apply_compact_layout():
    st.markdown(
        """
        <style>

        /* App Background */
        .stApp {
            background-color: #F3F2F1;
        }

        /* Main block padding */
        .block-container {
            padding-top: 0.6rem;
            padding-bottom: 0.6rem;
        }

        /* Card container */
        [data-testid="stContainer"] {
            background-color: #FFFFFF;
            border-radius: 16px;
            border: none;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        }

        /* Inner content – NO extra border */
        [data-testid="stContainer"] > div {
            padding: 0.6rem 0.7rem;
            border-radius: 16px;
            background-color: #FFFFFF;
            border: none;
        }

        /* Typography */
        h1, h2, h3 {
            margin-top: 0.4rem;
            margin-bottom: 0.3rem;
            color: #1F2937; /* dark gray */
            font-weight: 600;
        }

        /* Text */
        p, span, label {
            color: #374151;
        }

        /* Reduce spacing between elements */
        .element-container {
            margin-bottom: 0.35rem;
        }

        /* Selectbox / inputs */
        div[data-baseweb="select"] {
            background-color: #F9FAFB;
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
