# ai_response.py
import requests
import json
import os

# Placeholder for your OpenAI API Key
# It's recommended to load this from environment variables in a production setup

API_KEY = os.getenv("API_KEY")
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def get_ai_response(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    """
    Sends a text prompt to the OpenAI API and returns the AI's response.

    Args:
        prompt (str): The user's question or input.
        model (str): The OpenAI model to use (e.g., "gpt-3.5-turbo", "gpt-4").
        temperature (float): Controls randomness. Lower values are more deterministic.

    Returns:
        str: The AI's generated text response, or an error message.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "***":
        return "Error: OpenAI API Key is not set. Please set the OPENAI_API_KEY environment variable or update it in ai_response.py."

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are Exam Whisperer, an AI assistant specialized in explaining educational topics concisely and accurately."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 500 # Adjust as needed based on expected response length
    }

    try:
        response = requests.post(OPENAI_API_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        response_data = response.json()
        
        # Extract the AI's message
        if response_data and 'choices' in response_data and len(response_data['choices']) > 0:
            return response_data['choices'][0]['message']['content']
        else:
            return "Error: Unexpected response format from OpenAI API."

    except requests.exceptions.RequestException as e:
        return f"Error communicating with OpenAI API: {e}"
    except json.JSONDecodeError:
        return "Error: Could not decode JSON response from OpenAI API."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    # Example usage:
    # To test this module, replace "YOUR_OPENAI_API_KEY_HERE" with your actual key
    # or set the environment variable OPENAI_API_KEY
    if OPENAI_API_KEY == "**":
        print("Please set your OPENAI_API_KEY in ai_response.py or as an environment variable to test this module.")
    else:
        question = "Explain the concept of renewable energy sources."
        ai_answer = get_ai_response(question)
        print(f"Question: {question}\nAI Answer: {ai_answer}")

        question_brief = "Summarize the water cycle."
        ai_answer_brief = get_ai_response(question_brief, model="gpt-3.5-turbo")
        print(f"\nQuestion: {question_brief}\nAI Answer: {ai_answer_brief}")
