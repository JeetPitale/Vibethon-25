# Vibethon-25

Vibethon-25 is an AI-powered Python application designed for dynamic, intelligent responses. It features modular utilities and prioritizes secure development by avoiding hardcoded secrets.

## 🚀 Features

- 🤖 AI-generated responses
- 🧩 Modular utility functions
- 🔐 Secure secret management using environment variables
- 💬 Easy integration for chatbots, assistants, and automation
- 🧪 Ready for testing and customization

## 🛠️ Tech Stack

- Python 3.10+
- OpenAI API or other AI services
- Built-in `os` module for environment variable handling
- Git & GitHub for version control

## 🧑‍💻 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/JeetPitale/Vibethon-25.git
cd Vibethon-25
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root directory:

```env
API_KEY=your_api_key_here
```

Update your code to use:

```python
import os
api_key = os.getenv("API_KEY")
```

> ✅ **Never hardcode secrets in your files. Always use environment variables.**

## 🧪 Running the Project

Depending on your project structure, run:

```bash
python main.py
```

Or if you're testing specific scripts:

```bash
python utils/ai_response.py
```

## 📁 Project Structure

```
Vibethon-25/
├── utils/
│   └── ai_response.py
├── main.py
├── .env.example
├── README.md
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome!  
Please open an issue first to discuss what you’d like to change.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Credits

Developed by [Jeet Pitale](https://github.com/JeetPitale) as part of Vibethon 2025.
