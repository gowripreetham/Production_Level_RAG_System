import chromadb
from src.generator import generate_answer
from src.retriever import build_retriever, hybrid_search

QUESTION = "In the Paris School Streets study, what are the four distinct categories of School Streets identified through field visits and street imagery analysis, what are their approximate proportions, and what was the average temperature differential detected between School Streets with cooling pavement and adjacent control streets?"


collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()
filtered = hybrid_search(QUESTION, collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)




context = ""

if not filtered:
    print("I don't have enough information in the provided documents to answer this question.")
else:
    for doc, meta, dist in filtered:
        context+= f"Source: {meta['source']}\n{doc}\n\n"
# print("CONTEXT BEING SENT:", context)

answer = generate_answer(QUESTION,context)
print(answer)




