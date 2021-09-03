import typing as tp

from pydantic import BaseModel


class ResponseBase(BaseModel):
    """basic response model"""

    status: bool
    message: str


class AddAccountRequest(BaseModel):
    """a request to add account to the list of tracked"""

    username: str
    instance: str
    instance_id: str


class AddAccountResponse(ResponseBase):
    """a request to add account to the list of tracked"""

    account_internal_id: str


class DeleteAccountRequest(BaseModel):
    """a request to delete an account from the list of tracked"""

    account_internal_id: str
    remove_associated_data: bool


class TrackedAccountList(ResponseBase):
    """a request to retrieve the list of tracked accounts"""

    tracked_accounts: tp.List[tp.Dict[str, str]]


class AccountRawData(AddAccountResponse):
    """a request to retrieve the list of meterings for an account"""

    data: tp.List[tp.Dict[str, tp.Union[int, str]]]


class GraphRequest(BaseModel):
    """a request to retrieve a graph for an account"""

    since: tp.Optional[str]
    to: tp.Optional[str]


class GetReportRequest(BaseModel):
    """a request to retrieve a simple text report"""

    accounts: tp.Optional[tp.List[str]]


class GetReportResponse(ResponseBase):
    """a response holding a simple text report"""

    report: str
