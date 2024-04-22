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

st.title("Create New Post")
st.markdown("---")

postUser = session_state.st.session_state.username
postTitle = st.text_input("Post Title")
postContent = st.text_area("Post Description")

options = row([9, 2], vertical_align="bottom")
if options.button("Cancel"):
    switch_page("message_board_page")
if options.button("Create Post"):
    db_utils.add_message(st.session_state.conn, session_state.st.session_state.username, postTitle, postContent)
    print("Message added")
    switch_page("message_board_page")