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


## Phase 3: Vector Storage with ChromaDB

### Why ChromaDB?
ChromaDB was chosen over Weaviate because it is beginner-friendly and 
perfect for local personal projects. Weaviate is designed for products 
at scale and would add unnecessary infrastructure complexity at this 
stage. Each chunk is stored with four things: the chunk text, its 
embedding vector, metadata (source filename), and a unique id.

### Duplicate chunk bug & fix
When running main.py multiple times, all 871 chunks were being added 
again on every run — creating silent duplicates in the database. Fixed 
by checking if the first chunk of each paper (e.g. "1.pdf_chunk_0") 
already exists in the collection before adding anything. If it exists, 
the paper is skipped entirely.

### PersistentClient vs Client
`chromadb.Client()` stores data in memory only — wiped when the Python 
session ends. Switched to `chromadb.PersistentClient(path="chroma_db")` 
which saves the database to a local folder permanently. The `chroma_db/` 
folder is added to `.gitignore` since databases should never be pushed 
to GitHub.


## Phase 4: Query & Relevance Filtering

### How ChromaDB measures similarity
ChromaDB uses cosine distance, not cosine similarity. The scale is 
0 to 2 where 0 means identical and 2 means completely opposite. 
This is the reverse of cosine similarity where 1 means identical. 
Formula: cosine distance = 1 - cosine similarity.

### Why a relevance threshold is needed
Without a threshold, ChromaDB always returns results regardless of 
how irrelevant they are — because we ask for n_results=3 it will 
always return 3 chunks even if none of them are related to the 
question. A threshold of 0.8 was chosen based on testing — relevant 
questions scored around 0.4-0.5, irrelevant questions scored 1.7+. 
Any chunk with distance > 0.8 is filtered out.

### Behavior on irrelevant questions
If all retrieved chunks are above the threshold, the system returns: 
"I don't have enough information in the provided documents to answer 
this question." This is critical for production — the system must be 
grounded to its own data and never hallucinate answers from irrelevant 
context.


## Phase 5: Generation with OpenAI

### LLM Choice
GPT-5-nano was chosen for generation. It is the cheapest model in the 
GPT-5 family at $0.05 per 1M input tokens, making it cost effective 
for testing. It is also reliable and more than capable for RAG 
generation where the heavy lifting is done by retrieval, not the LLM.

### Prompt Structure
The prompt is split into system and user messages because that is how 
OpenAI's chat completion API expects input. The system message defines 
how the model should behave — acting as a research assistant, citing 
sources, only using provided context. The user message contains the 
actual context chunks and question.

### Bug: Model refusing to answer
The model was refusing to answer even when relevant context was 
provided. The cause was an overly restrictive system prompt that 
told the model to respond with an exact refusal phrase if context 
was "insufficient." GPT-5-nano is a reasoning model and interpreted 
this too conservatively. Fixed by simplifying the system prompt and 
making the instructions less rigid — giving the model more flexibility 
to use the context it was provided.


## Phase 6: Hybrid Retrieval (BM25 + Semantic)

### Result
Score improved from 6.5/10 to 8.2/10 (+1.7 points)

### Why BM25 helped
Semantic search alone struggles with exact numbers and domain-specific 
terminology. BM25 keyword matching directly solved three major failure 
patterns: numerical retrieval (Q6 +5, Q8 +3.5), precise terminology 
(Q5 +5), and cross-fact retrieval (Q4 +3).

### Remaining gaps
Enumerated lists in methodology sections still fragmented (Q9). 
Granular proportions within categories partially missing (Q10). 
These are chunking boundary problems, not retrieval algorithm problems.
Next step: cross-encoder re-ranking to further improve precision.