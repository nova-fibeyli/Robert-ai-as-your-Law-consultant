# Robert-Ai: Empathic Law Robo Support

## Overview

Robert-Ai is an innovative application designed to provide empathetic emotional support. This bot combines cutting-edge technologies to deliver meaningful and helpful interactions for users seeking companionship and understanding. And with new update he is now your in pocket law-consultant!

## Key Features

- **Python-Powered**: Developed using Python, a versatile and robust programming language.
- **MongoDB Integration**: Utilizes MongoDB to store and retrieve conversational data for context-aware responses.
- **Streamlit Framework**: A user-friendly interface built with Streamlit for seamless interaction.
- **Ollama Integration**: Incorporates Ollama's advanced AI models for generating empathetic and human-like responses.
- **File Upload & Document Querying**:
  - Allows users to upload documents and ask questions about their content.
  - Supports **.txt, .pdf, and .docx** file uploads.
  - Extracts and processes content to provide **relevant responses** within the document's context.
  - Enhances user experience by offering meaningful document-based insights.
  - Provides clear incights and consulatation regarding juridical system of Kazakhstan

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nova-fibeyli/Robert-ai-as-your-Law-consultant.git
   cd Robert-ai-as-your-Law-consultant
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application by running:

   ```bash
   streamlit run C:\law_consultant_robert\constitution_app\src\app.py
   ```

2. Enter your questions or messages, and Robert-Ai will respond empathetically.
3. **Upload files** (.txt, .pdf, .docx) and ask **questions** about their content.
4. Retrieve **document-specific responses** and engage with uploaded materials interactively.

Also if you want more precise answers you could run:
streamlit run C:\law_consultant_robert\constitution_app\src\app_alt.py

## Technologies Used

- **Python**: The backbone of this application for efficient scripting and development.
- **MongoDB**: A NoSQL database to store conversation history and facilitate dynamic responses. Log in into: https://account.mongodb.com/account/login?signedOut=true. In order to check database connection and all logs.
- **Streamlit**: An interactive and intuitive framework for creating a friendly UI.
- **Ollama**: Advanced AI language models that enhance Robert-Ai's conversational capabilities.
- **PyMuPDF (fitz)**: Extracts text from uploaded PDF documents.
- **pymongo**: Enables communication between Robert-Ai and MongoDB.
- **json**: Used to create a custom dataset based on constitution of Republic Kazakhstan.

## License

This project is licensed under the Apche 2.0  License.

## Repository

Visit the project repository at [Robert-Ai GitHub Repository](https://github.com/nova-fibeyli/Robert-ai-as-your-Law-consultant.git).
