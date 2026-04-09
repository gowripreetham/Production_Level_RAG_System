from openai import OpenAI
from dotenv import load_dotenv
import os
from src.prompt_manager import load_prompt



load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_answer(question, context):
    system_prompt = load_prompt()
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    # print("RAW RESPONSE:", response)
    return response.choices[0].message.content