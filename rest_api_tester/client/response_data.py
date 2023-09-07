from dataclasses import dataclass
from typing import Any, Union


@dataclass
class ResponseData:

    text: str
    headers: dict[str, Any]
    status_code: int
    extra: Union[dict[str, Any], None] = None
