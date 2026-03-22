from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Message:
    id: Optional[int]
    username: str
    content: str
    timestamp: datetime

    def to_dict(self):
        ts = self.timestamp
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        return {
            'id': self.id,
            'username': self.username,
            'content': self.content,
            'timestamp': ts.isoformat()
        }

    @classmethod
    def from_row(cls, row: tuple):
        ts = row[3]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        return cls(
            id=row[0],
            username=row[1],
            content=row[2],
            timestamp=ts
        )
