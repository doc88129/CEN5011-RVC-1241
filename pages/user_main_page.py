import numpy as np
import pandas as pd
import streamlit as st

from session_state import SessionState

st.title("Welcome...")

# TODO - Gather user info from database

st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Calories", 0, -1000, "inverse")
col2.metric("Protein", 0, -1000, "inverse")
col3.metric("Fat", 0, -1000, "inverse")

# TODO - update user graph based on historical data
st.write("\n")
chart_data = pd.DataFrame(np.random.randn(20, 3).__abs__(), columns=["a", "b", "c"])

st.line_chart(chart_data)

col1, col2 = st.columns(2)
if col1.button("Add Food Item to Meal"):
    st.switch_page("pages/search_page.py")
if col2.button("Add New Food Goal"):
    # TODO - add page for food goal
    pass

st.write("\n")
if st.button("Sign Out"):
    st.switch_page("home_page.py")
