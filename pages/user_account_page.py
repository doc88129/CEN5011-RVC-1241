import numpy as np
import pandas as pd
import mysql.connector
from passlib.hash import pbkdf2_sha256
import db_utils
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stateful_button import button
from streamlit_extras.row import row

# Persisting User
import session_state

# Create a global variable for database connection
if 'conn' not in st.session_state:
    st.session_state.conn = db_utils.connect_to_db()

# Check if the user is signed in
if st.session_state.username is None:
    st.title("Please Sign in/up to access your profile")
else:
    st.title(f"{st.session_state.username}'s Profile")

st.write('User Information')
st.write(f'Email')
# st.write(f'Gender: {}')
# st.write(f'Age: {}')
# st.write(f'Height: {}')
# st.write(f'Weight: {}')

# Display delete account button
if not st.session_state.deleteConfirmation and st.button("Delete Account"):
    st.session_state.deleteConfirmation = True

# Display warning and confirmation buttons if delete confirmation is True
if st.session_state.deleteConfirmation:
    st.warning("Are you sure you want to delete your account? This action cannot be undone.")
    row2 = row([2, 4], vertical_align="bottom")
    if row2.button("Yes, delete my account"):
        print(st.session_state.userID)
        cursor = st.session_state.conn.cursor()
        cursor.execute("DELETE FROM user WHERE username=%s", (st.session_state.username,))
        st.session_state.conn.commit()
        st.session_state.userID = None
        st.session_state.username = None
        st.session_state.deleteConfirmation = False
        switch_page("home_page")
    elif row2.button("Cancel"):
        st.session_state.deleteConfirmation = False
        switch_page("user_account_page")
