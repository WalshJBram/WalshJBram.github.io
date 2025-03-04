from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load the Gemini API key from the .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://gemini.googleapis.com/v1/chat"  # Example URL, adjust as needed

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Call Gemini API to get a response (modify as needed for the specific model)
    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={"messages": [{"role": "user", "content": user_message}]}
        )

        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get('reply', 'I am not sure how to respond to that.')
        else:
            bot_reply = "Sorry, there was an error with the AI model."

        return jsonify({'reply': bot_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
