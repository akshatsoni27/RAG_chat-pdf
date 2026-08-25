from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    "What is deep learning?",
    "Neural networks are used in artificial intelligence."
]

embeddings = model.encode(texts)

print("Success!")
print("Number of embeddings:", len(embeddings))
print("Dimensions:", len(embeddings[0]))