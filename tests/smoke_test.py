import sys
sys.path.append(".")

from src.retriever import build_retriever, hybrid_search, rerank

TEST_QUESTION = "What methodology was used for speed limit setting?"

def run_smoke_test():
    print("Running smoke test...\n")
    
    # Build retriever
    print("Step 1: Building retriever...")
    collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()
    print(f"✅ Retriever built — {len(all_chunks)} chunks loaded\n")
    
    # Run hybrid search
    print("Step 2: Running hybrid search...")
    hybrid_results = hybrid_search(TEST_QUESTION, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
    assert len(hybrid_results) > 0, "❌ Hybrid search returned no results"
    print(f"✅ Hybrid search returned {len(hybrid_results)} results\n")
    
    # Run reranker
    print("Step 3: Running reranker...")
    final_results = rerank(TEST_QUESTION, hybrid_results, top_n=3)
    assert len(final_results) > 0, "❌ Reranker returned no results"
    print(f"✅ Reranker returned {len(final_results)} results\n")
    
    # Check results have content
    for doc, meta, score in final_results:
        assert len(doc) > 0, "❌ Empty chunk returned"
        assert "source" in meta, "❌ Missing source metadata"
    
    print("✅ All checks passed — pipeline is working correctly")
    print(f"\nTop result source: {final_results[0][1]['source']}")
    print(f"Top result preview: {final_results[0][0][:150]}...")

if __name__ == "__main__":
    run_smoke_test()