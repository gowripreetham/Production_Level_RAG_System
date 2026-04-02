from src.extractor import extract_text_from_pdf
from src.chunker import chunk_text
from src.embedder import store_chunks
import os

DOCS = "/Users/gowripreetam/Desktop/RAG-P/rag-professor/data"

pdf_files = sorted([f for f in os.listdir(DOCS) if f.endswith(".pdf")])

for pdf_file in pdf_files:
    pdf_path = os.path.join(DOCS, pdf_file)
    extracted_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text("\n".join(extracted_text))
    store_chunks(chunks, pdf_file)