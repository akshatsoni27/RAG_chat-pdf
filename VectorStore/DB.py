from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

docs = [
    Document(
        page_content="Python is widely used in Artificial Intelligence.",
        metadata={"source": "doc1"}
    ),
    Document(
        page_content="Pandas is used for data analysis in Python.",
        metadata={"source": "doc2"}
    ),
    Document(
        page_content="Neural networks are used in Deep Learning.",
        metadata={"source": "doc3"}
    )
]

embedding_model = MistralAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="chroma-db"
)

# Similarity Search
result = vectorstore.similarity_search(
    "What is used for data analysis?",
    k=2
)

for r in result:
    print(r.page_content)
    print(r.metadata)

# Retriever
retriever = vectorstore.as_retriever()

retrieved_docs = retriever.invoke(
    "Explain Deep Learning."
)

for d in retrieved_docs:
    print(d.page_content)