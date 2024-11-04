import streamlit as st
import requests
import pandas as pd

def fetch_cards():
    """Fetch cards from FastAPI endpoint"""
    API_URL = "http://10.154.246.69:8000"  # Replace with your FastAPI server URL
    
    try:
        response = requests.get(
            f"{API_URL}/cards/"            
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def main():
    st.title("Cards Dashboard")
    
    # Sidebar controls
    st.sidebar.header("Filters")


    
    # Fetch data button
    if st.button("Fetch Cards"):
        with st.spinner("Fetching cards..."):
            cards = fetch_cards()
            
            if cards:
                # Convert to DataFrame for better display
                df = pd.DataFrame(cards)
                
                # Display the data
                st.subheader("Cards Data")
                st.dataframe(df)
                
                
if __name__ == "__main__":
    main()