import numpy as np
import pandas as pd
import mysql.connector
from passlib.hash import pbkdf2_sha256
import db_utils
import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stateful_button import button

#Persisting User
import session_state

conn = db_utils.connect_to_db()

if session_state.st.session_state.username == None:
    st.title(f"Please Sign in/ up to access your profile")
else:
    st.title(f"{session_state.st.session_state.username}'s Profile")

st.write('User Information')
st.write(f'Email')

# Display delete account button
if not session_state.st.session_state.deleteConfirmation and st.button("Delete Account"):
    session_state.st.session_state.deleteConfirmation = True

# Display warning and confirmation buttons if delete confirmation is True
if session_state.st.session_state.deleteConfirmation:
    st.warning("Are you sure you want to delete your account? This action cannot be undone.")
    if st.button("Yes, delete my account"):
        print(session_state.st.session_state.userID)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE username=%s", (session_state.st.session_state.username,))
        conn.commit()
        session_state.st.session_state.userID = None
        session_state.st.session_state.username = None
        session_state.st.session_state.deleteConfirmation = False
        switch_page("home_page")
    elif st.button("Cancel"):
        session_state.st.session_state.deleteConfirmation = False
        switch_page("user_account_page")