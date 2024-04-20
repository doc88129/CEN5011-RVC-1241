import streamlit as st

if __name__ == "__main__":
    st.title("Calorie Scraper")
    st.markdown("---")

    st.page_link("pages/login_page.py", label="Login", use_container_width=True)
    st.page_link("pages/sign_up_page.py", label="Sign Up", use_container_width=True)
