print("starting...")
import chromadb
print("chromadb imported")
from src.generator import generate_answer
print("generator imported")
from src.retriever import build_retriever, hybrid_search, rerank
print("retriever imported")
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
        hybrid_results = hybrid_search(QUESTION, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
        
        # Store actual chunk content for inspection
        chunks_data = []
        for doc, meta, dist in hybrid_results:
            chunks_data.append({
                "source": meta.get('source', 'unknown'),
                "distance": dist,
                "text_preview": doc  # first 300 chars
            })
        
        span1.update(output={
            "chunks_retrieved": len(hybrid_results),
            "all_chunks": chunks_data
        })

    # SPAN 2 — Reranking
    with langfuse.start_as_current_observation(as_type="span", name="reranking", input={"chunks_in": len(hybrid_results), "top_n": 3}) as span2:
        filtered = rerank(QUESTION, hybrid_results, top_n=3)
        
        top_chunks_data = []
        for doc, meta, dist in filtered:
            top_chunks_data.append({
                "source": meta.get('source', 'unknown'),
                "score": dist,
                "text_preview": doc[:500]
            })
        
        span2.update(output={
            "chunks_out": len(filtered),
            "top_chunks": top_chunks_data
        })

    # Build context
    context = ""
    if not filtered:
        print("I don't have enough information in the provided documents to answer this question.")
    else:
        for doc, meta, dist in filtered:
            context += f"Source: {meta['source']}\n{doc}\n\n"

    # SPAN 3 — Generation
    with langfuse.start_as_current_observation(as_type="span", name="generation", input={"question": QUESTION, "context_length": len(context)}) as span3:
        answer = generate_answer(QUESTION, context)
        span3.update(output={"answer": answer})

    trace.update(output={"answer": answer})

langfuse.flush()
print(answer)