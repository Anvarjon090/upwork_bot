from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class SentJob:
    id: int | None
    job_id: str
    title: str
    sent_at: datetime | None = None
