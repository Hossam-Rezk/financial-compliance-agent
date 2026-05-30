from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from src.models.enums import processEnum
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_dir(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[1].lower()

    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)
        if file_ext == processEnum.ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_ext == processEnum.ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def get_file_content(self, file_id: str):
        try:
            loader = self.get_file_loader(file_id=file_id)
            documents = loader.load()
            return documents
        except Exception as e:
            raise ValueError(f"Error processing file: {e}")

    def process_file_content(self, file_content: list, file_id: str, chunk_size: int = 100, overlap_size: int = 20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size
        )

        file_content_texts = [
            rec.page_content for rec in file_content  # ← {} → [], page.content → page_content
        ]
        file_content_metadata = [
            rec.metadata for rec in file_content       # ← {} → []
        ]

        try:
            chunks = text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)
            return chunks
        except Exception as e:
            raise ValueError(f"Error splitting file content: {e}")