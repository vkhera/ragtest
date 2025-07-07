
from rag.ollama_client import query_ollama
import chromadb
from chromadb.utils import embedding_functions

def cli_chat():
    client = chromadb.PersistentClient(path="VectorDB/ChromaDB")
    ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection("pdf_docs", embedding_function=ef)
    print("Welcome to the RAG CLI chat. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        # Retrieve relevant docs
        #print("Retrieving relevant documents for:", user_input)
        results = collection.query(query_texts=[user_input], n_results=3)
        #print("Results:", results)
        context = " ".join([doc for doc in results.get('documents', [[]])[0]])
        #print("Context:", context)
        prompt = f"Context: {context}\nQuestion: {user_input}"
        answer = query_ollama(prompt)
        print(f"Ollama: {answer}")
