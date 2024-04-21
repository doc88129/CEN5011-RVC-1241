import streamlit as st

def init():
    if 'userID' not in st.session_state:
        st.session_state.userID = None
        st.session_state.username = None