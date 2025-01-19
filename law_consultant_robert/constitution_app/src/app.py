import json
import streamlit as st
from llama_index.core.llms import ChatMessage
from pymongo import MongoClient
import logging
import time
import pandas as pd
import fitz  # PyMuPDF for PDF processing

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://AdvancedProgramming:AdvancedProgramming@cluster0.uemob.mongodb.net/test?retryWrites=true&w=majority")
db = client.support_bot
dialogue_collection = db.dialogues

# Load Constitution JSON Dataset
json_path = "src/dataset/constitution.json"  # Update this to the correct path if needed
try:
    with open(json_path, "r", encoding="utf-8") as f:
        constitution = json.load(f)
        logging.info("Constitution JSON file loaded successfully.")
except FileNotFoundError:
    logging.error(f"Constitution JSON file not found: {json_path}")
    constitution = {}  # Fallback to an empty dictionary if the file is missing
except Exception as e:
    logging.error(f"Error loading Constitution JSON file: {str(e)}")
    constitution = {}  # Fallback to an empty dictionary on error

# Function to load dataset into MongoDB
def load_dataset():
    try:
        train_data = pd.read_csv("EmpatheticDialogues/train.csv")
        dialogues = train_data[["prompt", "utterance"]].drop_duplicates().dropna()
        dialogue_collection.insert_many(dialogues.to_dict(orient="records"), ordered=False)
        logging.info("EmpatheticDialogues dataset loaded into MongoDB.")
    except Exception as e:
        logging.info("Dataset already exists or encountered an error.")

# Load the EmpatheticDialogues dataset into MongoDB
load_dataset()

# Function to find response from MongoDB
def find_response(user_input):
    result = dialogue_collection.find_one({"prompt": {"$regex": user_input, "$options": "i"}})
    return result["utterance"] if result else None

# Function to store query and response in MongoDB
def store_query_response(user_input, assistant_response):
    dialogue_collection.insert_one({
        "prompt": user_input,
        "utterance": assistant_response,
        "timestamp": time.time()
    })
    logging.info(f"Stored query and response in MongoDB: {user_input} - {assistant_response}")

# Function to handle file upload
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "pdf":
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            file_text = "\n".join([page.get_text("text") for page in doc])
        else:
            file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        return file_text[:500]  # Preview the first 500 characters
    return ""

# Stream chat logic, integrating the Constitution dataset
def stream_chat(model, messages):
    try:
        user_input = messages[-1].content if messages else ""
        if not user_input:
            return "I didn’t catch that. Could you say it again?"

        # Attempt to find the article number in the user input
        for article in constitution.get("articles", []):
            if f"article {article['number']}".lower() in user_input.lower():
                return f"Article {article['number']}: {article['content']}"

        # Fallback to search the content of articles for keywords
        for article in constitution.get("articles", []):
            if any(word in user_input.lower() for word in article["content"].lower().split()):
                return f"Related to Article {article['number']}: {article['content']}"

        # Default fallback: Check MongoDB for a response
        mongo_response = find_response(user_input)
        if mongo_response:
            return mongo_response

        return "Sorry, I couldn't find relevant information in the Constitution or database."

    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        return "An error occurred. Please try again later."

# Main app function
def main():
    st.title("Chat with Robert ['-']")
    logging.info("App started")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    logging.info(f"Model selected: {model}")

    for message in reversed(st.session_state.messages):
        with st.chat_message(message.role):
            st.write(message.content)

    prompt = st.text_input("Enter your question:", key="user_prompt")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
    send_button = st.button("Send")

    if send_button:
        file_text = handle_file_upload(uploaded_file)
        full_prompt = f"{prompt}\n\n[File Content Preview]: {file_text}" if file_text else prompt

        if not full_prompt.strip():
            st.error("Please enter text or upload a file.")
        else:
            st.session_state.messages.append(ChatMessage(role="user", content=full_prompt))
            logging.info(f"User input: {full_prompt}")

            with st.chat_message("assistant"):
                response_container = st.empty()
                response_text = ""
                start_time = time.time()

                with st.spinner("Generating response..."):
                    try:
                        response_message = stream_chat(model, st.session_state.messages)
                        response_text = response_message if response_message else "I'm sorry, I couldn't process your request."

                        st.session_state.messages.append(ChatMessage(role="assistant", content=response_text))
                        logging.info(f"Response: {response_text}")

                        store_query_response(full_prompt, response_text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
