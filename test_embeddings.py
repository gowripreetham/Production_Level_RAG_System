from sentence_transformers import SentenceTransformer, util
sentence1 = ["I'm a man"]
sentence2 = ["The stock market crashed today"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)

cos_scores = util.cos_sim(embedding1,embedding2)

print(embedding1.shape)

print(cos_scores)



