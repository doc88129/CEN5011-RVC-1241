import numpy as np
import pandas as pd
import db_utils
import streamlit as st
from streamlit_extras.stateful_button import button
import mysql.connector
from mysql.connector import Error

# Persisting User
import session_state

st.title("Welcome...")

# Connect to the database
conn = db_utils.connect_to_db()

if conn:
    # Retrieve user information from the database
    user_info = db_utils.get_user_info(conn, session_state.st.session_state.userID)

    if user_info is not None:  # Check if user_info is not None
        # Display user metrics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Height", float(user_info['height']))
        col2.metric("Weight", float(user_info['weight']))
        col3.metric("Age", float(user_info['age']))
        col4.metric("Gender", user_info['gender'])

        # Display user food goals
        st.write("\n")
        st.subheader("Food Goals")
        user_food_goals = db_utils.get_user_food_goals(conn, session_state.st.session_state.userID)
        if user_food_goals:
            for goal in user_food_goals:
                st.write(f"- **Goal Type:** {goal['goal_type']}")
                st.write(f"  - Target Weight: {goal['target_weight']}")
                st.write(f"  - Target Calories per Day: {goal['target_calories_per_day']}")
                st.write(f"  - Target Protein per Day: {goal['target_protein_per_day']}")
                st.write(f"  - Target Carbs per Day: {goal['target_carbs_per_day']}")
                st.write(f"  - Target Fat per Day: {goal['target_fat_per_day']}")
                st.write(f"  - End Date: {goal['end_date']}")
        else:
            st.write("No food goals found for the user.")

        # Update user graph based on historical data
        st.write("\n")
        user_historical_data = db_utils.get_user_historical_data(conn, session_state.st.session_state.userID)
        chart_data = pd.DataFrame(user_historical_data, columns=["date_consumed", "calories", "protein", "carbs", "fat"])
        st.line_chart(chart_data.set_index('date_consumed'))

        col1, col2 = st.columns(2)
        if col1.button("Add Food Item to Meal"):
            st.switch_page("pages/search_page.py")
        if col2.button("Add New Food Goal"):
            goal_info = {}  # Example goal information, you can change this
            goal_info['goal_type'] = st.selectbox("Goal Type", ["Weight Loss", "Weight Gain", "Maintenance"])
            goal_info['target_weight'] = st.number_input("Target Weight", value=0.0, step=0.1)
            goal_info['target_calories_per_day'] = st.number_input("Target Calories per Day", value=0, step=1)
            goal_info['target_protein_per_day'] = st.number_input("Target Protein per Day", value=0, step=1)
            goal_info['target_carbs_per_day'] = st.number_input("Target Carbs per Day", value=0, step=1)
            goal_info['target_fat_per_day'] = st.number_input("Target Fat per Day", value=0, step=1)
            goal_info['end_date'] = st.date_input("End Date")
            
            # Use stateful_button to create toggle behavior
            if button("Log New Food Goal", key="log_food_goal"):
                db_utils.log_new_food_goal(conn, session_state.st.session_state.userID, goal_info)
                st.success("New food goal logged successfully!")

    else:
        st.error("Failed to retrieve user information. Please try again later.")

    st.write("\n")
    if st.button("Sign Out"):
        st.switch_page("home_page.py")
else:
    st.error("Failed to connect to the database. Please try again later.")

# Close the database connection
if conn:
    conn.close()