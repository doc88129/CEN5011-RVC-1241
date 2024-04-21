import mysql.connector
from mysql.connector import Error
from passlib.hash import pbkdf2_sha256

import session_state

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            database="fooddb",
            user="root",
            password="password"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print(e)

# Function to retrieve user information from the database
def get_user_info(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
        user_info = cursor.fetchone()
        return user_info
    except Error as e:
        print(e)

# Function to retrieve user's historical data from the database
def get_user_historical_data(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT meal.meal_id, meal.meal_name, meal.meal_type, meal.calories, meal.protein, meal.carbs, meal.fat, meal.date_consumed 
            FROM meal 
            JOIN user_meal ON meal.meal_id = user_meal.meal_id 
            WHERE user_meal.user_id = %s
        """, (user_id,))
        meal_data = cursor.fetchall()
        return meal_data
    except Error as e:
        print(e)


# Function to log food item to meal in the database
def log_food_item(conn, user_id, food_item_info):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Meal (meal_name, meal_type, calories, protein, carbs, fat, date_consumed) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW())""",
                       (food_item_info['meal_name'], food_item_info['meal_type'],
                        food_item_info['calories'], food_item_info['protein'], 
                        food_item_info['carbs'], food_item_info['fat']))
        
        # Fetch the last inserted meal_id
        meal_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO User_Meal (user_id, meal_id) VALUES (%s, %s)""",
                       (user_id, meal_id))
        conn.commit()
    except Error as e:
        print(e)

# Function to log new food goal in the database
def log_new_food_goal(conn, user_id, goal_info):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Goal (goal_type, target_weight, target_calories_per_day, target_protein_per_day, 
                              target_carbs_per_day, target_fat_per_day, start_date, end_date) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)""",
                       (goal_info['goal_type'], goal_info['target_weight'], goal_info['target_calories_per_day'], 
                        goal_info['target_protein_per_day'], goal_info['target_carbs_per_day'], 
                        goal_info['target_fat_per_day'], goal_info['end_date']))
        cursor.execute("""
            INSERT INTO User_Goal (user_id, goal_id) VALUES (%s, LAST_INSERT_ID())""", (user_id,))
        conn.commit()
    except Error as e:
        print(e)

def get_user_food_goals(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM Goal 
            WHERE goal_id IN (
                SELECT goal_id FROM User_Goal WHERE user_id = %s
            )
        """, (user_id,))
        user_food_goals = cursor.fetchall()
        return user_food_goals
    except Error as e:
        print(e)

def delete_user_food_goal(conn, user_id, goal_id):
    try:
        cursor = conn.cursor()
        # First, delete the entry from the User_Goal table
        cursor.execute("DELETE FROM User_Goal WHERE user_id = %s AND goal_id = %s", (user_id, goal_id))
        # Then, delete the corresponding goal from the Goal table
        cursor.execute("DELETE FROM Goal WHERE goal_id = %s", (goal_id,))
        conn.commit()
        print("Goal deleted successfully")
    except Error as e:
        print(e)

        
def check_username(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
    row = cursor.fetchone()
    if row:
        return True
    else:
        return False

def checkEmail(db, email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
    row = cursor.fetchall()
    if row:
        return True
    else:
        return False

# Function to add a new user
def add_user(conn, username, password, email, height, weight, age, gender):

    hashedPassword = pbkdf2_sha256.hash(password)
    cursor = conn.cursor()

    # Execute INSERT query to add the new user
    cursor.execute("INSERT INTO user (username, password, email, height, weight, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, hashedPassword, email, height, weight, age, gender))
    conn.commit()

    # Retrieve the auto-generated user_id
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))

    new_user_id = cursor.fetchone()[0]

    # Set session state
    session_state.st.session_state.userID = new_user_id
    session_state.st.session_state.username = username

    print(session_state.st.session_state.username)

def add_message(conn, username, title, content):

    cursor = conn.cursor()

    # Execute INSERT query to add the new user
    cursor.execute("INSERT INTO message (username, title, content) VALUES (%s, %s, %s)", (username, title, content))
    conn.commit()
    
def verifyLogin(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
    row = cursor.fetchone()

    if row:
        hashedPassword = row[3]
        if pbkdf2_sha256.verify(password, hashedPassword):
            new_user_id = row[0]

            # Set session state
            session_state.st.session_state.userID = new_user_id
            session_state.st.session_state.username = username
            print(session_state.st.session_state.userID)
            return True

    return False

    
