# RAG System — Project Decisions & Progress

## Phase 1: Foundation

### What is this project?
This is a Production Level RAG system built for a Professor at SJSU. 
The system helps him get answers to questions from his past research 
papers. This version considers research papers from 2024 to 2026 
(8 papers total). Project inspired by a YouTube video by Aishwarya 
Srinivasan.

**Domain choice:** Professor's own research papers were chosen because 
he has complete knowledge of the content and can serve as a expert 
evaluator — he knows exactly what questions to ask and whether the 
answers are correct.

### What is a vector embedding?
Vector embeddings are mathematical representations of words, sentences, 
or paragraphs as numbers. Raw text is impossible for machines to process 
directly, so we convert it into vectors. Machines don't understand 
meaning the way humans do — their version of "understanding" is through 
similarity. Cosine similarity measures how close two vectors are in 
N-dimensional space, regardless of their magnitude — only the direction 
matters.

### What did the similarity experiment prove?
Sentences with the same semantic meaning produce high cosine similarity 
scores (close to 1). Unrelated sentences produce low scores (close to 0).

Results:
- Similar sentences ("I'm a man" vs "Me a man"): **0.83**
- Unrelated sentences ("I'm a man" vs "The stock market crashed today"): 
**0.08**

This is the foundation of the entire RAG pipeline. Retrieval only works 
if similarity works — and we proved it does.

### Tech decisions made today:
- Python 3.11.9 via pyenv (upgraded from 3.9.6 for library compatibility)
- Virtual environment: venv
- Embedding model: all-MiniLM-L6-v2 (384 dimensions, fast, good quality)
- Vector similarity: cosine similarity via sentence-transformers util


## Phase 2: PDF Extraction & Cleaning

### Why pymupdf over pdfplumber?
pymupdf produces cleaner continuous text for research papers, handles 
multi-column layouts better, and is significantly faster. pdfplumber 
preserves visual layout which is useful for tables but not for our 
use case where we need clean readable text for chunking.

### Cleaning rules implemented:
- Remove lines containing `@` (email addresses)
- Remove lines starting with `http` (URLs)
- Remove lines containing `.com` (web addresses)
- Remove lines containing `Published by` (copyright notices)

Rules were kept intentionally conservative. Content is more valuable 
than cleanliness — a little boilerplate in chunks is far less damaging 
than accidentally removing real research content.

### Risk of over-cleaning:
Over-aggressive cleaning risks removing relevant context from the 
extracted text. Lost content cannot be retrieved — meaning the system 
will fail to answer questions about that content entirely. Cleaning 
can always be improved iteratively once the system is working end to end.

### Tool decision:
- PDF extraction: pymupdf (fitz)