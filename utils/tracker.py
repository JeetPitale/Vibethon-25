# tracker.py
import json
import os
from datetime import datetime

# Define the path for the history file relative to where the script is executed
# This ensures it creates 'data' in the same directory as app.py
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def _ensure_data_dir_exists():
    """Ensures that the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def _read_history() -> list:
    """Reads the session history from the JSON file."""
    _ensure_data_dir_exists() # Ensure directory exists before trying to read
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {HISTORY_FILE} is corrupted or empty. Starting with an empty history.")
        # Optionally, you might want to back up or clear the corrupted file
        return []
    except FileNotFoundError:
        # This case should ideally be caught by os.path.exists, but included for robustness
        return []

def _write_history(history_data: list):
    """Writes the session history to the JSON file."""
    _ensure_data_dir_exists() # Ensure directory exists before trying to write
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=4)

def log_session(question: str, answer: str, quiz_attempt: dict = None) -> None:
    """
    Logs a Q&A session and optionally a quiz attempt.

    Args:
        question (str): The user's question.
        answer (str): The AI's answer.
        quiz_attempt (dict, optional): Details of the quiz attempt.
                                      Should include 'quiz_question', 'selected_option', 'correct_answer', 'is_correct'.
                                      Defaults to None.
    """
    session_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "quiz_attempt": quiz_attempt if quiz_attempt else {} # Store an empty dict if no quiz attempt
    }
    
    history = _read_history()
    history.append(session_entry)
    _write_history(history)
    print("Session logged successfully.")

def get_all_sessions() -> list:
    """
    Retrieves all logged Q&A and quiz session history.

    Returns:
        list: A list of dictionaries, each representing a session.
    """
    return _read_history()

def clear_all_sessions():
    """Clears all logged session history."""
    _ensure_data_dir_exists() # Ensure directory exists
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print(f"All sessions cleared from {HISTORY_FILE}.")
    else:
        print("No history file found to clear.")

if __name__ == '__main__':
    # Example Usage:
    # Clear previous runs for a clean test
    print("--- Starting Tracker Demo ---")
    clear_all_sessions()

    # Log some sessions
    log_session(
        question="What is the capital of Canada?",
        answer="The capital of Canada is Ottawa."
    )
    
    quiz_data_1 = {
        "quiz_question": "Which city is the capital of Canada?",
        "options": ["Toronto", "Vancouver", "Ottawa", "Montreal"],
        "selected_option": "Ottawa",
        "correct_answer": "Ottawa",
        "is_correct": True
    }
    log_session(
        question="Tell me about Canadian geography.",
        answer="Canada is a vast country in North America...",
        quiz_attempt=quiz_data_1
    )

    quiz_data_2 = {
        "quiz_question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"],
        "selected_option": "Pablo Picasso",
        "correct_answer": "Leonardo da Vinci",
        "is_correct": False
    }
    log_session(
        question="Explain Renaissance art.",
        answer="Renaissance art emerged in Italy in the 14th century...",
        quiz_attempt=quiz_data_2
    )

    # Retrieve and print all sessions
    sessions = get_all_sessions()
    print("\n--- All Logged Sessions ---")
    if not sessions:
        print("No sessions logged yet.")
    else:
        for i, session in enumerate(sessions):
            print(f"\nSession {i+1}:")
            print(f"  Timestamp: {session['timestamp']}")
            print(f"  Question: {session['question']}")
            print(f"  Answer: {session['answer']}")
            if session['quiz_attempt']:
                print(f"  Quiz Attempt: {json.dumps(session['quiz_attempt'], indent=2)}")
            else:
                print("  Quiz Attempt: None (Q&A only)")

    print("\nAttempting to read from a non-existent file (after clearing):")
    clear_all_sessions()
    empty_sessions = get_all_sessions()
    print(f"Sessions after clearing: {empty_sessions}")

    print("\n--- Tracker Demo Complete ---")
