from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Load PDF
loader = PyPDFLoader("Document_Loaders/Deeplearn.pdf")
docs = loader.load()

print("Pages:", len(docs))

# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0
)

chunks = splitter.split_documents(docs)

print("Chunks:", len(chunks))

# Prompt
template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that summarizes text."),
    ("human", "Summarize the following text:\n\n{data}")
])

# Mistral model
model = ChatMistralAI(
    model="mistral-small-2506"
)

# Test with first chunk
prompt = template.format_messages(
    data=chunks[0].page_content
)

result = model.invoke(prompt)

print(result.content)