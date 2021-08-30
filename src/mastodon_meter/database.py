import os
import typing as tp
from abc import ABC, abstractmethod

from pymongo import MongoClient

from .Account import Account
from .Metering import Metering
from .Types import Collection


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
    def get_tracked_accounts(self) -> tp.Set[Account]:
        """get the list of all tracked accounts"""
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
    def get_all_meterings(self, account_internal_id: str) -> tp.List[Metering]:
        """get all meterings for an account from the database"""
        raise NotImplementedError


class MongoDbWrapper(DatabaseWrapper):
    """A database wrapper implementation for MongoDB"""

    def __init__(self) -> None:
        """connect to database using credentials"""
        username: str = os.getenv("MONGO_USERNAME")
        password: str = os.getenv("MONGO_PASSWORD")
        cluster_url: str = os.getenv("MONGO_CLUSTER")
        assert all((username, password, cluster_url))
        mongo_client_url: str = (
            f"mongodb+srv://{username}:{password}@{cluster_url}/mastodon-meter?retryWrites=true&w=majority"
        )
        mongo_client: MongoClient = MongoClient(mongo_client_url)

        self._database = mongo_client["mastodon-meter"]
        self._meterings_collection: Collection = self._database["meterings"]
        self._tracked_accounts_collection: Collection = self._database["tracked-accounts"]

    @abstractmethod
    def add_tracked_account(self, account_id: str, instance_url: str) -> None:
        """add the provided account into the list of tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def delete_tracked_account(self, account_id: str, instance_url: str) -> None:
        """delete the provided account from the list of tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def get_tracked_accounts(self) -> tp.Set[Account]:
        """get the list of all tracked accounts"""
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
    def get_all_meterings(self, account_internal_id: str) -> tp.List[Metering]:
        """get all meterings for an account from the database"""
        raise NotImplementedError
