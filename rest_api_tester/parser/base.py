from typing import Protocol, Union, Any

from rest_api_tester.test import TestData


class ParserProto(Protocol):

    @staticmethod
    def parse(
        path_to_data: str,
        path_to_test_cases: str,
        test_name: str,
        request_json_modifiers: Union[dict[str, Any], None],
        response_json_modifiers: Union[dict[str, Any], None]
    ) -> TestData:
        ...
