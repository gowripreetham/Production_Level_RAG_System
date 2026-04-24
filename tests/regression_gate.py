import sys
import statistics
from langfuse import get_client
from src.generator import generate_answer
from src.retriever import build_retriever, hybrid_search, rerank
from src.tracer import score_groundedness
from tests.eval_questions import EVAL_QUESTIONS
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

GROUNDEDNESS_THRESHOLD = 0.90

print("=" * 60)
print("RAG REGRESSION GATE")
print("=" * 60)

print("\nBuilding retriever...")
client, bm25, all_chunks, all_ids, all_metadatas = build_retriever()
print("Ready!\n")

groundedness_scores = []
results = []

for q in EVAL_QUESTIONS:
    question = q["question"]
    qid = q["id"]
    difficulty = q["difficulty"]

    print(f"{qid} [{difficulty}]: {question[:70]}...")

    with langfuse.start_as_current_observation(
        as_type="span",
        name="rag_query",
        input={"question": question, "question_id": qid, "run_type": "regression_gate"}
    ) as trace:

        # Retrieval
        with langfuse.start_as_current_observation(as_type="span", name="hybrid_retrieval", input={"question": question}) as span1:
            try:
                hybrid_results = hybrid_search(question, client, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
                if not hybrid_results:
                    raise ValueError("Retriever returned 0 chunks")
                span1.update(output={"status": "success", "chunks_retrieved": len(hybrid_results)})
            except Exception as e:
                span1.update(output={"status": "failed", "error": str(e)})
                langfuse.flush()
                raise

        # Reranking
        with langfuse.start_as_current_observation(as_type="span", name="reranking", input={"chunks_in": len(hybrid_results)}) as span2:
            try:
                filtered = rerank(question, hybrid_results, top_n=3)
                span2.update(output={"status": "success", "chunks_out": len(filtered)})
            except Exception as e:
                span2.update(output={"status": "failed", "error": str(e)})
                langfuse.flush()
                raise

        # Build context
        context = ""
        for doc, meta, dist in filtered:
            context += f"Source: {meta['source']}\n{doc}\n\n"

        # Generation
        with langfuse.start_as_current_observation(as_type="span", name="generation", input={"question": question}) as span3:
            try:
                usage, answer = generate_answer(question, context)
                input_cost = (usage.prompt_tokens / 1_000_000) * 0.15
                output_cost = (usage.completion_tokens / 1_000_000) * 0.60
                total_cost = input_cost + output_cost
                span3.update(output={
                    "status": "success",
                    "answer": answer,
                    "total_cost": total_cost
                })
            except Exception as e:
                span3.update(output={"status": "failed", "error": str(e)})
                langfuse.flush()
                raise

        # Groundedness scoring
        try:
            groundedness = score_groundedness(question, context, answer)
        except Exception as e:
            print(f"  Groundedness scoring failed: {e}")
            groundedness = 0.0

        trace.update(output={
            "answer": answer,
            "status": "success",
            "groundedness": groundedness,
            "question_id": qid,
            "run_type": "regression_gate"
        })

    groundedness_scores.append(groundedness)
    status = "✅" if groundedness >= GROUNDEDNESS_THRESHOLD else "⚠️"
    print(f"  Groundedness: {groundedness:.2f} {status}\n")
    results.append({"id": qid, "difficulty": difficulty, "groundedness": groundedness})

langfuse.flush()

# Final evaluation
avg_groundedness = statistics.mean(groundedness_scores)
below_threshold = [r for r in results if r["groundedness"] < GROUNDEDNESS_THRESHOLD]

print("=" * 60)
print("REGRESSION GATE RESULTS")
print("=" * 60)
print(f"\nAverage groundedness: {avg_groundedness:.2f}")
print(f"Threshold:            {GROUNDEDNESS_THRESHOLD}")
print(f"Questions below threshold: {len(below_threshold)}")

if below_threshold:
    print("\nFailing questions:")
    for r in below_threshold:
        print(f"  {r['id']} [{r['difficulty']}] — {r['groundedness']:.2f}")

print()
if avg_groundedness >= GROUNDEDNESS_THRESHOLD:
    print("✅ REGRESSION GATE PASSED")
    print(f"Average groundedness {avg_groundedness:.2f} meets threshold {GROUNDEDNESS_THRESHOLD}")
    sys.exit(0)
else:
    print("❌ REGRESSION GATE FAILED")
    print(f"Average groundedness {avg_groundedness:.2f} is below threshold {GROUNDEDNESS_THRESHOLD}")
    print("This change has caused quality degradation. Fix before merging.")
    sys.exit(1)