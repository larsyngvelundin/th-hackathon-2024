import streamlit as st
import requests
import json


def create_card(field1: str, field2: str):
    """Create a new card via FastAPI endpoint"""
    API_URL = "http://10.154.246.69:8000"

    # Create the card data structure matching your Card model
    card_data = {
        "field1": field1,  # Replace field1 with your actual field name
        "field2": field2,  # Replace field2 with your actual field name
    }

    try:
        response = requests.post(
            f"{API_URL}/cards/",
            json=card_data,  # This will be converted to a Card object by FastAPI
        )
        response.raise_for_status()
        return True, "Card created successfully!", response.json()
    except requests.exceptions.RequestException as e:
        return False, f"Error creating card: {str(e)}", None


st.header("Add New Card")

with st.form("add_card_form"):
    # Update these field names to match your Card model
    field1 = st.text_input("Field 1")  # Replace with your actual field name
    field2 = st.text_input("Field 2")  # Replace with your actual field name

    submit = st.form_submit_button("Create Card")

    if submit:
        success, message, new_card = create_card(field1, field2)
        if success:
            st.success(message)
            st.json(new_card)
        else:
            st.error(message)
