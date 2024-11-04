import streamlit as st

# import requests
# import pandas as pd
from streamlit.components.v1 import html


pageHtml = """
    <style>
        body {
            width: 100vw;
            height: 100vh;
        }

        #containerDiv {

            position: relative;
            top: 50%;
            left: 50vw;
            transform: translate(-25%, -50%);
            color: white;
        }

        #currentCard {

            perspective: 1000px;
            width: 500px;
            height: 300px;
        }

        .card {
            color: black;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            transition: transform 0.6s;
            position: relative;
        }

        #cardHint,
        #cardAnswer {
            width: 100%;
            height: 100%;
            position: absolute;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #cardHint {
            background-color: #ffeead;
        }

        #cardAnswer {
            background-color: #96ceb4;
            transform: rotateY(180deg);
        }
        #cardAnswer.incorrect {
            background-color: #ff6969;
        }

        .flip {
            transform: rotateY(180deg);
        }

        .cardSide {
            text-align: center;
        }

        #userInput {
            margin: 50px;
        }
    </style>
    <div id="containerDiv">
        <div id="currentCard" class="card">
            <div id="cardHint" class="cardSide"></div>
            <div id="cardAnswer" class="cardSide"></div>
        </div>
        <label for="userInput">Answer:</label>
        <input type="text" id="userInput" size="40" onen />
        <div id="resultDiv"></div>
    </div>
    <script>
        // Replace 'http://10.154.246.69:8000' with the actual endpoint you need to fetch from
        const url = 'http://10.154.246.69:8000/cards';

        let resultDiv = document.getElementById("resultDiv");
        let allCards = [];
        let currentIndex = 0;
        let clearOnEnter = false;
        cardEl = document.getElementById("currentCard");
        hintEl = document.getElementById("cardHint");
        answerEl = document.getElementById("cardAnswer");
        function loadCard() {
            currentCard = allCards[currentIndex];
            currentIndex = currentIndex + 1;
            console.log("current card:", currentCard);
            hintEl.innerText = currentCard.hint;
            answerEl.innerText = currentCard.command;
        }
        function flipCard() {
            cardEl.classList.toggle('flip');
        }
        function sleep(ms = 0) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        inputField = document.getElementById("userInput");
        async function resetCard() {

            flipCard();
            await sleep(300);
            loadCard();
            answerEl.classList.remove("incorrect");
            clearOnEnter = false;
            resultDiv.innerHTML = "";
            inputField.value = "";
        }
        inputField.addEventListener("keypress", function (event) {
            // If the user presses the "Enter" key on the keyboard
            if (event.key === "Enter") {
                // Cancel the default action, if needed

                event.preventDefault();
                console.log(inputField.value);
                if (inputField.value == currentCard.command) {
                    resultDiv.innerHTML = "CORRECT!";
                }
                else {
                    resultDiv.innerHTML = "THAT'S NOT CORRECT!";
                    answerEl.classList.add("incorrect");
                }
                if (clearOnEnter) {
                    resetCard();
                }
                else {
                    flipCard();
                    clearOnEnter = true;
                }
            }
        });
        function shuffleArray(array) {
            for (var i = array.length - 1; i >= 0; i--) {
                var j = Math.floor(Math.random() * (i + 1));
                var temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
            return array;
        }
        async function getCards() {
            // Use the fetch API to get data from the server
            allCards = await fetch(url)
                .then(response => {
                    // Check if the request was successful
                    if (!response.ok) {
                        // Handle the error if not successful
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    // Parse the response body as JSON if the request was successful
                    return response.json();
                })
                .then(data => {
                    // Now you have your data in the 'data' variable
                    // console.log(data);

                    // You can now work with your data or assign it to another variable
                    const fetchedData = data;
                    return fetchedData;
                    // Do something with 'fetchedData'
                })
                .catch(error => {
                    // Handle any errors that occurred during the fetch
                    console.error('Fetch error:', error);
                });
        }
        async function main() {
            await getCards();
            // console.log("allCards", allCards);
            allCards = shuffleArray(allCards);
            // console.log("allCards", allCards);
            loadCard();
        }
        main();
    </script>
"""
html(pageHtml)
st.markdown("<style>iframe{height: 100vh !important;}</style>", unsafe_allow_html=True)

# def fetch_cards():
#     """Fetch cards from FastAPI endpoint"""
#     API_URL = "http://10.154.246.69:8000"  # Replace with your FastAPI server URL

#     try:
#         response = requests.get(f"{API_URL}/cards/")
#         response.raise_for_status()  # Raise an exception for bad status codes
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching data: {str(e)}")
#         return None


# def get_card_details(card_row):
#     card_details = {}
#     card_details["hint"] = card_row["hint"]
#     card_details["command"] = card_row["command"]
#     return card_details


# cards = fetch_cards()

# st.title("Cards Dashboard")

# # st.sidebar.header("Filters")

# # Fetch data button
# # if st.button("Fetch Cards"):
# # with st.spinner("Fetching cards..."):
# if cards:
#     # Convert to DataFrame for better display
#     df = pd.DataFrame(cards)

#     # Display the data
#     st.subheader("Cards Data")
#     # st.dataframe(df)
#     current_card = get_card_details(df.iloc[1])
#     st.write(current_card["hint"])
#     user_input = st.text_input("Command:")
#     if len(user_input) > 0:
#         st.write("guessreceived")
#     st.write(dir(current_card))
#     st.rerun()
#     st.experimental_rerun()
