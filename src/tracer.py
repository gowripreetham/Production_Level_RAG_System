from langfuse import get_client
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

langfuse = get_client()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_trace(question: str):
    span = langfuse.start_as_current_observation(
        as_type="span",
        name="rag_query",
        input={"question": question}
    )
    return span

def end_trace(span, answer: str):
    span.__exit__(None, None, None)
    langfuse.flush()

def start_span(parent, name: str, input_data: dict):
    span = langfuse.start_as_current_observation(
        as_type="span",
        name=name,
        input=input_data
    )
    return span

def end_span(span, output_data: dict):
    span.update(output=output_data)
    span.__exit__(None, None, None)

def score_groundedness(question: str, context: str, answer: str) -> float:
    prompt = f"""Think of yourself as a Judge who can evaluate how grounded the given answer is for the given question based on the context given. Give the groundedness score in the range of 0.0 to 1.0. Only return the score nothing else!

Question: {question}

Context: {context}

Answer: {answer}"""

    response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    )

    score = float(response.choices[0].message.content.strip())
    return score