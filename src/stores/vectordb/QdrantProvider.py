from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from src.helpers.config import get_settings
import logging
import uuid

logger = logging.getLogger("uvicorn.error")


class QdrantProvider:

    def __init__(self):
        self.settings = get_settings()
        self.client = QdrantClient(url=self.settings.QDRANT_URL)
        self.collection_name = self.settings.QDRANT_COLLECTION_NAME

    def init_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.settings.VECTOR_EMBEDDING_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Qdrant collection '{self.collection_name}' created.")
        else:
            logger.info(f"Qdrant collection '{self.collection_name}' already exists.")

    def upsert_vectors(self, vectors: list[dict]):
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=item["vector"],
                payload={
                    "chunk_text": item["chunk_text"],
                    "chunk_order": item["chunk_order"],
                    "project_id": item["project_id"],
                },
            )
            for item in vectors
        ]
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        return len(points)

    def search(self, query_vector: list[float], project_id: str, top_k: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="project_id",
                        match=MatchValue(value=project_id),
                    )
                ]
            ),
            with_payload=True,
        )
        return [
            {
                "chunk_text": r.payload["chunk_text"],
                "chunk_order": r.payload["chunk_order"],
                "project_id": r.payload["project_id"],
                "score": r.score,
            }
            for r in results
        ]
