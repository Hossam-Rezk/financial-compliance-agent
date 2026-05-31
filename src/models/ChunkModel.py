from .BaseDataModel import BaseDataModel
from.db_schemes import DataChunk
from .enums.DbEnum import DbEnum
from pymongo import InsertOne 

class ChunkModel(BaseDataModel):
    def __init__(self, database_client):
        super().__init__(database_client=database_client)
        self.collection = self.db_client[DbEnum.Collection_Chunk_Name.value]

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict())
        chunk.id = result.inserted_id
        return chunk

    async def get_chunks_by_project_id(self, project_id: str):
        result = await self.collection.find({"chunk_metadata.project_id": project_id}).to_list(length=None)
        if result is None:
            return None
        return DataChunk(**result)
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.dict()) for chunk in batch]
            await self.collection.bulk_write(operations)
        return len(chunks)
    
    
            
          