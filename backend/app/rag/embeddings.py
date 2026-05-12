from app.config.settings import Settings


class EmbeddingService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not self.settings.openai_api_key:
            return [self._deterministic_embedding(text) for text in texts]

        from langchain_openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(
            model=self.settings.embedding_model,
            api_key=self.settings.openai_api_key,
        )
        return await embeddings.aembed_documents(texts)

    async def embed_query(self, text: str) -> list[float]:
        return (await self.embed_documents([text]))[0]

    def _deterministic_embedding(self, text: str, dimensions: int = 128) -> list[float]:
        vector = [0.0] * dimensions
        for index, char in enumerate(text.lower()):
            vector[(ord(char) + index) % dimensions] += 1.0
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        return [value / norm for value in vector]

