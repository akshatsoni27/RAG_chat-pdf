# PDF RAG Assistant

A focused Retrieval-Augmented Generation (RAG) application for asking questions about PDF documents. Upload a PDF through the Streamlit interface, retrieve the most relevant passages, and receive answers grounded only in the uploaded document.

The project uses Mistral for embeddings and question answering, Chroma for vector search, LangChain for orchestration, and PyPDF for document loading.

## Features

- Upload any PDF from a browser
- Split PDF text into overlapping chunks
- Create semantic embeddings with `mistral-embed`
- Retrieve relevant passages with Chroma MMR search
- Answer questions with `mistral-small-2506`
- Refuse to invent answers when the document does not contain the information
- Display source page numbers for each answer
- Local secrets and generated vector data excluded from Git

## How It Works

```text
PDF upload
    |
    v
PyPDFLoader -> text chunks -> Mistral embeddings -> Chroma
                                                     |
Question -------------------------------------------+
    |
    v
Relevant chunks -> grounded prompt -> Mistral answer + source pages
```

## Requirements

- Python 3.10 or newer
- A Mistral API key
- Internet access when indexing documents and generating answers

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd RAG-App
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a file named `.env` in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

Never commit `.env` or place API keys directly in Python files. The repository's `.gitignore` already excludes local environment files.

## Run the Streamlit App

```bash
streamlit run app.py
```

Open the URL shown in the terminal, usually:

```text
http://localhost:8501
```

Then:

1. Upload a PDF.
2. Wait for indexing to finish.
3. Ask a question in the chat box.
4. Review the answer and source page numbers.

Each uploaded file is identified by its content hash. Re-uploading the same file during a session does not rebuild its index unnecessarily.

## Project Structure

```text
.
├── app.py                     # Streamlit upload and chat interface
├── rag.py                     # PDF loading, indexing, retrieval, and QA logic
├── requirements.txt           # Python dependencies
├── README.md                  # Setup and usage instructions
└── .gitignore
```

## Configuration

The main retrieval settings are defined in `rag.py`:

- Chunk size: `1000` characters
- Chunk overlap: `200` characters
- Retrieved chunks: `4`
- Retrieval strategy: Maximal Marginal Relevance (MMR)
- Embedding model: `mistral-embed`
- Chat model: `mistral-small-2506`

## Grounding Behavior

The assistant is instructed to use only retrieved PDF context. When the answer cannot be found in that context, it responds with:

> I could not find the answer in the document.

This is a retrieval-based assistant, so answer quality depends on PDF text extraction, chunking, embedding quality, and the relevance of the retrieved passages.

## Troubleshooting

### `MISTRAL_API_KEY` errors

Check that `.env` is in the project root and contains a valid key:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

Restart Streamlit after changing environment variables.

### Rebuild the local index

The Streamlit app creates an in-memory index for each uploaded PDF. Restart the app to clear its current session.

Any local `chroma_db` directory from previous experiments is generated data and is intentionally ignored by Git.

## Security

- Keep API keys in `.env` only.
- Do not commit `.env`, local databases, or uploaded documents containing sensitive information.
- Rotate the API key immediately if it has ever been exposed in a public repository or log.

## License

This project is not currently licensed. All rights are reserved by the copyright holder.

Before publishing, add a `LICENSE` file with the license you choose. Without a license,
others generally may not use, modify, or distribute this code beyond what copyright law
allows.
