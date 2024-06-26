import numpy as np
import pandas as pd
import db_utils
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Persisting User
import session_state

st.title("Meal Log")

st.sidebar.title("Navigation")
st.markdown("---")

if st.sidebar.button("My Account"):
    switch_page("user_account_page")
if st.sidebar.button("My Tracks"):
    switch_page("user_main_page")
if st.sidebar.button("Meal Log"):
    switch_page("meal_log")
if st.sidebar.button("Message Board"):
    switch_page("message_board_page")
    
# Check database connection
if st.session_state.conn:
    # Retrieve user information from the database
    user_info = db_utils.get_user_info(st.session_state.conn, st.session_state.userID)

    if user_info is not None:
        st.write(f"Welcome, {user_info['username']}!")

        # Retrieve user's historical meal data
        user_meal_data = db_utils.get_user_historical_data(st.session_state.conn, st.session_state.userID)
        if user_meal_data:
            st.subheader("Meal Log")
            # Convert meal data to DataFrame
            meal_df = pd.DataFrame(user_meal_data)
            # Remove 'meal_type' column
            meal_df.drop(columns=['meal_type'], inplace=True)
            # Group meal data by date
            meals_by_date = meal_df.groupby('date_consumed')
            # Display meal data organized by date
            for date, meals in meals_by_date:
                st.write(f"Date: {date}")
                # Exclude 'meal_id' column
                meals_without_id = meals.drop(columns=['meal_id'])
                # Calculate total consumption for the day
                total_consumption = meals_without_id.sum(axis=0) 
                # Add total consumption row to the DataFrame
                meals_without_id.loc['Total'] = total_consumption
                meals_without_id.loc['Total', 'meal_name'] = '-'
                meals_without_id.loc['Total', 'date_consumed'] = '-'
                st.table(meals_without_id)
                st.write('---')
        else:
            st.write("No meal data found.")

    else:
        st.error("Failed to retrieve user information. Please try again later.")
else:
    st.error("Failed to connect to the database. Please try again later.")