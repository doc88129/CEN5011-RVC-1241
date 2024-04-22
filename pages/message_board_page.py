import mysql.connector
from passlib.hash import pbkdf2_sha256
import db_utils
import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stateful_button import button
from streamlit_extras.row import row

#Persisting User
import session_state

if 'conn' not in st.session_state:
    st.session_state.conn = db_utils.connect_to_db()

st.sidebar.title("Navigation")

if st.sidebar.button("My Account"):
    switch_page("user_account_page")
if st.sidebar.button("My Tracks"):
    switch_page("user_main_page")
if st.sidebar.button("Meal Log"):
    switch_page("meal_log")

def gatherMessages():

    mycursor = st.session_state.conn.cursor()
    mycursor.execute("SELECT username, DATE(datetime_posted), title, content FROM message ORDER BY datetime_posted DESC LIMIT 6")

    messages = mycursor.fetchall()

    for post in messages:
        messageTitle = post[2]
        messageUser = post[0]
        messageDate = post[1]
        messageContent = post[3]

        messageInfo = row([6, 2, 4], vertical_align="bottom")
        messageInfo.subheader(messageTitle)
        messageInfo.write(messageUser)
        messageInfo.write(messageDate)
        st.write(messageContent)

header = row([12, 2], vertical_align="bottom")
header.title("User Posts")
if header.button("New Post"):
    if session_state.st.session_state.username == None:
        st.warning("Please sign up/in to an account to create a post")
    else:
        switch_page("new_post_page")
gatherMessages()
