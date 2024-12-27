# Chatbot Application with Mistral AI and Streamlit

### Demo Video

https://github.com/user-attachments/assets/23ff4359-106b-44be-a45f-2924e93778fb




https://github.com/user-attachments/assets/05a9dd3a-9d66-477f-a677-6ae694002fc9



This project is a chatbot application built using Mistral AI's language model, LangChain's conversational retrieval capabilities, and Streamlit for a user-friendly interface. It supports document ingestion, intelligent retrieval, and conversational capabilities with memory.

---

## Features

- **Document Ingestion**: Load and process PDF documents into chunks.
- **Intelligent Retrieval**: Combines multiple retrievers with contextual compression.
- **Conversational Chatbot**: Generates responses using the Mistral AI model with memory to retain chat history.
- **Streamlit Interface**: Provides a user-friendly frontend for interacting with the chatbot.

---

## Installation

### Prerequisites

1. Python 3.8 or higher
2. Mistral AI API key (stored in a `.env` file)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Yores24/Multi-retriever-RAG.git
   cd Multi-retriever-RAG
2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. Install the dependencies:

    ```bash

    pip install -r requirements.txt

4. Add your Mistral API key to a .env file in the root directory:

    MISTRAL_API_KEY=your_api_key_here

5. Run the Streamlit app:

    ```bash

    streamlit run app.py

## Structure
```
Multi-Retriever-Rag
├── .env
│  
├── .gitignore
├── Demo.mp4
├── Generation.py
├── README.md
├── Retrieval.py
├── app.py
├── data
│   ├── c1.pdf
│   ├── c2.pdf
│   ├── c3.pdf
│   ├── c4.pdf
│   └── c5.pdf
├── faiss_index
│   ├── index.faiss
│   └── index.pkl
├── ingestion.py
├── models
│   ├── embedding-model
│   └── embedding-model2
│   
├── notebook
│   └── lotr.ipynb
└── requirements.txt
```
## Usage

-Place your PDF files in the specified data folder.
-Launch the Streamlit app.
-Upload documents and start interacting with the chatbot.
## Requirements

-See requirements.txt for the complete list of dependencies.

## Notes

-Ensure your Mistral API key is valid and has sufficient permissions.
-Large documents may take time to process depending on their size and content.
