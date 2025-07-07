from flask import Flask, request, jsonify, render_template_string
from rag.ollama_client import query_ollama
import chromadb
from chromadb.config import Settings

app = Flask(__name__)
client = chromadb.Client(Settings(persist_directory="VectorDB/ChromaDB"))
collection = client.get_or_create_collection("pdf_docs")

CHAT_HTML = '''
<!DOCTYPE html>
<html><head><title>RAG Chat</title></head><body>
<h2>RAG Chat</h2>
<form method="post">
  <input name="user_input" autofocus autocomplete="off" style="width: 300px;"/>
  <input type="submit" value="Send"/>
</form>
<div>{{response}}</div>
</body></html>
'''

@app.route('/', methods=['GET', 'POST'])
def chat():
    response = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        results = collection.query(query_texts=[user_input], n_results=3)
        context = " ".join([doc for doc in results.get('documents', [[]])[0]])
        prompt = f"Context: {context}\nQuestion: {user_input}"
        answer = query_ollama(prompt)
        response = f"<b>You:</b> {user_input}<br><b>Ollama:</b> {answer}"
    return render_template_string(CHAT_HTML, response=response)

def start_web():
    app.run(port=5000, debug=True)
