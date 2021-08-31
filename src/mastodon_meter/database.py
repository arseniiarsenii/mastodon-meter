import os
import typing as tp
from dataclasses import asdict

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor, AsyncIOMotorDatabase

from .Account import Account
from .Metering import Metering
from .Singleton import SingletonMeta
from .Types import Document


class MongoDbWrapper(metaclass=SingletonMeta):
    """A database wrapper implementation for MongoDB"""

    def __init__(self) -> None:
        """connect to database using credentials"""
        logger.info("Connecting to MongoDB")
        mongo_client_url: tp.Optional[str] = os.getenv("MONGO_CONNECTION_URL")

        if mongo_client_url is None:
            message = "Cannot establish database connection: $MONGO_CONNECTION_URL environment variable is not set."
            logger.critical(message)
            raise IOError(message)

        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_client_url)

        self._database: AsyncIOMotorDatabase = mongo_client["mastodon-meter"]
        self._meterings_collection: AsyncIOMotorCollection = self._database["meterings"]
        self._tracked_accounts_collection: AsyncIOMotorCollection = self._database["tracked-accounts"]

        logger.info("Connected to MongoDB")

    @staticmethod
    async def _find_matching_documents(key: str, value: str, collection_: AsyncIOMotorCollection) -> tp.List[Document]:
        """
        finds all elements in the specified collection, which have
        specified key matching specified value
        """
        cursor: AsyncIOMotorCursor = collection_.find({key: value})
        result: tp.List[Document] = []

        for doc in await cursor.to_list(length=100):
            del doc["_id"]
            result.append(doc)

        return result

    @staticmethod
    async def _get_all_items_in_collection(collection_: AsyncIOMotorCollection) -> tp.List[Document]:
        """get all documents in the provided collection"""
        cursor: AsyncIOMotorCursor = collection_.find()
        result: tp.List[Document] = []

        for doc in await cursor.to_list(length=100):
            del doc["_id"]
            result.append(doc)

        return result

    async def add_tracked_account(self, account: Account) -> None:
        """add the provided account into the list of tracked accounts"""
        collection: AsyncIOMotorCollection = self._tracked_accounts_collection
        await collection.insert_one(asdict(account))

    async def delete_tracked_account(self, account_internal_id: str) -> None:
        """delete the provided account from the list of tracked accounts"""
        collection: AsyncIOMotorCollection = self._tracked_accounts_collection
        await collection.delete_one({"internal_id": account_internal_id})

    async def get_tracked_accounts(self) -> tp.List[Account]:
        """get the list of all tracked accounts"""
        collection: AsyncIOMotorCollection = self._tracked_accounts_collection
        tracked_accounts = await self._get_all_items_in_collection(collection)
        return [Account(**data) for data in tracked_accounts]

    async def add_meterings(self, meterings: tp.List[Metering]) -> None:
        """add the provided metering into the database"""
        collection: AsyncIOMotorCollection = self._meterings_collection
        metering_documents: tp.List[Document] = [asdict(m) for m in meterings]
        await collection.insert_many(metering_documents)

    async def delete_meterings(self, metering_ids: tp.Set[str]) -> None:
        """delete the provided metering from the database"""
        collection: AsyncIOMotorCollection = self._meterings_collection
        for metering_id in metering_ids:
            await collection.delete_one({"internal_id": metering_id})

    async def get_all_meterings(self, account_internal_id: str) -> tp.List[Metering]:
        """get all meterings for an account from the database"""
        metering_data: tp.List[Document] = await self._find_matching_documents(
            "parent_account_internal_id",
            account_internal_id,
            self._meterings_collection,
        )
        return [Metering(**data) for data in metering_data]
