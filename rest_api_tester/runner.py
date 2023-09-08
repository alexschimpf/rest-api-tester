from typing import Any, Union, Callable, cast

from rest_api_tester.client.base_client import BaseTestClient
from rest_api_tester.test import TestResult, TestData
from rest_api_tester.parser.base import ParserProto
from rest_api_tester.parser.json_jinja_parser import JsonJinjaParser


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
        :param client:
            Test client that will make requests to your server
        :param path_to_data:
            Absolute path to the directory containing test case files
        :param request_timeout:
            In seconds
        :param default_content_type:
            If given, this will automatically be added to all test case request headers.
            If a test case already includes a 'Content-Type' header, that will be used instead.
        """

        self.client = client
        self.path_to_data = path_to_data
        self.request_timeout = request_timeout
        self.default_content_type = default_content_type

    def run(
        self,
        path_to_test_cases: str,
        test_name: str,
        url_params: Union[dict[str, Any], None] = None,
        file_parser: ParserProto = JsonJinjaParser,
        test_data_modifier: Union[Callable[[TestData], TestData], None] = None,
        request_template_vars: Union[dict[str, Any], None] = None,
        response_template_vars: Union[dict[str, Any], None] = None
    ) -> TestResult:
        """
        Runs a test and returns a TestResult
        You can verify the result using `test.TestCase.verify_test_result()`

        :param path_to_test_cases:
            This is relative to the "path_to_data" folder
        :param test_name:
            The JSON key that is associated with the test in the test file
        :param url_params:
            Used to fill in test URLs dynamically.
            For example, if URL='/items/{item_id}' and url_params={'item_id': 1}, the URL will become '/items/1'.
        :param file_parser:
            This class parses a test cases file and returns a TestData object for a given test case
        :param test_data_modifier:
            Function to modify the test data before the test is run.
            This is done after `request_template_vars` and `response_template_vars` are processed.
        :param request_template_vars:
            These key/values will be rendered into the test's request template
        :param response_template_vars:
            These key/values will be rendered into the test's expected response template
        """

        test_data = self._get_test_data(
            path_to_test_cases=path_to_test_cases,
            test_name=test_name,
            url_params=url_params,
            file_parser=file_parser,
            test_data_modifier=test_data_modifier,
            request_template_vars=request_template_vars,
            response_template_vars=response_template_vars
        )
        return self._run(test_data=test_data)

    def _get_test_data(
        self,
        path_to_test_cases: str,
        test_name: str,
        url_params: Union[dict[str, Any], None] = None,
        file_parser: ParserProto = JsonJinjaParser,
        test_data_modifier: Union[Callable[[TestData], TestData], None] = None,
        request_template_vars: Union[dict[str, Any], None] = None,
        response_template_vars: Union[dict[str, Any], None] = None
    ) -> TestData:
        test_data = file_parser.parse(
            path_to_data=self.path_to_data,
            path_to_test_cases=path_to_test_cases,
            test_name=test_name,
            request_template_vars=request_template_vars,
            response_template_vars=response_template_vars
        )

        test_data.headers = test_data.headers or {}
        if self.default_content_type and 'content-type' not in test_data.headers:
            test_data.headers['content-type'] = self.default_content_type

        if url_params:
            test_data.url = test_data.url.format(**url_params)

        if test_data_modifier:
            test_data = test_data_modifier(test_data)

        return test_data

    def _run(self, test_data: TestData) -> TestResult:
        method = test_data.method.upper()

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
