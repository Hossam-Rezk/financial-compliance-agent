# Financial Compliance Agent

An end-to-end RAG (Retrieval-Augmented Generation) pipeline designed to audit financial documents against a predefined set of compliance rules. It uses a hybrid architecture with local embeddings for privacy and Groq's lightning-fast API for LLM inference.

---

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite (TypeScript, Vanilla CSS Glassmorphism)
- **Vector Database**: Qdrant — stores and searches document embeddings semantically
- **Document Store**: MongoDB — stores project metadata and document chunks
- **LLM Engine**: Groq (LLaMA 3.3 70B) — ultra-fast cloud inference for compliance analysis and report generation
- **Embeddings**: Ollama (nomic-embed-text) — local vector embeddings for privacy-preserving document indexing

---

## The 4-Agent Compliance Pipeline

When an analysis is requested, the system orchestrates 4 specialized AI agents in sequence:

1. **RetrieverAgent** — Embeds the query and performs semantic search over the document corpus in Qdrant, surfacing the most relevant chunks for analysis.
2. **ComplianceCheckerAgent** — Reviews each retrieved chunk against a predefined compliance ruleset and identifies specific violations with supporting evidence from the document.
3. **RiskScorerAgent** — Assigns a severity level (Critical / High / Medium / Low) and a numeric risk score from 0 to 100 to each finding, along with a rationale and recommended action.
4. **ReportGeneratorAgent** — Synthesizes all scored findings into a structured report containing an overall risk score, severity summary, executive summary, per-finding breakdown, and actionable recommendations.

All agent outputs are validated Pydantic models — no unstructured text passes between agents.

---

## Local Development Setup

### Prerequisites
- Docker & Docker Compose
- Node.js (v20+) & npm
- Python 3.10+
- A free Groq API key from https://console.groq.com

### 1. Environment Configuration
Copy the environment template and add your Groq API key:
```bash
cp .env.example .env
```
Open `.env` and fill in:
```
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Start Infrastructure
Spin up MongoDB, Qdrant, and Ollama containers:
```bash
docker-compose up -d
```

### 3. Pull the Embedding Model (Required)
Ollama does not download models automatically. Pull the embedding model into the container:
```bash
docker exec -it ollama ollama pull nomic-embed-text
```

### 4. Start the Backend
Install dependencies and run the FastAPI server:
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --reload-dir src
```
API available at `http://127.0.0.1:8000`

### 5. Start the Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
UI available at `http://localhost:5173`

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/data/upload/{project_id}` | Upload a PDF or TXT document to a project |
| `POST` | `/api/v1/data/process/{project_id}` | Chunk, embed, and index the uploaded document into Qdrant and MongoDB |
| `POST` | `/api/v1/nlp/analyze/{project_id}` | Run the full 4-agent compliance audit pipeline and return a structured risk report |
| `POST` | `/api/v1/nlp/chat/{project_id}` | Chat with the compliance assistant about the uploaded document |

---

## Test Documents

Two test documents are included to validate the pipeline:

- **`audit_test_violations.txt`** — A financial services agreement containing multiple deliberate compliance violations across data privacy, financial reporting, and contract law. Expected result: Critical risk score, 10+ findings.
- **`audit_test_compliant.txt`** — A fully compliant corporate services contract satisfying all ruleset requirements. Expected result: 0 findings, clean pass.

---

## Key Design Decisions

- **Groq for generation, Ollama for embeddings** — Groq provides near-instant LLM responses (vs minutes on CPU), while Ollama keeps embeddings local for privacy.
- **Pydantic v2 throughout** — Every agent input and output is a validated model, preventing silent failures between pipeline stages.
- **Rate limiting** — The analyze endpoint is limited to 5 requests/minute and chat to 10 requests/minute via SlowAPI to prevent abuse.
- **WSL2 compatibility** — Run uvicorn with `--reload-dir src` to avoid permission errors on Docker-mounted volumes in WSL2.
