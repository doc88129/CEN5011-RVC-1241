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

# Create a global variable for database connection
if 'conn' not in st.session_state:
    st.session_state.conn = db_utils.connect_to_db()
    

if session_state.st.session_state.username == None:
    st.title(f"Please Sign in/ up to access your profile")
else:
    st.title(f"Edit your Information")
    st.markdown("---")

    info = db_utils.get_user_info(st.session_state.conn, session_state.st.session_state.userID)
    id = session_state.st.session_state.userID
    print(info)

    heightFeet = int(info['height'] / 12)
    heightInches = int(info['height'] - (heightFeet * 12))

    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=100, step=1, value=info['age'])
    weight = st.number_input("Weight (lb)", min_value=1, max_value=500, step=1, value=int(info['weight']))
    col1, col2 = st.columns(2)
    height1 = col1.number_input("Height (ft)", min_value=1, max_value=10, step=1, value=heightFeet)
    height2 = col2.number_input("Height (in)", min_value=1, max_value=11, step=1, value=heightInches)

    height = (height1 * 12) + height2

    options = row([9, 2], vertical_align="bottom")
    if options.button("Cancel"):
        switch_page("user_account_page")
    if options.button("Save Changes"):
        cursor = st.session_state.conn.cursor()
        cursor.execute("UPDATE user SET gender=%s WHERE user_id=%s", (gender, id))
        st.session_state.conn.commit()
        cursor.execute("UPDATE user SET age=%s WHERE user_id=%s", (age, id))
        st.session_state.conn.commit()
        cursor.execute("UPDATE user SET weight=%s WHERE user_id=%s", (weight, id))
        st.session_state.conn.commit()
        cursor.execute("UPDATE user SET height=%s WHERE user_id=%s", (height, id))
        st.session_state.conn.commit()
        switch_page("user_account_page")

