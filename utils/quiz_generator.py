# quiz_generator.py
import requests
import json
import os

# Placeholder for your OpenAI API Key for quiz generation
OPENAI_API_KEY_QUIZ = os.environ.get("OPENAI_API_KEY_QUIZ", "***")
OPENAI_QUIZ_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def generate_quiz(topic_or_answer: str) -> dict:
    """
    Generates a multiple-choice quiz based on a given topic or answer using the OpenAI API.

    Args:
        topic_or_answer (str): The text or topic from which to generate a quiz.

    Returns:
        dict: A dictionary containing the quiz question, options, and correct answer,
              or an error dictionary.
        Example structure:
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "answer": "Paris"
        }
    """
    if not OPENAI_API_KEY_QUIZ or OPENAI_API_KEY_QUIZ == "***":
        return {"error": "OpenAI API Key for quiz generation is not set. Please set the OPENAI_API_KEY_QUIZ environment variable or update it in quiz_generator.py."}

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY_QUIZ}",
        "Content-Type": "application/json"
    }

    # Craft a prompt that instructs the AI to generate a quiz in a specific JSON format
    prompt_template = f"""
    Generate a single multiple-choice question (MCQ) quiz based on the following text/topic.
    The quiz should have:
    1. A 'question' field (string).
    2. An 'options' field (an array of 4 strings).
    3. An 'answer' field (string) which is one of the options.
    Ensure the answer is one of the provided options.

    Respond ONLY with a JSON object. Do not include any other text or markdown.
    Ensure the JSON is perfectly parsable and follows the structure exactly.

    Text/Topic for Quiz:
    "{topic_or_answer}"
    """

    payload = {
        "model": "gpt-3.5-turbo", # Recommended for cost-efficiency and good performance
        "messages": [
            {"role": "system", "content": "You are a quiz master. Generate quizzes in strict JSON format."},
            {"role": "user", "content": prompt_template}
        ],
        "temperature": 0.7, # Can be adjusted for more creative/diverse options
        "max_tokens": 200,  # Max tokens for the quiz generation JSON (adjust if quizzes get longer)
        "response_format": {"type": "json_object"} # Crucial for getting JSON output
    }

    raw_content = "" # Initialize raw_content to an empty string

    try:
        response = requests.post(OPENAI_QUIZ_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        response_data = response.json()
        
        if response_data and 'choices' in response_data and len(response_data['choices']) > 0:
            raw_content = response_data['choices'][0]['message']['content']
            # Attempt to parse the JSON content
            quiz_data = json.loads(raw_content)
            
            # Basic validation of the quiz structure
            if all(k in quiz_data for k in ["question", "options", "answer"]) and \
               isinstance(quiz_data["options"], list) and len(quiz_data["options"]) == 4 and \
               quiz_data["answer"] in quiz_data["options"]: # Ensure answer is one of the options
                return quiz_data
            else:
                return {"error": "Generated quiz data has an invalid format or invalid answer.", "raw_response": raw_content}
        else:
            return {"error": "Unexpected response format from OpenAI quiz API.", "response_data": response_data}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with OpenAI API for quiz: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"Could not decode JSON quiz response: {e}. Raw content: {raw_content}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred during quiz generation: {e}"}

if __name__ == '__main__':
    # Example usage:
    # To test this module, replace "YOUR_OPENAI_API_KEY_HERE" with your actual key
    # or set the environment variable OPENAI_API_KEY_QUIZ
    if OPENAI_API_KEY_QUIZ == "***":
        print("Please set your OPENAI_API_KEY_QUIZ in quiz_generator.py or as an environment variable to test this module.")
    else:
        # Example 1: Quiz based on a topic
        quiz = generate_quiz("The process of photosynthesis, which converts light energy into chemical energy.")
        print("\nQuiz 1 (Photosynthesis):")
        print(json.dumps(quiz, indent=2))

        # Example 2: Quiz based on an AI answer (e.g., from ai_response.py)
        sample_ai_answer = "Gravity is a fundamental force of nature that attracts any objects with mass or energy. It is responsible for phenomena such as the falling of apples, the orbits of planets, and the structure of galaxies."
        quiz_from_answer = generate_quiz(sample_ai_answer)
        print("\nQuiz 2 (Gravity):")
        print(json.dumps(quiz_from_answer, indent=2))

        # Example with a challenging input for quiz generation
        quiz_complex = generate_quiz("Explain string theory in one paragraph.")
        print("\nQuiz 3 (String Theory):")
        print(json.dumps(quiz_complex, indent=2))
