import ujson
from dataclasses import dataclass
from typing import Any, Union, Dict


@dataclass
class ResponseData:

    text: str
    headers: Dict[str, Any]
    status_code: int
    extra: Union[Dict[str, Any], None] = None

    @property
    def json(self) -> Any:
        return ujson.loads(self.text)
