import numpy as np
import pandas as pd
import db_utils
import streamlit as st
from streamlit_extras.stateful_button import button
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.row import row
import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta

# Persisting User
import session_state

st.sidebar.title("Navigation")

if st.sidebar.button("My Account"):
    switch_page("user_account_page")
if st.sidebar.button("Message Board"):
    switch_page("message_board_page")
if st.sidebar.button("Meal Log"):
    switch_page("meal_log")


# Function to calculate target nutritional values based on user's weight and goal
def calculate_target_nutrition(weight, target_weight, goal_type, goal_duration_days):
    # Check if goal_duration_days is provided and greater than zero
    if not goal_duration_days or goal_duration_days < 0:
        st.error("Goal duration must be provided and greater than zero.")
        st.stop()
    
    # Constants based on scientific research for macronutrient ratios
    PROTEIN_RATIO = 0.25  # Percentage of total daily calories from protein
    CARBS_RATIO = 0.45  # Percentage of total daily calories from carbohydrates
    FAT_RATIO = 0.30  # Percentage of total daily calories from fat
    
    try:
        # Calculate daily calorie change based on the goal type
        if goal_type == "Weight Loss":
            daily_calorie_change = (weight - target_weight) / goal_duration_days
        elif goal_type == "Weight Gain":
            daily_calorie_change = (target_weight - weight) / goal_duration_days
        else:
            daily_calorie_change = 0  # No change in calories for weight maintenance
        
        # Calculate target calories per day based on the calculated daily calorie change
        target_calories_per_day = weight * 14  # Example formula to calculate target calories
        target_calories_per_day += daily_calorie_change
        
        # Calculate target protein, carbs, and fat based on macronutrient ratios
        target_protein_per_day = target_calories_per_day * PROTEIN_RATIO / 4  # Protein has 4 calories per gram
        target_carbs_per_day = target_calories_per_day * CARBS_RATIO / 4  # Carbs have 4 calories per gram
        target_fat_per_day = target_calories_per_day * FAT_RATIO / 9  # Fat has 9 calories per gram
        
        return target_calories_per_day, target_protein_per_day, target_carbs_per_day, target_fat_per_day
    except ZeroDivisionError:
        st.error("Goal duration must be provided and greater than zero.")
        st.stop()



st.title(f"Welcome to {session_state.st.session_state.username}'s Diet Tracker")

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
            for i, goal in enumerate(user_food_goals, start=1):
                keys = list(goal.keys())
                for index, key in enumerate(keys):
                    words = key.split("_")
                    for j, word in enumerate(words):
                        words[j] = word.capitalize()
                    words = " ".join(words)
                    keys[index] = words
                columns = dict(zip(goal.keys(), keys))
                new = dict()
                for attribute, value in goal.items():
                    new[columns[attribute]] = value

                del new['Goal Id']
                st.dataframe(new, width=1000)
                goal_id = goal['goal_id']
                if st.button(f"Delete Goal {i}", key=f"delete_goal_{goal_id}"):
                    db_utils.delete_user_food_goal(st.session_state.conn, st.session_state.userID, goal_id)
                    st.success("Goal deleted successfully!")
                    # Refresh the page to reflect the updated goals
                    st.experimental_rerun()
        else:
            st.write("No food goals found for the user.")

        options = row([4, 4], vertical_align="bottom")

        if options.button("Add Food Item to Meal", key="button1"):
            st.switch_page("pages/search_page.py")
            
        # Check if the user already has a food goal
        existing_goal = bool(user_food_goals)
        
        # Add new food goal section only if the user doesn't have an existing goal
        if not st.session_state.open and not existing_goal:
            if options.button("Add New Food Goal", key="button2"):
                st.session_state.open = True

        if st.session_state.open:
            st.subheader("New Food Goal")
            goal_info = {}  # Example goal information, you can change this
            goal_info['goal_type'] = st.selectbox("Goal Type", ["Weight Loss", "Weight Gain", "Maintenance"])
            goal_info['target_weight'] = st.number_input("Target Weight", value=0.0, step=0.1)
            goal_info['start_date'] = date.today()  # Set start date to the current date
            goal_info['end_date'] = st.date_input("End Date", value=date.today()+timedelta(days=1), format="MM/DD/YYYY")
            
            # Calculate target nutritional values based on the user's weight, target weight, goal type, and duration
            target_calories_per_day, target_protein_per_day, target_carbs_per_day, target_fat_per_day = calculate_target_nutrition(
                float(user_info['weight']),
                goal_info['target_weight'],
                goal_info['goal_type'],
                (goal_info['end_date'] - goal_info['start_date']).days  # Calculate the duration of the goal in days
)


            # Populate the target nutritional values fields
            goal_info['target_calories_per_day'] = target_calories_per_day
            goal_info['target_protein_per_day'] = target_protein_per_day
            goal_info['target_carbs_per_day'] = target_carbs_per_day
            goal_info['target_fat_per_day'] = target_fat_per_day

           

            st.write("\n")
            options = row([4, 4], vertical_align="bottom")
            if options.button("Apply", key="button3"):
                db_utils.log_new_food_goal(st.session_state.conn, st.session_state.userID, goal_info)
                st.session_state.open = False
                # Refresh the page to reflect the updated goals
                st.experimental_rerun()
            if options.button("Cancel", key="button4"):
                st.session_state.open = False
                # Refresh the page to reflect the updated goals
                st.experimental_rerun()
            st.markdown("---")

        st.write("\n")
        if st.button("Sign Out"):
            st.session_state.clear()
            st.switch_page("home_page.py")
    else:
        st.error("Failed to retrieve user information. Please try again later.")
else:
    st.error("Failed to connect to the database. Please try again later.")
