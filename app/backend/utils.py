import os
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv

load_dotenv()

def get_index():
    client = QdrantClient(host="localhost", port=6333)

    # Check which collections is used
    try:
        response = client.get_collections()
        print("Successfully connected to Qdrant.")
        print("Available collections:", response, sep="\n")
    except Exception as e:
        print("Failed to connect to Qdrant:", e)
    
    # create embedding model to embed query locally
    embed_model = HuggingFaceEmbedding(model_name="KhoaUIT/Halong-UIT-R2GQA", max_length=512)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="corpus_halong-trained",
        enable_hybrid=True
    )
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embed_model
    )
    
    return index

def get_llm():
    return GoogleGenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-2.5-flash-preview-04-17",
        temperature=0.0
    )
