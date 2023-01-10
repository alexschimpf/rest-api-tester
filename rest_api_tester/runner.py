from typing import Any, Union, Dict, Callable, cast

from rest_api_tester.client import BaseTestClient
from rest_api_tester.test import TestResult, TestData
from rest_api_tester.parser import json_parser


class TestCaseRunner:

    __test__ = False

    def __init__(
        self,
        client: BaseTestClient,
        path_to_data: str,
        request_timeout: int = 10,
        default_content_type: Union[str, None] = None
    ):
        """
        :param client: test client that will make requests to your server
        :param path_to_data: absolute path to the directory containing test case files
        :param request_timeout: in seconds
        :param default_content_type:
            - if given, this will automatically be added to all test case request headers
            - if a test case already includes a 'Content-Type' header, that will be used instead
        """

        self.client = client
        self.path_to_data = path_to_data
        self.request_timeout = request_timeout
        self.default_content_type = default_content_type

    def run(
        self,
        path_to_test_cases: str,
        test_name: str,
        url_params: Union[Dict[str, Any], None] = None,
        file_parser: Callable[[str, str, str], TestData] = json_parser.parse,
        test_data_modifier: Union[Callable[[TestData], TestData], None] = None
    ) -> TestResult:
        """
        Runs a test and returns a TestResult
        You can verify the result using `test.TestCase.verify_test_result()`

        :param path_to_test_cases: this is relative to the "path_to_data" folder
        :param test_name: the JSON key that is associated with the test in the test file
        :param url_params:
            - used to fill in test URLs dynamically
            - e.g. if URL='/items/{item_id}' and url_params={'item_id': 1}, the URL will become '/items/1'
        :param file_parser:
            - this function parses a test cases file and returns a TestData object for a given test case
            - it takes the following arguments: (path_to_data, path_to_test_cases, test_name)
        :param test_data_modifier: function to modify the test data before the test is run
        """

        test_data = self._get_test_data(
            path_to_test_cases=path_to_test_cases,
            test_name=test_name,
            url_params=url_params,
            file_parser=file_parser,
            test_data_modifier=test_data_modifier
        )
        return self._run(test_data=test_data)

    def _get_test_data(
        self,
        path_to_test_cases: str,
        test_name: str,
        url_params: Union[Dict[str, Any], None] = None,
        file_parser: Callable[[str, str, str], TestData] = json_parser.parse,
        test_data_modifier: Union[Callable[[TestData], TestData], None] = None
    ) -> TestData:
        test_data = file_parser(self.path_to_data, path_to_test_cases, test_name)

        test_data.headers = test_data.headers or {}
        if self.default_content_type and 'Content-Type' not in test_data.headers:
            test_data.headers['Content-Type'] = self.default_content_type

        if url_params:
            test_data.url = test_data.url.format(**url_params)

        if test_data_modifier:
            test_data = test_data_modifier(test_data)

        return test_data

    def _run(self, test_data: TestData) -> TestResult:
        method = test_data.method

        if method == 'GET':
            response = self.client.get(
                url=test_data.url,
                headers=test_data.headers,
                cookies=test_data.cookies,
                timeout=self.request_timeout,
                allow_redirects=test_data.allow_redirects
            )
        elif method == 'POST':
            response = self.client.post(
                url=test_data.url,
                headers=test_data.headers,
                cookies=test_data.cookies,
                data=cast(str, test_data.request_data),
                timeout=self.request_timeout,
                allow_redirects=test_data.allow_redirects
            )
        elif method == 'PUT':
            response = self.client.put(
                url=test_data.url,
                headers=test_data.headers,
                cookies=test_data.cookies,
                data=cast(str, test_data.request_data),
                timeout=self.request_timeout,
                allow_redirects=test_data.allow_redirects
            )
        elif method == 'PATCH':
            response = self.client.patch(
                url=test_data.url,
                headers=test_data.headers,
                cookies=test_data.cookies,
                data=cast(str, test_data.request_data),
                timeout=self.request_timeout,
                allow_redirects=test_data.allow_redirects
            )
        elif method == 'DELETE':
            response = self.client.delete(
                url=test_data.url,
                headers=test_data.headers,
                cookies=test_data.cookies,
                timeout=self.request_timeout,
                allow_redirects=test_data.allow_redirects
            )
        else:
            raise ValueError('Unsupported HTTP method')

        return TestResult(
            response=response,
            test_data=test_data
        )
