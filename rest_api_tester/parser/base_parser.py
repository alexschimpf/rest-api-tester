from abc import ABC, abstractmethod
from typing import Union, Any, Dict

from rest_api_tester.test import TestData


class BaseParser(ABC):

    @staticmethod
    @abstractmethod
    def parse(
        path_to_scenarios_dir: str,
        path_to_test_cases: str,
        test_name: str,
        request_json_modifiers: Union[Dict[str, Any], None],
        response_json_modifiers: Union[Dict[str, Any], None]
    ) -> TestData:
        ...
