from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Flask
app = Flask(__name__)
CORS(app)  # ✅ Full CORS support

# Cohere API Key
COHERE_API_KEY = "9UdObC5ScVqsabnce7bUwYNyZXOTZuOi02sK6PyB"  
co = cohere.Client(COHERE_API_KEY)

# Root route
@app.route('/')
def home():
    return 'AthliZen AI Server (Cohere) is running.'

# Chat endpoint
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        print("📩 Question from frontend:", question)

        if not question:
            return jsonify({'answer': "Please ask a valid question."}), 400

        # ✅ Provide context via initial chat history
        response = co.chat(
            model='command-r',
            message=question,
            temperature=0.7,
            chat_history=[
                {
                    "role": "SYSTEM",
                    "message": (
                        "You are a CIS professional a-levels/Igcse tutor, you only answer to questions related to a-levels/Igcse Physics/Maths."
                    )
                }
            ]
        )

        answer = response.text.strip()
        print("🤖 AI Response:", answer)
        return jsonify({'answer': answer})

    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()
        return jsonify({'answer': f"Error: {str(e)}"}), 500

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
