from langchain_community.document_loaders import PyPDFLoader
data = PyPDFLoader("DeepLearning.pdf")

docs = data.load()

print(docs[15])