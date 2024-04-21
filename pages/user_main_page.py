import numpy as np
import pandas as pd
import db_utils
import streamlit as st
from streamlit_extras.stateful_button import button
from streamlit_extras.row import row
import mysql.connector
from mysql.connector import Error

# Persisting User
import session_state

st.title("Welcome...")


if st.session_state.conn:
    # Retrieve user information from the database
    user_info = db_utils.get_user_info(st.session_state.conn, st.session_state.userID)

    if user_info is not None:  # Check if user_info is not None
        # Display user metrics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Height (in)", int(user_info['height']))
        col2.metric("Weight (lb)", float(user_info['weight']))
        col3.metric("Age", int(user_info['age']))
        col4.metric("Gender", user_info['gender'])

        # Display user food goals
        st.write("\n")
        st.markdown("---")
        st.subheader("Food Goals")
        user_food_goals = db_utils.get_user_food_goals(st.session_state.conn, st.session_state.userID)
        if user_food_goals:
            for goal in user_food_goals:
                keys = list(goal.keys())
                for index, key in enumerate(keys):
                    words = key.split("_")
                    for i, word in enumerate(words):
                        words[i] = word.capitalize()
                    words = " ".join(words)
                    keys[index] = words
                columns = dict(zip(goal.keys(), keys))
                new = dict()
                for attribute, value in goal.items():
                    new[columns[attribute]] = value

                st.dataframe(new, width=1000)

        else:
            st.write("No food goals found for the user.")

        # Update user graph based on historical data
        st.write("\n")
        user_historical_data = db_utils.get_user_historical_data(st.session_state.conn, st.session_state.userID)
        chart_data = pd.DataFrame(user_historical_data, columns=["date_consumed", "calories", "protein", "carbs", "fat"])
        st.line_chart(chart_data.set_index('date_consumed'))
        st.markdown("---")

        options = row([4, 4], vertical_align="bottom")

        if options.button("Add Food Item to Meal", key="button1"):
            st.switch_page("pages/search_page.py")
        if options.button("Add New Food Goal", key="button2") and not st.session_state.open:
            st.session_state.open = True
        if st.session_state.open:
            st.subheader("New Food Goal")
            goal_info = {}  # Example goal information, you can change this
            goal_info['goal_type'] = st.selectbox("Goal Type", ["Weight Loss", "Weight Gain", "Maintenance"])
            goal_info['target_weight'] = st.number_input("Target Weight", value=0.0, step=0.1)
            goal_info['target_calories_per_day'] = st.number_input("Target Calories per Day", value=0, step=1)
            goal_info['target_protein_per_day'] = st.number_input("Target Protein per Day", value=0, step=1)
            goal_info['target_carbs_per_day'] = st.number_input("Target Carbs per Day", value=0, step=1)
            goal_info['target_fat_per_day'] = st.number_input("Target Fat per Day", value=0, step=1)
            goal_info['end_date'] = st.date_input("End Date")

            st.write("\n")
            options = row([4, 4], vertical_align="bottom")
            if options.button("Add New Food Item to Meal", key="button3"):
                db_utils.log_new_food_goal(st.session_state.conn, st.session_state.userID, goal_info)
                st.session_state.open = False
            if options.button("Cancel", key="button4"):
                st.session_state.open = False
            st.markdown("---")

    else:
        st.error("Failed to retrieve user information. Please try again later.")

    st.write("\n")
    if st.button("Sign Out"):
        st.session_state.clear()
        st.switch_page("home_page.py")
else:
    st.error("Failed to connect to the database. Please try again later.")

