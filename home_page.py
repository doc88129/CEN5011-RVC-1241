import streamlit as st
import mysql.connector
from passlib.hash import pbkdf2_sha256

# Initialize SQLite connection

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="scrape",
#     password="password",
#     database="fooddb"
# )
#
# if mydb.is_connected():
#     print('Yes')

def verifyLogin(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))

    row = cursor.fetchone()

    if row:
        hashedPassword = row[3]
        if pbkdf2_sha256.verify(password, hashedPassword):
            return True
    return False


def new_user():
    # TODO add user to DB
    pass


def showSignInPopup():
    # Create input fields for username and password
    st.markdown("---")
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


def showSignUpPopup():
    st.markdown("---")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    password2 = st.text_input("Confirm Password", type="password")

    st.markdown("---")
    st.subheader("Health Info")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    weight = st.number_input("Weight (lb)", min_value=1, max_value=500, step=1)
    col1, col2 = st.columns(2)
    height1 = col1.number_input("Height (ft)", min_value=1, max_value=10, step=1, value=5)
    height2 = col2.number_input("Height (in)", min_value=1, max_value=12, step=1, value=8)

    # TODO - info validation
    # TODO - create user in DB


if __name__ == "__main__":
    st.title("Calorie Scraper")

    if st.button("Login"):
        st.session_state.show_signup_popup = False
        st.session_state.show_login_popup = True

    if st.button("Sign Up"):
        st.session_state.show_login_popup = False
        st.session_state.show_signup_popup = True

    if st.session_state.get('show_login_popup'):
        showSignInPopup()
    if st.session_state.get('show_signup_popup'):
        showSignUpPopup()
