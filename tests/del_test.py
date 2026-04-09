import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="papers")

all_data = collection.get()
small_chunks = [(id, doc) for id, doc in zip(all_data["ids"], all_data["documents"]) if len(doc) < 300]

print(f"Total chunks under 300 chars: {len(small_chunks)}")
for id, doc in small_chunks:
    print(f"\nID: {id}")
    print(f"Text: {doc}")
    print("---")