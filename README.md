# AI Multimodal Tutor

AI Multimodal Tutor is a Flask-based educational web app that helps students ask questions in text or image form, get AI-generated explanations, and practice with short quizzes.

## Features

- User signup and login
- Subject-wise tutoring interface
- Text question input
- Image-to-text question input using Tesseract OCR
- AI-generated step-by-step explanations using Groq
- Auto-generated multiple-choice quiz for practice
- Recent chat history saved per user in SQLite
- Voice input support in the browser with Web Speech API

## Tech Stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Groq API
- pytesseract
- Pillow
- NLTK
- spaCy
- HTML/CSS/JavaScript

## Project Structure

```text
AI_TUTOR/
|-- README.md
|-- ai_tutor/
|   |-- app.py
|   |-- models.py
|   |-- modules/
|   |   |-- ai_model.py
|   |   |-- nlp_processor.py
|   |   |-- ocr.py
|   |   `-- quiz_generator.py
|   `-- templates/
|       |-- index.html
|       |-- login.html
|       `-- signup.html
```

## How It Works

1. A user signs up or logs in.
2. The user selects a subject and enters a text question or uploads an image.
3. If an image is uploaded, OCR extracts readable text from it.
4. The app sends the question to Groq for a step-by-step explanation.
5. The app extracts a topic and generates a short quiz.
6. The question, explanation, quiz, and topic are saved in chat history.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/23wh1a0524/AI_MULTI_MODAL_TUTOR.git
cd AI_MULTI_MODAL_TUTOR
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask flask-login flask-sqlalchemy werkzeug groq python-dotenv pytesseract pillow nltk spacy
python -m spacy download en_core_web_sm
```

### 4. Add environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Install Tesseract OCR

Install Tesseract OCR on Windows and make sure this path exists:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If your installation path is different, update it in:

`ai_tutor/modules/ocr.py`

### 6. Run the app

```bash
cd ai_tutor
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Demo Video Link
-[Watch Project Execution Video](https://drive.google.com/file/d/17yvB2c7TzW-lq-3jBBPS7iG2Rrzbua9y/view?usp=drive_link)

## Notes

- The app stores data in `tutor.db` using SQLite.
- Uploaded images are stored in the `uploads/` folder created at runtime.
- NLTK resources are downloaded automatically when the app starts.
- A valid Groq API key is required for explanation and quiz generation.

## Future Improvements

- Add `requirements.txt`
- Add password validation and stronger secret management
- Add admin or teacher dashboard
- Add deployment instructions for Render or Railway
- Add unit tests and API tests

## Author

Developed as an AI-powered student tutoring project using OCR, NLP, and LLM-based explanation generation.
