from langfuse import get_client
from src.generator import generate_answer
from src.retriever import build_retriever, hybrid_search, rerank
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

# Build retriever once
print("Building retriever...")
collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()
print("Ready!\n")

# Test questions covering different aspects
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
        
        with langfuse.start_as_current_observation(as_type="span", name="hybrid_retrieval", input={"question": question, "n_results": 20}) as span1:
            hybrid_results = hybrid_search(question, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
            chunks_data = [{"source": m.get('source', 'unknown'), "distance": d, "text_preview": doc[:300]} for doc, m, d in hybrid_results]
            span1.update(output={"chunks_retrieved": len(hybrid_results), "all_chunks": chunks_data})
        
        with langfuse.start_as_current_observation(as_type="span", name="reranking", input={"chunks_in": len(hybrid_results), "top_n": 3}) as span2:
            filtered = rerank(question, hybrid_results, top_n=3)
            top_chunks_data = [{"source": m.get('source', 'unknown'), "score": d, "text_preview": doc[:500]} for doc, m, d in filtered]
            span2.update(output={"chunks_out": len(filtered), "top_chunks": top_chunks_data})
        
        context = ""
        for doc, meta, dist in filtered:
            context += f"Source: {meta['source']}\n{doc}\n\n"
        
        with langfuse.start_as_current_observation(as_type="span", name="generation", input={"question": question, "context_length": len(context)}) as span3:
            answer = generate_answer(question, context)
            span3.update(output={"answer": answer})
        
        trace.update(output={"answer": answer})
    
    print(f"Answer: {answer}\n")

langfuse.flush()
print("\n✅ All questions processed! Check your Langfuse dashboard.")