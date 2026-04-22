from langfuse import get_client
from dotenv import load_dotenv

load_dotenv()

langfuse = get_client()

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