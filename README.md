# Production-Level RAG System

A production-grade Retrieval Augmented Generation (RAG) system built to 
answer questions from academic research papers with citations. Built from 
scratch to understand every component of how RAG works in production — 
not just following a tutorial, but making real engineering decisions, 
measuring outcomes, and iterating based on data.

Inspired by [Aishwarya Srinivasan's](https://www.youtube.com/@AishwaryaSrinivasan) 
portfolio project recommendations.

---

## Why RAG?

Giving an LLM your entire document corpus as context is expensive, slow, 
and surprisingly ineffective — research shows that LLM answer quality 
degrades as context length grows (the "lost in the middle" problem). RAG 
solves this by retrieving only the most relevant chunks before generation, 
keeping context focused and costs low.

---

## What I Built

A domain-specific "Ask My Docs" system built on 8 research papers by 
Professor Marcel Moran (SJSU, 2024–2026) covering urban planning, street 
design, and transportation policy. The system retrieves relevant passages 
and generates answers with citations pointing back to the exact source paper.

---

## Architecture

![RAG Pipeline Architecture](assets/architecture.png)

---

## Evaluation Results

I ran 6 rounds of evaluation across 10 questions (5 easy, 5 tough) 
measuring how each architectural upgrade improved performance.

| Round | Configuration | Score |
|-------|--------------|-------|
| R1 | Semantic search only | 6.5/10 |
| R2 | + BM25 hybrid retrieval | 8.2/10 |
| R3 | + Cross-encoder reranker (k=3) | 6.8/10 |
| R4 | + Cross-encoder reranker (k=10) | 7.9/10 |
| R5 | + Unstructured chunking (k=10) | 8.65/10 |
| R6 | + Unstructured chunking (k=3) | **8.8/10** |

Key insight: The biggest jump came not from retrieval algorithms but from 
fixing chunking. No amount of BM25 or re-ranking can retrieve a chunk that 
doesn't exist in the right form.

### RAGAS Automated Evaluation (Final System)

| Metric | Score |
|--------|-------|
| Faithfulness | 0.95 |
| Context Recall | 0.83 |
| Context Precision | 0.97 |

---

## Tech Stack

| Component | Tool |
|-----------|------|
| PDF Extraction | Unstructured |
| Chunking | unstructured chunk_by_title |
| Vector Store | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 (sentence-transformers) |
| Keyword Search | BM25 (rank-bm25) |
| Re-ranking | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| Generation | GPT-5-nano (OpenAI) |
| Evaluation | RAGAS |
| Prompt Management | Custom YAML versioning |

---

## Project Structure

rag-professor/
├── data/                    # Research paper PDFs
├── src/
│   ├── extractor.py         # PDF extraction with Unstructured
│   ├── chunker.py           # Semantic chunking
│   ├── embedder.py          # ChromaDB storage
│   ├── retriever.py         # Hybrid search + re-ranking
│   ├── generator.py         # LLM answer generation
│   └── prompt_manager.py    # Prompt versioning
├── tests/
│   ├── eval_questions.py    # 10 annotated evaluation questions
│   ├── run_eval.py          # Manual evaluation runner
│   ├── ragas_eval.py        # RAGAS automated evaluation
│   └── smoke_test.py        # Lightweight CI test
├── .github/workflows/
│   └── eval.yml             # GitHub Actions CI pipeline
├── prompts.yaml             # Versioned prompt templates
├── DECISIONS.md             # Architecture decisions log
├── EVALUATION.md            # Phase 1 baseline evaluation
└── main.py                  # Ingestion pipeline

---

## Setup
```bash
# Clone the repo
git clone https://github.com/gowripreetham/Production_Level_RAG_System.git
cd Production_Level_RAG_System

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Add your PDFs to data/ folder
# Then ingest them
python main.py

# Ask a question
python query.py
```

---

## CI Pipeline

GitHub Actions runs a smoke test on every push to main — verifying that 
all components initialize correctly and the retrieval pipeline returns 
results. Full RAGAS evaluation is run manually due to the document corpus 
not being committed to the repository (PDFs are excluded from version 
control for storage reasons).

---

## Key Learnings

- **Chunking quality matters more than retrieval algorithm** — switching 
  to Unstructured's structure-aware parser solved failures that BM25 and 
  re-ranking couldn't fix
- **Hybrid retrieval is essential for technical content** — BM25 finds 
  exact numbers and domain terms that semantic search misses
- **Measure everything** — running 6 rounds of evaluation with specific 
  questions revealed exactly where failures were happening and why
- **Prompt versioning is not optional** — treating prompts as versioned 
  config rather than hardcoded strings enables systematic experimentation



## Project 3: RAG Monitoring & Observability

Building the RAG system was 30% of the work. This layer handles 
the remaining 70% — knowing whether the system is working correctly, 
understanding why it fails, and preventing quality regressions.

### What was added

**Langfuse Tracing**
Every query is now fully traced. For each request you can see 
exactly which 20 chunks were retrieved, which 3 survived reranking, 
what prompt was sent to the LLM, and what answer was generated. 
Every step has timing and status recorded.

**Production Metrics**
Every query tracks:
- Cost per query (input tokens, output tokens, total via OpenAI usage API)
- Latency at P50, P95, P99 percentiles — not just averages
- Failure rate with try/except on every pipeline step
- Groundedness score via LLM-as-judge (0.0 to 1.0)

**Monitoring Report**
A report script pulls all historical traces from Langfuse and 
computes production statistics across all queries:

RAG SYSTEM MONITORING REPORT
Total queries:    32
Failure rate:     0.0%
P50 latency:      11.52s
P95 latency:      29.40s
Avg cost/query:   $0.000911
Est. monthly:     $2.73 (3000 queries)
Avg groundedness: 0.96
Easy questions:   0.99
Tough questions:  0.92

**Regression Gate (GitHub Actions + Qdrant Cloud)**
Every push to main triggers an automated quality check:
- Connects to Qdrant Cloud (embeddings hosted remotely)
- Runs all 10 evaluation questions through the full pipeline
- Scores groundedness for each answer
- Passes only if average groundedness ≥ 0.90
- Blocks the merge if quality has degraded

This means no prompt change, chunking update, or retrieval 
modification can reach production without passing a real 
quality evaluation.

### Key findings from monitoring

- 0% failure rate across all queries
- Average groundedness of 0.96 — answers are almost always 
  supported by retrieved chunks
- Q6 (DiD coefficient question) consistently scores lower — 
  a retrieval issue where the specific statistical result 
  doesn't surface in the top 3 chunks
- GPT-5-nano costs $2.73/month at 3000 queries/day — 
  extremely cost efficient
- P95 latency of 29s reflects M1 8GB hardware constraints — 
  would be 2-3x faster on a production server

### Tech stack additions

| Component | Tool |
|---|---|
| Tracing | Langfuse v4 |
| Vector store | Qdrant Cloud |
| CI/CD | GitHub Actions |
| LLM judge | GPT-5-nano |
| Metrics | Custom Python report |



