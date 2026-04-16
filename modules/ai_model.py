from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_explanation(question, subject="General"):
    system_prompt = f"""You are a strict academic tutor for the subject: {subject}.

IMPORTANT RULES:
1. Only answer questions that are related to {subject}.
2. If the question is clearly about a DIFFERENT subject, do NOT answer it. Instead respond with exactly:
   "⚠️ This question seems to be about [detected subject]. Please switch to the [detected subject] tab to get the best answer!"
3. If the question is general or ambiguous, answer it under the context of {subject}.
4. Always explain step by step, clearly for a student."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Explain this step by step: {question}"}
        ]
    )
    return response.choices[0].message.content                          
    