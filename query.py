import chromadb
from src.generator import generate_answer

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="papers")

QUESTION = "How many School Streets exist in Paris as of summer 2025, and how much total street distance has been pedestrianized?"

results = collection.query(
    query_texts=[QUESTION],
    n_results=3
)

filtered = [(doc, meta, dist) for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
) if dist < 0.8]

# print(filtered)

context = ""

if not filtered:
    print("I don't have enough information in the provided documents to answer this question.")
else:
    for doc, meta, dist in filtered:
        context+= f"Source: {meta['source']}\n{doc}\n\n"
# print("CONTEXT BEING SENT:", context)

answer = generate_answer(QUESTION,context)
print(answer)




