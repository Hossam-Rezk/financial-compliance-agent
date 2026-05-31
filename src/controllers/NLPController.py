from .BaseController import BaseController
from src.stores.llm.OllamaProvider import OllamaProvider
from src.stores.vectordb.QdrantProvider import QdrantProvider
from src.agents.RetrieverAgent import RetrieverAgent
from src.agents.ComplianceCheckerAgent import ComplianceCheckerAgent
from src.agents.RiskScorerAgent import RiskScorerAgent
from src.agents.ReportGeneratorAgent import ReportGeneratorAgent


class NLPController(BaseController):

    def __init__(self):
        super().__init__()
        self.ollama = OllamaProvider()
        self.qdrant = QdrantProvider()

    async def embed_and_upsert(self, chunks: list, project_id: str) -> int:
        vectors = []
        for index, chunk in enumerate(chunks):
            embedding = await self.ollama.embed(chunk.page_content)
            vectors.append({
                "vector": embedding,
                "chunk_text": chunk.page_content,
                "chunk_order": index + 1,
                "project_id": project_id,
            })
        return self.qdrant.upsert_vectors(vectors)

    async def search(self, query: str, project_id: str, top_k: int = 5) -> list:
        query_vector = await self.ollama.embed(query)
        return self.qdrant.search(
            query_vector=query_vector,
            project_id=project_id,
            top_k=top_k,
        )

    async def analyze(
        self,
        query: str,
        project_id: str,
        top_k: int = 5,
    ) -> dict:
        chunks = await RetrieverAgent().run(
            query=query,
            project_id=project_id,
            top_k=top_k,
        )

        findings = await ComplianceCheckerAgent().run(chunks=chunks)

        scored_findings = await RiskScorerAgent().run(findings=findings)

        report = await ReportGeneratorAgent().run(
            query=query,
            project_id=project_id,
            scored_findings=scored_findings,
        )

        return report
