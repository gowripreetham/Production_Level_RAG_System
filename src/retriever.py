from rank_bm25 import BM25Okapi
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from sentence_transformers import SentenceTransformer, CrossEncoder
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv()

COLLECTION_NAME = "papers"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

def build_retriever():
    client = get_qdrant_client()

    # Pull ALL chunks from Qdrant
    all_chunks = []
    all_ids = []
    all_metadatas = []

    offset = None
    while True:
        results, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        for point in results:
            all_chunks.append(point.payload["text"])
            all_ids.append(point.payload["chunk_id"])
            all_metadatas.append({"source": point.payload["source"]})

        if offset is None:
            break

    # Build BM25 index from chunks
    tokenized_chunks = [chunk.split() for chunk in all_chunks]
    bm25 = BM25Okapi(tokenized_chunks)

    return client, bm25, all_chunks, all_ids, all_metadatas


def hybrid_search(question, client, bm25, all_chunks, all_ids, all_metadatas, n_results=20):
    # Semantic search via Qdrant
    query_embedding = embedding_model.encode(question).tolist()
    semantic_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=20
    ).points
    semantic_ids = [r.payload["chunk_id"] for r in semantic_results]

    # BM25 keyword search
    id_to_chunk = {all_ids[i]: all_chunks[i] for i in range(len(all_ids))}
    id_to_meta = {all_ids[i]: all_metadatas[i] for i in range(len(all_ids))}

    tokenized_query = question.split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_ranked_indices = np.argsort(bm25_scores)[::-1]
    bm25_ranked_ids = [all_ids[i] for i in bm25_ranked_indices]

    # RRF combination
    rrf_scores = {}

    for rank, chunk_id in enumerate(semantic_ids):
        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0
        rrf_scores[chunk_id] += 1 / (60 + rank)

    for rank, chunk_id in enumerate(bm25_ranked_ids):
        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0
        rrf_scores[chunk_id] += 1 / (60 + rank)

    # Sort by RRF score
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    top_ids = sorted_ids[:n_results]

    results = []
    for chunk_id in top_ids:
        if chunk_id in id_to_chunk:
            results.append((
                id_to_chunk[chunk_id],
                id_to_meta[chunk_id],
                rrf_scores[chunk_id]
            ))

    return results


def rerank(question, hybrid_results, top_n=3):
    pairs = [(question, doc) for doc, meta, score in hybrid_results]
    scores = reranker.predict(pairs)

    scored_results = list(zip(scores, hybrid_results))
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return [(doc, meta, score) for score, (doc, meta, _) in scored_results[:top_n]]