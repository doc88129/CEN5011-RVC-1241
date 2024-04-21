import streamlit as st
import requests
from bs4 import BeautifulSoup
import db_utils

#Persisting User
import session_state

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <table> elements
        table_elements = soup.find('table')
        calories = table_elements.find('td', class_='nft-cal-amt ENERC_KCAL').text
        fat = table_elements.find('span', class_='FAT').text
        protein = table_elements.find('span', class_='PROCNT').text
        carbs = table_elements.find('span', class_='CHOCDF').text

        name = soup.find('h1', class_='nutritionFactsTitle').text

        food_item_info = {
            'meal_name': name,
            'meal_type': name,
            'calories': int(''.join(c for c in calories if c.isdigit())),
            'protein': int(''.join(c for c in protein if c.isdigit())),
            'carbs': int(''.join(c for c in carbs if c.isdigit())),
            'fat': int(''.join(c for c in fat if c.isdigit()))
        }

        db_utils.log_food_item(st.session_state.conn, st.session_state.userID, food_item_info)
        st.success(f"{food_item_info['meal_name']} was added to today's Meal")

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


st.title(f"{session_state.st.session_state.username}'s Diet Tracker")

search = st.text_input("Enter a food item")
if st.button("Return"):
    st.switch_page("pages/user_main_page.py")
st.markdown("---")

response = requests.get(f"https://www.myfooddata.com/search?search={search}")
soup = BeautifulSoup(response.content, 'html.parser')

for result in soup.find_all(attrs={"class": "searchresult"}):
    title = result.find(attrs={"class": "searchheading"})
    url = result.find(attrs={"class": "searchlink"})

    st.button(title.text, args=url, on_click=scrape_website)

    st.write("\n")
