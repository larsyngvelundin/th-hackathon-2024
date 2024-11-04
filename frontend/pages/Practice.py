import streamlit as st
import requests
import pandas as pd


def fetch_cards():
    """Fetch cards from FastAPI endpoint"""
    API_URL = "http://10.154.246.69:8000"  # Replace with your FastAPI server URL

    try:
        response = requests.get(f"{API_URL}/cards/")
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None


def get_card_details(card_row):
    card_details = {}
    card_details["hint"] = card_row["hint"]
    card_details["command"] = card_row["command"]
    return card_details


cards = fetch_cards()

st.title("Cards Dashboard")

# st.sidebar.header("Filters")

# Fetch data button
# if st.button("Fetch Cards"):
# with st.spinner("Fetching cards..."):
if cards:
    # Convert to DataFrame for better display
    df = pd.DataFrame(cards)

    # Display the data
    st.subheader("Cards Data")
    # st.dataframe(df)
    current_card = get_card_details(df.iloc[1])
    st.write(current_card["hint"])
    user_input = st.text_input("Command:")
    if len(user_input) > 0:
        st.write("guessreceived")
    st.write(dir(current_card))
    st.rerun()
    st.experimental_rerun()
