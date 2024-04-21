import streamlit as st
import mysql.connector
import db_utils

#Persisting User
import session_state

# Connect to the database once at the start of the application
if 'conn' not in st.session_state:
    st.session_state.conn = db_utils.connect_to_db()
    


def showSignInPopup():

    st.markdown("---")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    if st.button('Sign In'):
        if not(username) or not(password):
            st.error('Missing username or password')
        elif db_utils.verifyLogin(st.session_state.conn, username, password):
            st.success('Login successful!')
            st.session_state.show_login_popup = False
        else:
            st.error('Invalid username or password')

def showSignUpPopup():
    st.markdown("---")
    newEmail = st.text_input('Email')
    newUsername = st.text_input('Username')
    newPassword = st.text_input('Password', type='password')
    verifyPass = st.text_input('Verify Password', type='password')

    st.markdown("---")
    st.subheader("Health Info")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    weight = st.number_input("Weight (lb)", min_value=1, max_value=500, step=1)
    col1, col2 = st.columns(2)
    height1 = col1.number_input("Height (ft)", min_value=1, max_value=10, step=1, value=5)
    height2 = col2.number_input("Height (in)", min_value=1, max_value=11, step=1, value=8)

    if st.button('Create Account'):
        uExist = db_utils.check_username(st.session_state.conn, newUsername)
        eExist = db_utils.checkEmail(st.session_state.conn, newEmail)
        print(uExist, eExist)
        if not (newUsername) or not (newPassword) or not (newEmail) or not(verifyPass) or not(gender) or not(age) or not(weight) or not(height1) or not (height2):
            st.error('Please fill in all fields')
        elif not(newPassword == verifyPass):
            st.error('Passwords do not match')
        elif not (uExist) and not (eExist):
            height = (height1*12) + height2
            db_utils.add_user(st.session_state.conn, newUsername, newPassword, newEmail, height, weight, age, gender)
            st.success('Account created successfully!')
        elif uExist:
            st.warning('Username already exists!')
        else:
            st.warning('Account using the provided email already exists!')


if __name__ == "__main__":
    st.title("Calorie Scraper")
    session_state.init()

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


