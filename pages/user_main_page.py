import numpy as np
import pandas as pd
import streamlit as st

st.title("Welcome...")

st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Calories", 0, -1000, "inverse")
col2.metric("Protein", 0, -1000, "inverse")
col3.metric("Fat", 0, -1000, "inverse")

st.write("\n")
chart_data = pd.DataFrame(np.random.randn(20, 3).__abs__(), columns=["a", "b", "c"])

st.line_chart(chart_data)

col1, col2, col3 = st.columns(3)
col1.page_link("pages/search_page.py", label="Add Food Item to Meal")\
