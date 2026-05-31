# Financial Compliance Agent

An end-to-end local RAG (Retrieval-Augmented Generation) pipeline designed to audit financial documents against a predefined set of compliance rules using entirely open-source, local models.

![UI Mockup](https://via.placeholder.com/1200x600?text=Financial+Compliance+Agent+UI)

##  Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite (TypeScript, Vanilla CSS Glassmorphism)
- **Vector Database**: Qdrant
- **Document Store**: MongoDB
- **Local LLM & Embeddings**: Ollama (Mistral / Nomic-Embed-Text)

### The 4-Agent Pipeline
When an analysis is requested, the system orchestrates 4 specialized AI agents:
1. **RetrieverAgent**: Embeds the query and fetches the top-K relevant document chunks from Qdrant.
2. **ComplianceCheckerAgent**: Evaluates chunks against the compliance rule set to identify violations.
3. **RiskScorerAgent**: Evaluates the severity (Critical, High, Medium, Low) of each violation with a rationale.
4. **ReportGeneratorAgent**: Synthesizes the findings into a cohesive Executive Summary and structured JSON report.

---

##  Local Development Setup

### 1. Prerequisites
- Docker & Docker Compose
- Node.js (v20+) & npm
- Python 3.10+

### 2. Environment Configuration
Copy the environment template:
```bash
cp .env.example .env
```
*(The default values are configured to work out-of-the-box for local dev).*

### 3. Start Infrastructure
Spin up the MongoDB, Qdrant, and Ollama containers:
```bash
docker-compose up -d
```

### 4. Pull LLM Models (CRITICAL)
Ollama does **not** download models automatically. You must pull them into the container:
```bash
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull nomic-embed-text
```

### 5. Start the Backend
Install dependencies and run the FastAPI server:
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```
*The API will be available at `http://127.0.0.1:8000`*

### 6. Start the Frontend
In a new terminal, launch the React UI:
```bash
cd frontend
npm install
npm run dev
```
*The UI will be available at `http://localhost:5173`*

---

## 📖 API Reference

- `POST /api/v1/data/upload/{project_id}`: Upload a PDF/TXT document.
- `POST /api/v1/data/process/{project_id}`: Chunk the document, embed it, and store in Mongo/Qdrant.
- `POST /api/v1/nlp/analyze/{project_id}`: Run the full 4-agent compliance report pipeline.
- `POST /api/v1/nlp/chat/{project_id}`: Talk directly to the Compliance Assistant regarding the uploaded document.
