import streamlit as st
import requests
import pandas as pd

def fetch_cards(offset=0, limit=100):
    """Fetch cards from FastAPI endpoint"""
    API_URL = "http://10.154.246.69:8000"  # Replace with your FastAPI server URL
    
    try:
        response = requests.get(
            f"{API_URL}/cards/",
            params={"offset": offset, "limit": limit}
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
    limit = st.sidebar.slider("Number of cards to display", 1, 100, 50)
    offset = st.sidebar.number_input("Offset", min_value=0, value=0)
    
    # Fetch data button
    if st.button("Fetch Cards"):
        with st.spinner("Fetching cards..."):
            cards = fetch_cards(offset=offset, limit=limit)
            
            if cards:
                # Convert to DataFrame for better display
                df = pd.DataFrame(cards)
                
                # Display basic stats
                st.subheader("Statistics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Cards Fetched", len(df))
                
                # Display the data
                st.subheader("Cards Data")
                st.dataframe(df)
                
                
if __name__ == "__main__":
    main()