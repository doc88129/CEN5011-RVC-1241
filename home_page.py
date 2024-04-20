import streamlit as st
import mysql.connector
from passlib.hash import pbkdf2_sha256

# Initialize SQLite connection

mydb = mysql.connector.connect(
    host="localhost",
    user="scrape",
    password="password",
    database="fooddb"
)

if mydb.is_connected():
    print('Yes')

def verifyLogin(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))

    row = cursor.fetchone()

    if row:
        hashedPassword = row[3]
        if pbkdf2_sha256.verify(password, hashedPassword):
            return True
    return False

def showSignInPopup():
    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create a button to submit the sign-in credentials
    if st.button('Sign In'):
        if not(username) or not(password):
            st.error('Missing username or password')
        elif verifyLogin(mydb, username, password):
            st.success('Login successful!')
            st.session_state.show_login_popup = False  # Hide the popup
        else:
            st.error('Invalid username or password')

if __name__ == "__main__":
    st.title("Calorie Scraper")

    if st.button("Login"):
        st.session_state.show_login_popup = True

    if st.session_state.get('show_login_popup'):
        showSignInPopup()
