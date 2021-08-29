from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Account:
    """Stores information about the tracked account"""

    username: str
    instance: str
    id: str
    internal_id: str = field(default_factory=lambda: uuid4().hex)
    added_on: datetime = field(default_factory=lambda: datetime.utcnow())
