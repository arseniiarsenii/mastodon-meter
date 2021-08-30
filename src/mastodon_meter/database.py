import os
import typing as tp
from abc import ABC, abstractmethod
from dataclasses import asdict

from loguru import logger
from pymongo import MongoClient

from .Account import Account
from .Metering import Metering
from .Singleton import SingletonMeta
from .Types import Collection, Document


class DatabaseWrapper(ABC):
    """a common database wrapper interface"""

    @abstractmethod
    def add_tracked_account(self, account: Account) -> None:
        """add the provided account into the list of tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def delete_tracked_account(self, account_internal_id: str) -> None:
        """delete the provided account from the list of tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def get_tracked_accounts(self) -> tp.List[Account]:
        """get the list of all tracked accounts"""
        raise NotImplementedError

    @abstractmethod
    def add_meterings(self, meterings: tp.List[Metering]) -> None:
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


# not using inheritance because ABC and metaclasses don't work well together
class MongoDbWrapper(metaclass=SingletonMeta):
    """A database wrapper implementation for MongoDB"""

    def __init__(self) -> None:
        """connect to database using credentials"""
        logger.info("Connecting to MongoDB")
        username: str = str(os.getenv("MONGO_USERNAME"))
        password: str = str(os.getenv("MONGO_PASSWORD"))
        cluster_url: str = str(os.getenv("MONGO_CLUSTER"))
        assert all((username, password, cluster_url))
        mongo_client_url: str = (
            f"mongodb+srv://{username}:{password}@{cluster_url}/mastodon-meter?retryWrites=true&w=majority"
        )
        mongo_client: MongoClient = MongoClient(mongo_client_url)
        logger.info("Connected to MongoDB")

        self._database = mongo_client["mastodon-meter"]
        self._meterings_collection: Collection = self._database["meterings"]
        self._tracked_accounts_collection: Collection = self._database["tracked-accounts"]

    @staticmethod
    def _find_matching_documents(key: str, value: str, collection_: Collection) -> tp.List[Document]:
        """
        finds all elements in the specified collection, which have
        specified key matching specified value
        """
        result: tp.List[Document] = list(collection_.find({key: value}))

        for doc in result:
            del doc["_id"]

        return result

    @staticmethod
    def _get_all_items_in_collection(collection_: Collection) -> tp.List[Document]:
        """get all documents in the provided collection"""
        result: tp.List[Document] = list(collection_.find())

        for doc in result:
            del doc["_id"]

        return result

    def add_tracked_account(self, account: Account) -> None:
        """add the provided account into the list of tracked accounts"""
        collection: Collection = self._tracked_accounts_collection
        collection.insert_one(asdict(account))

    def delete_tracked_account(self, account_internal_id: str) -> None:
        """delete the provided account from the list of tracked accounts"""
        collection: Collection = self._tracked_accounts_collection
        collection.delete_one({"internal_id": account_internal_id})

    def get_tracked_accounts(self) -> tp.List[Account]:
        """get the list of all tracked accounts"""
        collection: Collection = self._tracked_accounts_collection
        tracked_accounts = self._get_all_items_in_collection(collection)
        return [Account(**data) for data in tracked_accounts]

    def add_meterings(self, meterings: tp.List[Metering]) -> None:
        """add the provided metering into the database"""
        collection: Collection = self._meterings_collection
        metering_documents: tp.List[Document] = [asdict(m) for m in meterings]
        collection.insert_many(metering_documents)

    def delete_meterings(self, metering_ids: tp.Set[str]) -> None:
        """delete the provided metering from the database"""
        collection: Collection = self._meterings_collection
        for metering_id in metering_ids:
            collection.delete_one({"internal_id": metering_id})

    def get_all_meterings(self, account_internal_id: str) -> tp.List[Metering]:
        """get all meterings for an account from the database"""
        metering_data: tp.List[Document] = self._find_matching_documents(
            "parent_account_internal_id",
            account_internal_id,
            self._meterings_collection,
        )
        return [Metering(**data) for data in metering_data]
