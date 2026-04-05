import sys
sys.path.append(".")

from tests.eval_questions import EVAL_QUESTIONS
from src.retriever import build_retriever, hybrid_search
from src.generator import generate_answer

collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()

for q in EVAL_QUESTIONS:
    print(f"\n{'='*60}")
    print(f"ID: {q['id']} | Difficulty: {q['difficulty']}")
    print(f"Q: {q['question']}")
    print(f"{'='*60}")
    
    filtered = hybrid_search(q["question"], collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
    
    context = ""
    for doc, meta, dist in filtered:
        context += f"Source: {meta['source']}\n{doc}\n\n"
    
    answer = generate_answer(q["question"], context)
    print(f"A: {answer}")
    print(f"Expected: {q['expected_answer']}")