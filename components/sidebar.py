import streamlit as st
from pathlib import Path

def draw_sidebar():

    with st.sidebar:

        logo = Path("assets/logo.png")
        if logo.exists():
            st.image(str(logo), width=130)
            
        st.title("Imperial Address")
        st.success("Society Analytics Dashboard")
        st.info("Version 1.0")