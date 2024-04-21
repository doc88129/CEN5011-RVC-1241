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
        cursor.execute("SELECT * FROM meal WHERE user_id = %s", (user_id,))
        meal_data = cursor.fetchall()
        return meal_data
    except Error as e:
        print(e)

# Function to log food item to meal in the database
def log_food_item(conn, user_id, meal_id, food_item_info):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meal (user_id, meal_id, meal_name, meal_type, calories, protein, carbs, fat, date_consumed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())",
                       (user_id, meal_id, food_item_info['meal_name'], food_item_info['meal_type'], food_item_info['calories'], food_item_info['protein'], food_item_info['carbs'], food_item_info['fat']))
        conn.commit()
    except Error as e:
        print(e)

# Function to log new food goal in the database
def log_new_food_goal(conn, user_id, goal_info):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO goal (user_id, goal_type, target_weight, target_calories_per_day, target_protein_per_day, target_carbs_per_day, target_fat_per_day, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)",
                       (user_id, goal_info['goal_type'], goal_info['target_weight'], goal_info['target_calories_per_day'], goal_info['target_protein_per_day'], goal_info['target_carbs_per_day'], goal_info['target_fat_per_day'], goal_info['end_date']))
        conn.commit()
    except Error as e:
        print(e)

def get_user_food_goals(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM goal WHERE user_id = %s", (user_id,))
        user_food_goals = cursor.fetchall()
        return user_food_goals
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
    
def verifyLogin(conn, username, password):

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))

    row = cursor.fetchone()

    if row:
        hashedPassword = row[3]
        if pbkdf2_sha256.verify(password, hashedPassword):
            cursor.execute("SELECT * FROM user WHERE username=%s", (username,))

            new_user_id = cursor.fetchone()[0]

            # Set session state
            session_state.st.session_state.userID = new_user_id
            session_state.st.session_state.username = username
            print(session_state.st.session_state.userID)
            return True
    return False
    
