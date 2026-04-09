from rank_bm25 import BM25Okapi
import chromadb
import numpy as np
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def build_retriever():
    # 1. Connect to ChromaDB
    # 2. Pull ALL chunks out of the collection
    # 3. Build BM25 index from those chunks
    # 4. Return both the collection and bm25 index
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="papers")

    all_data = collection.get()
    all_chunks = all_data["documents"]  # list of all chunk texts
    all_ids = all_data["ids"]           # list of all chunk ids
    all_metadatas = all_data["metadatas"]  # list of all metadata dicts

    tokenized_chunks = [chunk.split() for chunk in all_chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    
    return collection, bm25, all_chunks, all_ids, all_metadatas

def hybrid_search(question, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20):
    semantic_results = collection.query(
        query_texts=[question],
        n_results=20
    )
    semantic_ids = semantic_results["ids"][0]

    id_to_chunk = {all_ids[i]: all_chunks[i] for i in range(len(all_ids))}
    id_to_meta = {all_ids[i]: all_metadatas[i] for i in range(len(all_ids))}

    tokenized_query = question.split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_ranked_indices = np.argsort(bm25_scores)[::-1]
    bm25_ranked_ids = [all_ids[i] for i in bm25_ranked_indices]


    # Step 3: RRF combination
    rrf_scores = {}
    
    for rank, chunk_id in enumerate(semantic_ids):
        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0
        rrf_scores[chunk_id] += 1 / (60 + rank)
    
    for rank, chunk_id in enumerate(bm25_ranked_ids):
        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0
        rrf_scores[chunk_id] += 1 / (60 + rank)
    
    # Step 4: Sort by RRF score and return top results
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    top_ids = sorted_ids[:n_results]

    results = []
    for chunk_id in top_ids:
            results.append((
                id_to_chunk[chunk_id],
                id_to_meta[chunk_id],
                rrf_scores[chunk_id]
            ))
    
    return results

def rerank(question, hybrid_results, top_n=3):
    pairs = [(question, doc) for doc, meta, score in hybrid_results]
    scores = model.predict(pairs)

    scored_results = list(zip(scores, hybrid_results))
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return [(doc, meta, score) for score, (doc, meta, _) in scored_results[:top_n]]
     
     




