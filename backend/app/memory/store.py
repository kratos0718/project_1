from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import MemoryRecord


class MemoryStore:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def remember(
        self,
        memory_type: str,
        content: str,
        locality: str | None = None,
        source_complaint_id: str | None = None,
        importance: int = 1,
    ) -> MemoryRecord:
        record = MemoryRecord(
            memory_type=memory_type,
            locality=locality,
            content=content,
            source_complaint_id=source_complaint_id,
            importance=importance,
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def relevant(self, locality: str, limit: int = 6) -> list[MemoryRecord]:
        result = await self.session.execute(
            select(MemoryRecord)
            .where(MemoryRecord.locality == locality)
            .order_by(MemoryRecord.importance.desc(), MemoryRecord.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

