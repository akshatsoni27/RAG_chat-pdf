from langchain_community.document_loaders import TextLoader

data = TextLoader(
    "notes.txt",
    encoding="utf-8"
)

docs = data.load()

print(docs[0].page_content)