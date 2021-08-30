import typing as tp

import httpx

from .Account import Account
from .Metering import Metering
from .Types import ResponsePayload
from .database import DatabaseWrapper, MongoDbWrapper


class Gatherer:
    """Gathers data for all the tracked accounts and stores it in the database"""

    def __init__(self) -> None:
        self.db_wrapper: DatabaseWrapper = MongoDbWrapper()

    def get_data_for_an_account(self, account_internal_id: str) -> tp.List[Metering]:
        """get all meterings for an account from the database"""
        return self.db_wrapper.get_all_meterings(account_internal_id)

    def gather_meterings(self) -> None:
        """do meterings for all the tracked accounts"""
        tracked_accounts: tp.Set[Account] = self.db_wrapper.get_tracked_accounts()
        meterings: tp.Set[Metering] = set()

        for account in tracked_accounts:
            metering: Metering = self._meter(account)
            meterings.add(metering)

        self.db_wrapper.add_meterings(meterings)

    @staticmethod
    def _meter(account: Account) -> Metering:
        """get data for an account and package it into a Metering object"""
        response: httpx.Response = httpx.get(account.account_data_link)
        response_payload: ResponsePayload = response.json()
        metering: Metering = Metering(
            toot_count=response_payload["statuses_count"],
            subscribers_count=response_payload["followers_count"],
            parent_account_internal_id=account.internal_id,
        )
        return metering
