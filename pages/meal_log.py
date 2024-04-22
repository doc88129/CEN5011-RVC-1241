import db_utils
import streamlit as st

# Persisting User
import session_state

st.title("Meal Log")

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
            # Group meals by date
            meals_by_date = meal_df.groupby('date_consumed')
            # Iterate over each date
            for date, meals in meals_by_date:
                st.write(f"Date: {date}")
                # Display meals for the date
                for index, meal in meals.iterrows():
                    st.write(f"Meal Name: {meal['meal_name']}")
                    st.write(f"Meal Type: {meal['meal_type']}")
                    st.write(f"Calories: {meal['calories']}")
                    st.write(f"Protein: {meal['protein']} grams")
                    st.write(f"Carbs: {meal['carbs']} grams")
                    st.write(f"Fat: {meal['fat']} grams")
                    st.write('---')
        else:
            st.write("No meal data found.")

    else:
        st.error("Failed to retrieve user information. Please try again later.")
else:
    st.error("Failed to connect to the database. Please try again later.")