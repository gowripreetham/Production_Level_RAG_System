import sys
sys.path.append(".")
import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="papers")

# Get all chunks from a specific paper
results = collection.get(
    where={"source": "7.pdf"}
)

print(f"Total chunks in 7.pdf: {len(results['ids'])}\n")

for i, (chunk_id, chunk_text) in enumerate(zip(results['ids'], results['documents'])):
    print(f"{'='*60}")
    print(f"Chunk {i+1} | ID: {chunk_id}")
    print(f"{'='*60}")
    print(chunk_text)
    print()