from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

COLLECTION_NAME = "papers"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 dimensions

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

def ensure_collection_exists(client):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
        # Create payload index for source field so we can filter by it
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="source",
            field_schema="keyword"
        )
        print(f"Created collection: {COLLECTION_NAME}")

def store_chunks(chunks, filename):
    client = get_qdrant_client()
    ensure_collection_exists(client)

    # Duplicate check — search for existing chunk with this filename
    results = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter={
            "must": [{"key": "source", "match": {"value": filename}}]
        },
        limit=1
    )
    if results[0]:
        print(f"Skipping {filename} - already stored")
        return

    # Generate embeddings
    embeddings = model.encode(chunks).tolist()

    # Build points
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "source": filename,
                "chunk_id": f"{filename}_chunk_{i}",
                "text": chunk
            }
        ))

    # Upload to Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Stored {len(chunks)} chunks from {filename}")