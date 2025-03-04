from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from different origins



# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load the Gemini API key from the .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta3/models/gemini-pro:generateContent"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={"contents": [{"role": "user", "parts": [{"text": user_message}]}]},
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to get a response from the AI model'}), response.status_code
        
        data = response.json()
        bot_reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm not sure how to respond to that.")
        return jsonify({'reply': bot_reply})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
