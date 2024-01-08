from typing import Any, Callable, Union, Dict, List
from dataclasses import dataclass
import unittest
import pprint
import ujson

from rest_api_tester.client.response_data import ResponseData
from rest_api_tester import utils


@dataclass
class TestData:

    name: str
    url: str
    method: str
    allow_redirects: bool
    headers: Dict[str, Any]
    cookies: Dict[str, Any]
    request_data: Union[str, None]
    expected_status: int
    expected_response: Union[str, None]
    expected_headers: Union[Dict[str, Any], None]
    description: Union[str, None]
    file_path: str
    __test__ = False

    @property
    def request_data_json(self) -> Any:
        if not self.request_data:
            return None
        return ujson.loads(self.request_data)

    @property
    def expected_response_json(self) -> Any:
        if not self.expected_response:
            return None
        return ujson.loads(self.expected_response)


@dataclass
class TestResult:

    response: ResponseData
    test_data: TestData
    __test__ = False


@dataclass
class UpdateScenariosOnFailOptions:

    update_headers: bool = False


class TestCase(unittest.TestCase):

    def __init__(self, methodName: str = 'runTest') -> None:
        self.maxDiff = None
        self.update_scenarios_on_fail = False
        self.update_scenarios_on_fail_options = UpdateScenariosOnFailOptions()
        super().__init__(methodName=methodName)

    def verify_test_result(
        self,
        result: TestResult,
        verifier: Union[Callable[[TestResult], None], None] = None,
        excluded_response_paths: Union[List[str], None] = None,
        update_scenarios_on_fail: bool = False,
        update_scenarios_on_fail_options: Union[UpdateScenariosOnFailOptions, None] = None
    ) -> None:
        """
        Verifies that the test case result matches what is expected

        :param result:
            The test case result returned from `TestCaseRunner.run()`
        :param verifier:
            A function used to verify the response body.
            This function should typically be defined as a test case instance method so `self.assert...` methods
            can be utilized. If not provided, the `default_verifier` function from this class will be used.
        :param excluded_response_paths:
            A list of JSON paths that define which elements of the actual response body will be
            excluded during verification.
            See `rest_api_tester.utils.json_remove` for more details.
        :param update_scenarios_on_fail:
            If True, scenario files will automatically be updated when tests fail.
            This can be useful if you want to quickly set up your test scenarios.
            This can also be set for the entire test case instance via the instance
            variable `update_scenarios_on_fail`.
            Note: This may corrupt scenario files if tests are run in parallel or if tests are abruptly killed.
        :param update_scenarios_on_fail_options:
            Options for `update_scenarios_on_fail` behavior
        """

        update_scenarios_on_fail = any((
            update_scenarios_on_fail,
            self.update_scenarios_on_fail
        ))

        update_scenarios_on_fail_options = update_scenarios_on_fail_options or self.update_scenarios_on_fail_options

        expected_status = result.test_data.expected_status
        expected_response = result.test_data.expected_response
        actual_status = result.response.status_code
        actual_response = result.response.text

        if excluded_response_paths:
            actual_response_dict = result.response.json
            expected_response_dict = result.test_data.expected_response_json
            for excluded_response_path in excluded_response_paths:
                actual_response_dict = utils.json_update(
                    j=actual_response_dict, path=excluded_response_path, value='$$$')
                expected_response_dict = utils.json_update(
                    j=expected_response_dict, path=excluded_response_path, value='$$$')
            result.response.text = ujson.dumps(actual_response_dict)
            result.test_data.expected_response = ujson.dumps(expected_response_dict)

        try:
            # Check status
            message = [
                '',
                'Expected Response:',
                self._format_response(response=expected_response),
                '',
                'Actual Response:',
                self._format_response(response=actual_response),
                ''
            ]
            if result.test_data.description:
                message = ['', f'Test Description: {result.test_data.description}', ''] + message
            message_str = '\n'.join(message)
            self.assertEqual(expected_status, actual_status, message_str)

            # Check response body
            verifier = verifier or self.default_verifier
            verifier(result)

            # Check response headers
            expected_headers = result.test_data.expected_headers
            if expected_headers:
                actual_headers = result.response.headers
                message = ['', 'Headers do not match', '']
                if result.test_data.description:
                    message = ['', f'Test Description: {result.test_data.description}', ''] + message
                self.assertDictEqual(expected_headers, dict(actual_headers), '\n'.join(message))
        except Exception:
            if update_scenarios_on_fail:
                self._update_scenario(result=result, options=update_scenarios_on_fail_options)
            raise

    def default_verifier(self, result: TestResult) -> None:
        response_content_type = result.response.headers.get('content-type')

        expected_response = result.test_data.expected_response
        if expected_response:
            if response_content_type == 'application/json':
                actual_response = result.response.json
                if isinstance(actual_response, list):
                    self.assertListEqual(ujson.loads(expected_response), actual_response)
                elif isinstance(actual_response, dict):
                    self.assertDictEqual(ujson.loads(expected_response), actual_response)
            else:
                actual_response = result.response.text
                self.assertEqual(expected_response, actual_response)

    @staticmethod
    def _update_scenario(result: TestResult, options: UpdateScenariosOnFailOptions) -> None:
        actual_response = result.response.text
        actual_status = result.response.status_code
        actual_headers = result.response.headers

        print(f'\n\nUpdating test scenario {result.test_data.file_path}::{result.test_data.name}')

        with open(result.test_data.file_path, 'r') as f:
            scenarios = ujson.loads(f.read())
            scenario = scenarios[result.test_data.name]
            scenario['status'] = actual_status
            if options.update_headers:
                scenario['response_headers'] = actual_headers

            if actual_response:
                # TODO: Use case-insensitive dict instead?
                content_type = (
                    actual_headers.get('Content-Type') or
                    actual_headers.get('content-type') or
                    actual_headers.get('CONTENT-TYPE')
                )
                if content_type == 'application/json':
                    scenario['response'] = ujson.loads(actual_response)
                else:
                    scenario['response'] = actual_response
            else:
                scenario.pop('response', None)

        with open(result.test_data.file_path, 'w+') as f:
            f.write(ujson.dumps(scenarios, escape_forward_slashes=False, indent=4) + '\n')

    @staticmethod
    def _format_response(response: Union[str, None]) -> Any:
        if response in (None, ''):
            return '<Empty Response>'

        try:
            return pprint.pformat(ujson.loads(response))  # type: ignore
        except Exception:
            return response
