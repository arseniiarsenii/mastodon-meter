import typing as tp
from abc import ABC, abstractmethod

from .Metering import Metering


class DatabaseWrapper(ABC):
    """a common database wrapper interface"""

    @abstractmethod
    def add_tracked_account(self, account_id: str, instance_url: str) -> None:
        """add the provided account into the list of tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def delete_tracked_account(self, account_id: str, instance_url: str) -> None:
        """delete the provided account from the list of tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def add_meterings(self, meterings: tp.Set[Metering]) -> None:
        """add the provided metering into the database"""
        raise NotImplementedError

    @abstractmethod
    def delete_meterings(self, metering_ids: tp.Set[str]) -> None:
        """delete the provided metering from the database"""
        raise NotImplementedError

    @abstractmethod
    def get_all_meterings(self, account_internal_id: str) -> None:
        """get all meterings for an account from the database"""
        raise NotImplementedError
