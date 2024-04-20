import streamlit as st


st.subheader('Sign Up')
username = st.text_input('Enter your username')
password = st.text_input('Enter your password')
email = st.text_input('Enter your email')

if st.button('Sign Up'):
    if not username or not password or not email:
        st.error('Please fill all fields')
        st.stop()

    # TODO - add user to database

    st.success('Sign up successful')
    st.switch_page("pages/user_main_page.py")
