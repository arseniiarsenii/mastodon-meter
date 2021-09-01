import typing as tp
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
class Metering:
    """Stores information gathered in one metering"""

    toot_count: int
    subscribers_count: int
    parent_account_internal_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.utcnow())
    internal_id: str = field(default_factory=lambda: uuid4().hex)

    def is_within_range(self, from_: tp.Optional[datetime], to: tp.Optional[datetime]) -> bool:
        """determine ig the metering is within the given time range"""
        return all(
            (
                from_ is None or self.timestamp >= from_,
                to is None or self.timestamp <= to,
            )
        )
