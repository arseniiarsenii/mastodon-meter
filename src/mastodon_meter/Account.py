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

    @property
    def account_data_link(self) -> str:
        """a link pointing to an account entity (https://docs.joinmastodon.org/entities/account/)"""
        return f"{self.instance}/api/v1/accounts/{self.id}"

    @property
    def full_address(self) -> str:
        instance: str = self.instance.split("//")[-1]
        return f"{self.username}@{instance}"
