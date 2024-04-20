import streamlit as st


# Login section
st.subheader('Login')
username = st.text_input('Username')
password = st.text_input('Password')

if st.button('Login'):
    if not username or not password:
        st.error('Please fill in all fields')
        st.stop()

    # TODO - user verification

    st.success('Login successful!')
    st.switch_page("pages/user_main_page.py")
