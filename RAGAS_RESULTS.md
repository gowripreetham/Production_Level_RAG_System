# RAGAS Evaluation Results

Automated evaluation using the RAGAS framework measuring retrieval 
and generation quality of the production RAG system.

## Final System Configuration
- PDF Extraction: Unstructured (structure-aware parsing)
- Chunking: chunk_by_title (max 2000 chars, overlap 200)
- Retrieval: Hybrid search (Semantic + BM25 via RRF)
- Re-ranking: cross-encoder/ms-marco-MiniLM-L-6-v2, top_n=3
- Generation: GPT-5-nano
- Prompt: v2 — Flexible

## Results

| Metric | Score | What it means |
|--------|-------|---------------|
| Faithfulness | 0.95 | 95% of claims are supported by retrieved chunks — minimal hallucination |
| Context Precision | 0.97 | 97% of retrieved chunks are actually relevant to the question |
| Context Recall | 0.83 | Retriever finds the right chunks 83% of the time |

## Evaluation Dataset
- 10 manually annotated questions (5 easy, 5 tough)
- Questions span all 8 research papers
- Expected answers manually verified against source papers
- See `tests/eval_questions.py` for full dataset

## How to Run
```bash
python tests/ragas_eval.py
```

Note: Requires OPENAI_API_KEY in .env. Costs approximately $0.05-0.15 per run.