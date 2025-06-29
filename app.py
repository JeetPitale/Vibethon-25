from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# Sample in-memory session data (you can later connect this to a DB)
session_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    return jsonify(session_history)

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.get_json()
    question = data.get('question', '')
    
    # Simulated AI response
    answer = f"Air is a mixture of gases like nitrogen and oxygen. You asked: '{question}'"

    session = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    session_history.append(session)

    return jsonify({"answer": answer})

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    topic = data.get('topic_or_answer', '')

    # Simulated quiz question and answer (based on the topic)
    quiz = {
        "question": f"What is the main component of air?",
        "options": ["Nitrogen", "Oxygen", "Carbon Dioxide", "Hydrogen"],
        "answer": "Nitrogen"
    }

    return jsonify(quiz)

@app.route('/log_quiz_attempt', methods=['POST'])
def log_quiz_attempt():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    quiz_attempt = data.get('quiz_attempt')

    # Add to session history
    session = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "quiz_attempt": quiz_attempt
    }
    session_history.append(session)

    return jsonify({"message": "Quiz attempt logged successfully."})

if __name__ == '__main__':
    app.run(debug=True)
