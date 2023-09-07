from typing import Any, Callable, Union
from dataclasses import dataclass
import unittest
import pprint
import ujson

from rest_api_tester.client.response_data import ResponseData


@dataclass
class TestData:

    name: str
    url: str
    method: str
    allow_redirects: bool
    headers: dict[str, Any]
    cookies: dict[str, Any]
    request_data: Union[str, None]
    expected_status: int
    expected_response: Union[str, None]
    expected_headers: Union[dict[str, Any], None]
    __test__ = False


@dataclass
class TestResult:

    response: ResponseData
    test_data: TestData
    __test__ = False


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def verify_test_result(
        self,
        result: TestResult,
        verifier: Union[Callable[[TestResult], None], None] = None
    ) -> None:
        """
        Verifies that the test case result matches what is expected

        :param result:
            The test case result returned from `TestCaseRunner.run()`
        :param verifier:
            A function used to verify the response body.
            This function should typically be defined as a test case instance method so `self.assert...` methods
            can be utilized. If not provided, the `default_verifier` function from this class will be used.
        """

        # Check status
        actual_response = result.response.text
        actual_status = result.test_data.expected_status
        expected_status = result.response.status_code
        expected_response = result.test_data.expected_response
        message = '\n'.join([
            '',
            'Expected Response:',
            self._format_response(response=expected_response),
            '',
            'Actual Response:',
            self._format_response(response=actual_response),
            ''
        ])
        self.assertEqual(expected_status, actual_status, message)

        # Check response body
        verifier = verifier or self.default_verifier
        verifier(result)

        # Check response headers
        expected_headers = result.test_data.expected_headers
        if expected_headers:
            actual_headers = result.response.headers
            self.assertDictEqual(expected_headers, dict(actual_headers))

    def default_verifier(self, result: TestResult) -> None:
        response_content_type = result.response.headers.get('content-type')

        expected_response = result.test_data.expected_response
        if expected_response:
            if response_content_type == 'application/json':
                actual_response = ujson.loads(result.response.text)
                if isinstance(actual_response, list):
                    self.assertListEqual(ujson.loads(expected_response), actual_response)
                elif isinstance(actual_response, dict):
                    self.assertDictEqual(ujson.loads(expected_response), actual_response)
            else:
                actual_response = result.response.text
                self.assertEqual(expected_response, actual_response)

    @staticmethod
    def _format_response(response: Union[str, None]) -> Any:
        if response in (None, ''):
            return '<None>'

        try:
            return pprint.pformat(ujson.loads(response))  # type: ignore
        except Exception:
            return response
