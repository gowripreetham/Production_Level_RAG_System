import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="papers")



results = collection.query(
    query_texts=["How many School Streets exist in Paris as of summer 2025, and how much total street distance has been pedestrianized?"],
    n_results=3
)

filtered = [(doc, meta, dist) for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
) if dist < 0.8]


if not filtered:
    print("I don't have enough information in the provided documents to answer this question.")
else:
    for doc, meta, dist in filtered:
        print(f"Source: {meta['source']}")
        print(f"Distance: {dist}")
        print(f"Content: {doc}")
        print("---")




