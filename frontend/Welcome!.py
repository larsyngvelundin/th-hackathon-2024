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


def main():
    st.title("Welcome to the Practice session!")
    st.text("")
    st.divider()
    st.text(
        "Here you can practice (almoast) all the stuff you need to know about programing!"
    )
    st.header("")

    intro_col1, intro_col2, intro_col3 = st.columns(3)
    with intro_col1:
        st.markdown(
            """
        <a href="http://localhost:8501/Practise" target="_self">
            <button style="
                background-color: #4CAF50;
                color: white;
                padding: 14px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;">
                Go to Practise
            </button>
        </a>
    """,
            unsafe_allow_html=True,
        )
    with intro_col2:
        st.markdown(
            """
        <a href="http://localhost:8501/Add_card" target="_self">
            <button style="
                background-color: #4CAF50;
                color: white;
                padding: 14px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;">
                Go to Add Card
            </button>
        </a>
    """,
            unsafe_allow_html=True,
        )
    with intro_col3:
        st.markdown(
            """
        <a href="http://localhost:8501/Remove_card" target="_self">
            <button style="
                background-color: #4CAF50;
                color: white;
                padding: 14px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;">
                Go to Remove Card
            </button>
        </a>
    """,
            unsafe_allow_html=True,
        )
    st.title("")
    st.divider()

    st.text("If you want to see all the data in the database, press the button below.")
    st.text("")
    # Fetch data button
    if st.button("The BIG reveile"):
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
