import hashlib
import tempfile
from pathlib import Path

import streamlit as st

from rag import answer_question, create_vectorstore, load_pdf


st.set_page_config(page_title="PDF RAG", page_icon="PDF")
st.title("Ask your PDF")
st.caption("Upload a document, then ask questions grounded in its contents.")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_id = hashlib.sha256(file_bytes).hexdigest()

    if st.session_state.get("file_id") != file_id:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temporary_file:
            temporary_file.write(file_bytes)
            temporary_path = Path(temporary_file.name)

        try:
            with st.spinner("Reading and indexing your PDF..."):
                chunks = load_pdf(temporary_path)
                st.session_state.vectorstore = create_vectorstore(
                    chunks,
                    collection_name=f"upload_{file_id[:16]}",
                )
                st.session_state.file_id = file_id
                st.session_state.file_name = uploaded_file.name
                st.session_state.messages = []
        finally:
            temporary_path.unlink(missing_ok=True)

    st.success(f"Ready: {st.session_state.file_name}")

    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about your PDF")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the document..."):
                answer, sources = answer_question(st.session_state.vectorstore, question)
            st.markdown(answer)
            pages = sorted({source.metadata.get("page", 0) + 1 for source in sources})
            st.caption("Sources: page " + ", ".join(map(str, pages)))
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Upload a PDF to begin.")