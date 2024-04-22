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

def retrieveUserInfo(conn):
    id = session_state.st.session_state.userID
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=%s", (id,))
    row = cursor.fetchone()
    return row

conn = db_utils.connect_to_db()

st.sidebar.title("Navigation")

if st.sidebar.button("My Account"):
    switch_page("user_account_page")
if st.sidebar.button("My Tracks"):
    switch_page("user_main_page")
if st.sidebar.button("Meal Log"):
    switch_page("meal_log")
if st.sidebar.button("Message Board"):
    switch_page("message_board_page")

if session_state.st.session_state.username == None:
    st.title(f"Please Sign in/ up to access your profile")
else:
    st.title(f"{session_state.st.session_state.username}'s Profile")

    info = retrieveUserInfo(conn)

    print()
    heightFeet = int(info[4] / 12)
    heightInches = int(info[4] - (heightFeet * 12))

    st.subheader('User Information')
    st.write(f'Email Address: {info[2]}')
    st.write(f'Gender: {info[7]}')
    st.write(f'Age: {info[6]}')
    st.write(f'Weight: {info[5]}')
    st.write(f'Height: {heightFeet} Feet, {heightInches} Inches')
    st.write(f'Weight: {info[5]} lbs')

    delEdit = row([2, 4], vertical_align="bottom")


    # Display delete account button
    if delEdit.button("Edit Information"):
        switch_page("edit_info_page")
    if not session_state.st.session_state.deleteConfirmation and delEdit.button("Delete Account"):
        session_state.st.session_state.deleteConfirmation = True

    #Warning for deleting an account
    if session_state.st.session_state.deleteConfirmation:
        st.warning("Are you sure you want to delete your account? This action cannot be undone.")
        options = row([2, 4], vertical_align="bottom")
        if options.button("Yes, delete my account"):
            print(session_state.st.session_state.userID)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user WHERE username=%s", (session_state.st.session_state.username,))
            conn.commit()
            session_state.st.session_state.userID = None
            session_state.st.session_state.username = None
            session_state.st.session_state.deleteConfirmation = False
            switch_page("home_page")
        elif options.button("Cancel"):
            session_state.st.session_state.deleteConfirmation = False
            switch_page("user_account_page")