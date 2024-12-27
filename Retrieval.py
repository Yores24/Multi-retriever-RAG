from langchain.retrievers import (
    ContextualCompressionRetriever,
   
    MergerRetriever,
)
from langchain.retrievers.document_compressors import DocumentCompressorPipeline

from langchain.vectorstores import FAISS
from langchain_community.document_transformers import EmbeddingsRedundantFilter



def retrieval(vector_store,embeddings):
    # Define Individual Retrievers
    retriever_tns = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5, "include_metadata": False}
    )

    retriever_ad = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "include_metadata": False}
    )

    # Merge Retrievers
    lotr = MergerRetriever(retrievers=[retriever_tns, retriever_ad])

    # Add Embedding-Based Filtering
    filter = EmbeddingsRedundantFilter(embeddings=embeddings)

    # Create a Document Compression Pipeline
    pipeline = DocumentCompressorPipeline(transformers=[filter])

    # Contextual Compression Retriever
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline, base_retriever=lotr
    )
    return compression_retriever

# Function to Use the Compression Retriever
def retrieve_documents(query,compression_retriever):
    return compression_retriever.get_relevant_documents(query)

