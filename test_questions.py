from langfuse import get_client
from src.generator import generate_answer
from src.retriever import build_retriever, hybrid_search, rerank
from src.tracer import score_groundedness
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

print("Building retriever...")
collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()
print("Ready!\n")

QUESTIONS = [
    "What are the four categories of School Streets in Paris?",
    "How many bike lanes does Paris have?",
    "What temperature difference was found with cooling pavement?",
    "What methodology did researchers use to study School Streets?",
    "How much open space was created by pedestrianization in Paris?"
]

for i, question in enumerate(QUESTIONS, 1):
    print(f"\n{'='*60}")
    print(f"Question {i}: {question}")
    print('='*60)

    with langfuse.start_as_current_observation(as_type="span", name="rag_query", input={"question": question}) as trace:

        # SPAN 1 — Hybrid retrieval
        with langfuse.start_as_current_observation(as_type="span", name="hybrid_retrieval", input={"question": question, "n_results": 20}) as span1:
            try:
                hybrid_results = hybrid_search(question, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
                if not hybrid_results:
                    raise ValueError("Retriever returned 0 chunks")
                chunks_data = [{"source": m.get('source', 'unknown'), "distance": d, "text_preview": doc[:300]} for doc, m, d in hybrid_results]
                span1.update(output={"status": "success", "chunks_retrieved": len(hybrid_results), "all_chunks": chunks_data})
            except Exception as e:
                span1.update(output={"status": "failed", "error": str(e)})
                langfuse.flush()
                raise

        # SPAN 2 — Reranking
        with langfuse.start_as_current_observation(as_type="span", name="reranking", input={"chunks_in": len(hybrid_results), "top_n": 3}) as span2:
            try:
                filtered = rerank(question, hybrid_results, top_n=3)
                if not filtered:
                    raise ValueError("Reranker returned 0 chunks")
                top_chunks_data = [{"source": m.get('source', 'unknown'), "score": d, "text_preview": doc[:500]} for doc, m, d in filtered]
                span2.update(output={"status": "success", "chunks_out": len(filtered), "top_chunks": top_chunks_data})
            except Exception as e:
                span2.update(output={"status": "failed", "error": str(e)})
                langfuse.flush()
                raise

        # Build context
        context = ""
        for doc, meta, dist in filtered:
            context += f"Source: {meta['source']}\n{doc}\n\n"

        # SPAN 3 — Generation
        with langfuse.start_as_current_observation(as_type="span", name="generation", input={"question": question, "context_length": len(context)}) as span3:
            try:
                usage, answer = generate_answer(question, context)
                input_cost = (usage.prompt_tokens / 1_000_000) * 0.15
                output_cost = (usage.completion_tokens / 1_000_000) * 0.60
                total_cost = input_cost + output_cost
                span3.update(output={
                    "status": "success",
                    "answer": answer,
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_cost": total_cost
                })
            except Exception as e:
                span3.update(output={"status": "failed", "error": str(e)})
                langfuse.flush()
                raise

        # GROUNDEDNESS SCORING
        try:
            groundedness = score_groundedness(question, context, answer)
            trace.update(output={"answer": answer, "status": "success", "groundedness": groundedness})
            print(f"Groundedness score: {groundedness}")
        except Exception as e:
            print(f"Groundedness scoring failed: {e}")
            trace.update(output={"answer": answer, "status": "success"})

    print(f"Answer: {answer}\n")

langfuse.flush()
print("\n✅ All questions processed! Check your Langfuse dashboard.")