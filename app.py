from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # This allows your HTML file to talk to this Python script

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get("message", "")

    # Prepare the payload for Ollama
    payload = {
        "model": MODEL_NAME,
        "prompt": f"You are a helpful medical assistant. User says: {user_message}",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response_data = response.json()
        ai_response = response_data.get("response", "Sorry, I couldn't process that.")
        
        return jsonify({"reply": ai_response})
    
    except Exception as e:
        return jsonify({"reply": f"Error connecting to Ollama: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)