import typing as tp

from fastapi.responses import FileResponse

from .Account import Account
from .Metering import Metering

Document = tp.Dict[str, tp.Any]
ResponsePayload = tp.Dict[str, tp.Any]
GraphData = tp.Tuple[tp.List[Metering], Account]
FileOrError = tp.Union[ResponsePayload, FileResponse]
