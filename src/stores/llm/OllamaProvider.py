import ollama
from src.helpers.config import get_settings


class OllamaProvider:

    def __init__(self):
        self.settings = get_settings()
        self.client = ollama.AsyncClient(host=self.settings.OLLAMA_BASE_URL)

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat(
            model=self.settings.OLLAMA_MODEL,
            messages=messages
        )
        return response["message"]["content"]

    async def embed(self, text: str) -> list[float]:
        response = await self.client.embeddings(
            model=self.settings.OLLAMA_EMBED_MODEL,
            prompt=text
        )
        return response["embedding"]
