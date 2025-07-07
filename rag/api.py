from flask import Flask, request, jsonify
from rag.ollama_client import query_ollama
import chromadb
from chromadb.config import Settings

def start_api():
    app = Flask(__name__)
    client = chromadb.Client(Settings(persist_directory="VectorDB/ChromaDB"))
    collection = client.get_or_create_collection("pdf_docs")

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        user_input = data.get('user_input', '')
        results = collection.query(query_texts=[user_input], n_results=3)
        context = " ".join([doc for doc in results.get('documents', [[]])[0]])
        prompt = f"Context: {context}\nQuestion: {user_input}"
        answer = query_ollama(prompt)
        return jsonify({'answer': answer})

    app.run(port=5001, debug=True)
