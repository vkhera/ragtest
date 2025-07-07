import requests

OLLAMA_URL = "http://localhost:11434"

def query_ollama(prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json().get("response", "")
