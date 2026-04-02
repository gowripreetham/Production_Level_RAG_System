from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_answer(question, context):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {
                "role": "system",
                "content": "You are a research assistant. Answer the user's question using ONLY the provided context excerpts. For every claim cite the source using [Source: filename]. If you truly cannot find relevant information in the context, say so briefly."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    # print("RAW RESPONSE:", response)
    return response.choices[0].message.content