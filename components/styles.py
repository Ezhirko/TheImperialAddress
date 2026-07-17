import streamlit as st


def load_css():

    st.markdown("""
    <style>

    .block-container{

        padding-top:1rem;
        padding-bottom:1rem;
        max-width:95%;
    }

    div[data-testid="metric-container"]{

        background:#FFFFFF;

        border-radius:12px;

        padding:20px;

        box-shadow:0 2px 8px rgba(0,0,0,.12);
    }

    h1{

        color:#1F4E79;
    }

    </style>
    """,
    unsafe_allow_html=True)