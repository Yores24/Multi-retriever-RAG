import streamlit as st
from ingestion import load_files, chunk_documents, store_in_vector_store
from Retrieval import retrieval, retrieve_documents
from Generation import generation,update_chat_history
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain.vectorstores import FAISS
import os
import getpass
from dotenv import load_dotenv
load_dotenv()
# Set up Streamlit page
st.set_page_config(page_title="Chatbot", layout="wide")
st.title("Multi-Retriever Chat Bot")

# Sidebar for settings
st.sidebar.title("Chatbot Settings")
data_folder = st.sidebar.text_input("Data Folder Path", value="./data")
st.sidebar.markdown("**Model Configuration**")
embedding_model_1 = st.sidebar.text_input("Embedding Model (Indexing)", value="models/embedding-model")
embedding_model_2 = st.sidebar.text_input("Embedding Model (Retrieval)", value="models/embedding-model2")
llm_model_name = st.sidebar.text_input("Chat LLM Model", value="mistral-large-latest")
initialize_button = st.sidebar.button("Initialize Chatbot")

# Initialize components
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# api_key = getpass.getpass("Enter your Mistral API key: ")

# Set the environment variable for the Mistral API key
# os.environ["MISTRAL_API_KEY"] = api_key

# Check if the key is set correctly


# Chatbot Initialization
if initialize_button:
    try:
        # Load and process documents
        embeddings_indexing = HuggingFaceEmbeddings(model_name=embedding_model_1)
        embeddings_retrieval = HuggingFaceEmbeddings(model_name=embedding_model_2)
        st.write("Checking vector store is available")
        if os.path.exists("faiss_index"):
        # Load the FAISS vector store from the disk
            st.write("Loading local store")
            vector_store = FAISS.load_local("faiss_index", embeddings_indexing,allow_dangerous_deserialization=True)
        else:    
            st.write("Loading documents...")
            docs = load_files(data_folder)
            st.write(f"Loaded {len(docs)} documents.")

            st.write("Chunking documents...")
            chunks = chunk_documents(docs)

            # Store in vector store
            st.write("Creating vector store...")
            vector_store = store_in_vector_store(embeddings_indexing, chunks)

        # Set up retriever
        st.write("Setting up retriever...")
        compression_retriever = retrieval(vector_store, embeddings_retrieval)
        # Set up chat model and generation pipeline
        st.write("Initializing chat model...")
        api_key = os.getenv("MISTRAL_API_KEY") 
        chatllm = ChatMistralAI(model=llm_model_name, temperature=0, max_retries=2,api_key=api_key,max_tokens=100)
        qa_chain = generation(compression_retriever, chatllm)

        st.session_state.qa_chain = qa_chain
        st.success("Chatbot initialized successfully!")
    except Exception as e:
        st.error(f"Error during initialization: {e}")
 
st.write("### Chat with the PDF data:")
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)

user_input = st.text_input("Your question:", "")
 
if st.button("Ask") and user_input:
    if st.session_state.qa_chain:
        try:
            st.write("Fetching response...")
            qa_chain = st.session_state.qa_chain
            response = qa_chain(user_input)["answer"]

            # Update chat history
            st.session_state['chat_history'] = update_chat_history(st.session_state['chat_history'], user_input, response)

            st.chat_message("user").write(user_input)
            st.chat_message("assistant").write(response)
            # Display chat history
            # for sender, message in st.session_state.chat_history:
            #     if sender == "You":
            #         st.markdown(f"**{sender}:** {message}" )
            #     else:
            #         st.markdown(f"_**{sender}:** {message}_")
            # st.chat_message("user").write(user_input)
            # st.chat_message("assistant").write(response)
        except Exception as e:
            st.error(f"Error fetching response: {e}")
    else:
        st.warning("Please initialize the chatbot first.")
