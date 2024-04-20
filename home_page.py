import streamlit as st
import mysql.connector
from passlib.hash import pbkdf2_sha256

#Connect to database
mydb = mysql.connector.connect(
    host="localhost",
    user="scrape",
    password="password",
    database="fooddb"
)

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

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
        uExist = check_username(mydb, newUsername)
        eExist = checkEmail(mydb, newEmail)
        print(uExist, eExist)
        if not (newUsername) or not (newPassword) or not (newEmail) or not(verifyPass) or not(gender) or not(age) or not(weight) or not(height1) or not (height2):
            st.error('Please fill in all fields')
        elif not(newPassword == verifyPass):
            st.error('Passwords do not match')
        elif not (uExist) and not (eExist):
            height = (height1*12) + height2
            add_user(mydb, newUsername, newPassword, newEmail, height, weight, age, gender)
            st.success('Account created successfully!')
        elif uExist:
            st.warning('Username already exists!')
        else:
            st.warning('Account using the provided email already exists!')

def check_username(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
    row = cursor.fetchone()
    if row:
        return True
    else:
        return False

def checkEmail(db, email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
    row = cursor.fetchall()
    if row:
        return True
    else:
        return False

# Function to add a new user
def add_user(conn, username, password, email, height, weight, age, gender):

    hashedPassword = pbkdf2_sha256.hash(password)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(user_id) FROM user")
    id = cursor.fetchone()[0] + 1

    cursor.execute("INSERT INTO user (user_id, username, password, email, height, weight, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id, username, hashedPassword, email, height, weight, age, gender))
    conn.commit()
    state.userId = id
    state.username = username

    print(state.userId)

if __name__ == "__main__":
    st.title("Calorie Scraper")

    state = SessionState(userId=None, username=None)

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

