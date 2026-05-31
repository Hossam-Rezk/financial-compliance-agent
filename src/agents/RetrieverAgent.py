from src.stores.llm.OllamaProvider import OllamaProvider
from src.stores.vectordb.QdrantProvider import QdrantProvider


class RetrieverAgent:

    def __init__(self):
        self.ollama = OllamaProvider()
        self.qdrant = QdrantProvider()

    async def run(self, query: str, project_id: str, top_k: int = 5) -> list[dict]:
        query_vector = await self.ollama.embed(query)
        results = self.qdrant.search(
            query_vector=query_vector,
            project_id=project_id,
            top_k=top_k,
        )
        return results
