import streamlit as st
import requests
import pandas as pd


def delete_card(card_id: int):
    """Delete a card by ID"""
    API_URL = "http://10.154.246.69:8000"  # Replace with your FastAPI server URL

    try:
        response = requests.delete(f"{API_URL}/cards/{card_id}")
        response.raise_for_status()
        return True, "Card deleted successfully!"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False, "Card not found!"
        return False, f"Error: {str(e)}"
    except requests.exceptions.RequestException as e:
        return False, f"Error connecting to server: {str(e)}"


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


# Add this where you want the delete functionality in your existing page
card_id = st.number_input(
    "Enter Card ID from list below to Delete", min_value=1, step=1
)
if st.button("Delete Card"):
    success, message = delete_card(card_id)
    if success:
        st.success(message)
    else:
        st.error(message)

st.divider()

cards = fetch_cards()

if cards:
    # Convert to DataFrame for better display
    df = pd.DataFrame(cards)

    # Display the data
    st.text("")
    st.dataframe(df)
