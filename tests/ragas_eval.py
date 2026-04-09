import sys
sys.path.append(".")

from tests.eval_questions import EVAL_QUESTIONS
from src.retriever import build_retriever, hybrid_search, rerank
from src.generator import generate_answer
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextRecall, ContextPrecision
from ragas.llms import llm_factory
from ragas.embeddings import OpenAIEmbeddings
from datasets import Dataset
from openai import OpenAI as OpenAIClient

# Build retriever once
collection, bm25, all_chunks, all_ids, all_metadatas = build_retriever()

# Collect data for RAGAS
questions = []
answers = []
contexts = []
ground_truths = []

print("Running pipeline on all eval questions...\n")

for q in EVAL_QUESTIONS:
    print(f"Processing {q['id']}...")
    
    hybrid_results = hybrid_search(q["question"], collection, bm25, all_chunks, all_ids, all_metadatas, n_results=20)
    final_results = rerank(q["question"], hybrid_results, top_n=3)
    
    context = ""
    context_list = []
    for doc, meta, dist in final_results:
        context += f"Source: {meta['source']}\n{doc}\n\n"
        context_list.append(doc)
    
    answer = generate_answer(q["question"], context)
    
    questions.append(q["question"])
    answers.append(answer)
    contexts.append(context_list)
    ground_truths.append(q["expected_answer"])

# Create RAGAS dataset
data = {
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
}

dataset = Dataset.from_dict(data)

# Setup LLM and embeddings
openai_client = OpenAIClient()
llm = llm_factory("gpt-4o-mini", client=openai_client)
embeddings = OpenAIEmbeddings(client=openai_client)

faithfulness_metric = Faithfulness(llm=llm)
answer_relevancy_metric = AnswerRelevancy(llm=llm, embeddings=embeddings)
context_recall_metric = ContextRecall(llm=llm)
context_precision_metric = ContextPrecision(llm=llm)

print("\nRunning RAGAS evaluation...\n")
results = evaluate(
    dataset,
    metrics=[
        faithfulness_metric,
        context_recall_metric,
        context_precision_metric
    ]
)

print(results)