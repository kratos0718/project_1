import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_embedding():
    class MockEmbedder:
        def embed_documents(self, texts):
            return [[0.1, 0.2, 0.3]] * len(texts)
        def embed_query(self, text):
            return [0.1, 0.2, 0.3]
    return MockEmbedder()

@pytest.fixture
def mock_llm_response():
    return {
        "severity_score": 5,
        "escalation_priority": "medium",
        "duplicate_id": None,
        "summary": "This is a mocked summary.",
        "category": "sanitation"
    }
