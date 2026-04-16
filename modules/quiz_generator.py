from groq import Groq
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_quiz(topic, original_question="", subject="General"):
    # Dynamic count based on subject complexity
    count = 5 if subject in ['Mathematics', 'Physics', 'Chemistry'] else 4

    prompt = f"""You are an academic quiz generator for the subject: {subject}.
Based on this specific question, generate exactly {count} multiple choice questions.

Question/Topic: {original_question if original_question else topic}

Rules:
- Questions must be DIRECTLY about the content asked
- Each question must test a different aspect of understanding
- Make options plausible but only one correct
- Questions should range from easy to hard

Return ONLY a JSON array, no markdown, no extra text:
[{{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "answer": "A) ..."}}]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        clean = response.choices[0].message.content.replace("```json","").replace("```","").strip()
        return json.loads(clean)
    except:
        return []