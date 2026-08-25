from pathlib import Path

from rag import create_vectorstore, load_pdf


pdf_path = Path("Document_Loaders/deeplearning.pdf")
chunks = load_pdf(pdf_path)
create_vectorstore(chunks, persist_directory="chroma_db")

print(f"Indexed {len(chunks)} chunks from {pdf_path}.")