print("starting...")
import chromadb
print("chromadb imported")
from src.generator import generate_answer
print("generator imported")
from src.retriever import build_retriever, hybrid_search, rerank
print("retriever imported")
from src.tracer import score_groundedness
from langfuse import get_client
from dotenv import load_dotenv
load_dotenv()
print("tracer imported")

langfuse = get_client()

QUESTION = "In the Paris School Streets study, what are the four distinct categories of School Streets identified through field visits and street imagery analysis, what are their approximate proportions, and what was the average temperature differential detected between School Streets with cooling pavement and adjacent control streets?"

print("building retriever...")
collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()
print("retriever built!")

with langfuse.start_as_current_observation(as_type="span", name="rag_query", input={"question": QUESTION}) as trace:

    # SPAN 1 — Hybrid retrieval
    with langfuse.start_as_current_observation(as_type="span", name="hybrid_retrieval", input={"question": QUESTION, "n_results": 20}) as span1:
        try:
            hybrid_results = hybrid_search(QUESTION, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
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
            filtered = rerank(QUESTION, hybrid_results, top_n=3)
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
    with langfuse.start_as_current_observation(as_type="span", name="generation", input={"question": QUESTION, "context_length": len(context)}) as span3:
        try:
            usage, answer = generate_answer(QUESTION, context)
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
        groundedness = score_groundedness(QUESTION, context, answer)
        trace.update(output={"answer": answer, "status": "success", "groundedness": groundedness})
        print(f"Groundedness score: {groundedness}")
    except Exception as e:
        print(f"Groundedness scoring failed: {e}")
        trace.update(output={"answer": answer, "status": "success"})

langfuse.flush()
print(answer)