import streamlit as st
import mysql.connector
from passlib.hash import pbkdf2_sha256
import random

mydb = mysql.connector.connect(
    host="localhost",
    user="scrape",
    password="password",
    database="fooddb"
)

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
def add_user(conn, username, password, email):


    hashed_password = pbkdf2_sha256.hash(password)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(user_id) FROM user")
    id = cursor.fetchone()[0] + 1

    cursor.execute("INSERT INTO user (user_id, username, password, email) VALUES (%s, %s, %s, %s)", (id, username, hashed_password, email))
    conn.commit()

st.subheader('Sign Up')
newEmail = st.text_input('Email')
newUsername = st.text_input('Username')
newPassword = st.text_input('Password', type='password')
if st.button('Sign Up'):
    uExist = check_username(mydb, newUsername)
    eExist = checkEmail(mydb, newEmail)
    print(uExist, eExist)
    if not (newUsername) or not (newPassword) or not(newEmail):
        st.error('Please fill in all fields')
    elif not(uExist) and not(eExist):
        add_user(mydb, newUsername, newPassword, newEmail)
        st.success('Account created successfully!')
    elif uExist:
        st.warning('Username already exists!')
    else:
        st.warning('Account using the provided email already exists!')
