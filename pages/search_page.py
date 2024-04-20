import streamlit as st
import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <table> elements
        table_elements = soup.find('table')

        # Iterate over each <table> element
        for table in table_elements:
            # Find all text within the <table> element
            table_text = table.get_text(separator='\n', strip=True)

            # TODO - add food item to user database
            # Print the text
            print(table_text)
            print()  # Add an empty line for better readability
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


st.title("Diettracker")

search = st.text_input("Enter a food item")

response = requests.get(f"https://www.myfooddata.com/search?search={search}")
soup = BeautifulSoup(response.content, 'html.parser')

for result in soup.find_all(attrs={"class": "searchresult"}):
    title = result.find(attrs={"class": "searchheading"})
    url = result.find(attrs={"class": "searchlink"})

    st.button(title.text, args=url, on_click=scrape_website)

    st.write("\n")
