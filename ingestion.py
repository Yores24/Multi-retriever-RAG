import os
from langchain.document_loaders import PyPDFLoader

def load_files(data_folder):
    files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.pdf')]
    docs = []
    for file in files:
        try:
            loader = PyPDFLoader(file)  # Use PyPDFLoader for PDF files
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading file {file}: {e}")
    return docs


from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)


import os
from langchain.vectorstores import FAISS

def store_in_vector_store(embeddings, docs):
    index_path = "faiss_index"

    # Check if the FAISS index exists
    if os.path.exists(index_path):
        # Load the FAISS vector store from the disk
        vector_store = FAISS.load_local(index_path, embeddings,allow_dangerous_deserialization=True)
        print("FAISS index loaded from disk.")
    else:
        # If it doesn't exist, create a new vector store from documents
        vector_store = FAISS.from_documents(docs, embeddings)
        # Save it for future use
        vector_store.save_local(index_path)
        print("FAISS index created and saved to disk.")
    
    return vector_store