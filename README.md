# ⚖️ LegalIQ

### AI-Powered Legal Contract Intelligence Agent

LegalIQ is an AI legal contract agent built using **Local RAG (Retrieval-Augmented Generation)** to analyze legal contracts, extract important clauses, answer contract-related questions, and identify attention points.

## ✨ Features

- 💬 **Contract Q&A** — Ask questions about the uploaded contract.
- 📑 **Key Clause Extraction** — Extract important clauses such as termination, payment, confidentiality, liability, indemnification, governing law, and penalties.
- 📋 **Contract Summary** — Generate a structured summary of the contract.
- ⚠️ **Attention Point Analysis** — Identify areas that may require closer review.
- 📚 **Source References** — View the PDF pages used to generate responses.
- 🛡️ **Hallucination Protection** — Responses are grounded in the retrieved contract content.
- 🔒 **Local Processing** — Uses locally running AI models through Ollama.

## 🧠 Architecture

```text
                    LegalIQ Agent
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   Contract Q&A     Key Clauses      Summary / Attention
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                    Local RAG
                         ↓
                  Document Chunks
                         ↓
                 Nomic Embeddings
                         ↓
               Cosine Similarity
                         ↓
                    Llama 3.2
                         ↓
              Grounded Response
                         ↓
                 Source PDF Pages
```

## 🔄 RAG Workflow

```text
Upload Contract
      ↓
Extract Text using PyPDF
      ↓
Split into Overlapping Chunks
      ↓
Generate Embeddings
      ↓
Convert User Question into Embedding
      ↓
Cosine Similarity Retrieval
      ↓
Retrieve Relevant Contract Chunks
      ↓
Send Context to Llama 3.2
      ↓
Generate Grounded Answer
      ↓
Display Answer + Source Pages
```

## 🛠️ Tech Stack

- **Python 3.11**
- **Streamlit** — User interface
- **PyPDF** — PDF text extraction
- **Ollama** — Local model runtime
- **Llama 3.2** — Language model
- **nomic-embed-text** — Embeddings
- **NumPy** — Cosine similarity
- **RAG** — Document-grounded retrieval and generation

## 📁 Project Structure

```text
Legalcontractagent/
│
├── app.py
├── data/
│   └── contract.pdf
│
├── src/
│   ├── pdf_reader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── rag.py
│   ├── clause_extractor.py
│   ├── contract_summary.py
│   ├── risk_analysis.py
│   └── agent.py
│
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Legalcontractagent
```

### 2. Create the Conda environment

```bash
conda create -n legal_agent python=3.11
conda activate legal_agent
```

### 3. Install dependencies

```bash
pip install streamlit pypdf ollama numpy
```

### 4. Install the required Ollama models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Make sure Ollama is running before starting the application.

## ▶️ Run the Application

```bash
streamlit run app.py
```

## 🔐 Local & Privacy-Focused

LegalIQ uses locally running models through Ollama and does not require a cloud-based LLM API for contract analysis.

## 🎯 Project Goal

LegalIQ aims to make legal contract analysis **faster, structured, and document-grounded**, helping users find relevant information without manually searching through lengthy contracts.

---

**⚖️ LegalIQ — Find the evidence. Understand the contract.**
