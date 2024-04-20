import streamlit as st

if __name__ == "__main__":
    st.title("Calorie Scraper")
    st.markdown("---")

    if st.button("Login"):
        st.switch_page("pages/login_page.py")
    if st.button("Logout"):
        st.switch_page("pages/sign_up_page.py")
