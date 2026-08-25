from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful document question-answering assistant. "
        "Use only the provided context. If the answer is not in the context, "
        'say "I could not find the answer in the document." Do not use outside knowledge.',
    ),
    ("human", "Context:\n\n{context}\n\nQuestion:\n\n{question}"),
])


def load_pdf(pdf_path: str | Path) -> list[Document]:
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages = PyPDFLoader(str(path)).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)
    for chunk in chunks:
        chunk.page_content = chunk.page_content.encode("utf-8", "replace").decode("utf-8")
    return chunks


def create_vectorstore(
    documents: Iterable[Document],
    persist_directory: str | Path | None = None,
    collection_name: str = "rag_documents",
) -> Chroma:
    kwargs = {
        "documents": list(documents),
        "embedding": MistralAIEmbeddings(model="mistral-embed"),
        "collection_name": collection_name,
    }
    if persist_directory is not None:
        kwargs["persist_directory"] = str(persist_directory)
    return Chroma.from_documents(**kwargs)


def answer_question(vectorstore: Chroma, question: str, k: int = 4) -> tuple[str, list[Document]]:
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": 10},
    )
    documents = retriever.invoke(question)
    context = "\n\n".join(document.page_content for document in documents)
    response = ChatMistralAI(model="mistral-small-2506", temperature=0).invoke(
        PROMPT.invoke({"context": context, "question": question})
    )
    return str(response.content), documents