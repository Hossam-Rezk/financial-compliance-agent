from .BaseDataModel import BaseDataModel
from src.models.db_schemes import project
from .db_schemes import Project
from .enums.DbEnum import DbEnum

class ProjectModel(BaseDataModel):
    def __init__(self, database_client):
        super().__init__(database_client=database_client)
        self.collection = self.db_client[DbEnum.Collection_Project_Name.value]

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.dict(by_alias=True))
        project.id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        record = await self.collection.find_one({"project_id": project_id})
        if record:
            return Project(**record)
        else:
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)
            return project

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        total_documents = await self.collection.count_documents({})
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_pages