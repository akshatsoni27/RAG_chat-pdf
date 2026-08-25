from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

result = embedding_model.embed_query(
    "What is deep learning?"
)

print("Embedding created successfully!")
print("Dimensions:", len(result))