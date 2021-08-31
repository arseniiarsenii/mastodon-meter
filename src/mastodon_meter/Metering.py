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
