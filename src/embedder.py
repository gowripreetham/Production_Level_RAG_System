import chromadb

def store_chunks(chunks, filename):
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="papers")

    existing = collection.get(ids=[f"{filename}_chunk_0"])
    if len(existing["documents"]) > 0:
        print(f"Skipping {filename} - already stored")
        return

    for i, chunk in enumerate(chunks):
        collection.add(
                documents=[chunk],
                metadatas=[{"source": filename}],
                ids=[f"{filename}_chunk_{i}"]
            )
    
    print(f"Stored {len(chunks)} chunks from {filename}")




