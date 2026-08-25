from pathlib import Path

from rag import answer_question, create_vectorstore, load_pdf


chunks = load_pdf(Path("Document_Loaders/deeplearning.pdf"))
vectorstore = create_vectorstore(chunks, persist_directory="chroma_db")

print(f"RAG system ready with {len(chunks)} chunks. Type 0 to exit.")
while True:
    question = input("You: ").strip()
    if question == "0":
        break
    if not question:
        continue

    answer, sources = answer_question(vectorstore, question)
    print(f"\nAI: {answer}\n")
    print("Sources:")
    for source in sources:
        print(f"- page {source.metadata.get('page', 0) + 1}")