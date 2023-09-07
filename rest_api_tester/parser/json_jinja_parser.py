import os
import ujson
import jinja2
from typing import Any, Union

from rest_api_tester.test import TestData
from rest_api_tester.parser.base import ParserProto
from rest_api_tester.config import Config

EXTERNAL_FILE_PREFIX = 'file::'


class JsonJinjaParser(ParserProto):

    @staticmethod
    def parse(
        path_to_data: str,
        path_to_test_cases: str,
        test_name: str,
        request_template_vars: Union[dict[str, Any], None],
        response_template_vars: Union[dict[str, Any], None]
    ) -> TestData:
        jinja_env = jinja2.Environment(**Config.JINJA_SETTINGS)

        test_cases_file_path = os.path.join(path_to_data, path_to_test_cases)
        with open(test_cases_file_path, 'r') as f:
            test_cases = ujson.loads(f.read())

        test_case = test_cases[test_name]

        assert isinstance(test_case.get('url'), str)
        assert isinstance(test_case.get('status'), int)
        assert isinstance(test_case.get('method'), str)
        if 'cookies' in test_case:
            assert isinstance(test_case['cookies'], dict)
        if 'headers' in test_case:
            assert isinstance(test_case['headers'], dict)
        if 'response_headers' in test_case:
            assert isinstance(test_case['response_headers'], dict)
        if 'allow_redirects' in test_case:
            assert isinstance(test_case['allow_redirects'], bool)

        request = test_case.get('request')
        if request:
            if isinstance(request, dict):
                request = ujson.dumps(request)
            elif isinstance(request, str):
                if request.startswith(EXTERNAL_FILE_PREFIX):
                    request_file_path = os.path.join(path_to_data, request[len(EXTERNAL_FILE_PREFIX):])
                    with open(request_file_path, 'r') as f:
                        request = str(f.read().strip())
            else:
                raise Exception('Request format is invalid')

        if request_template_vars and request:
            request_template = jinja_env.from_string(request)
            request = request_template.render(**request_template_vars)

        response = test_case.get('response')
        if response:
            if isinstance(response, dict):
                response = ujson.dumps(response)
            elif isinstance(response, str):
                if response.startswith(EXTERNAL_FILE_PREFIX):
                    response_file_path = os.path.join(path_to_data, response[len(EXTERNAL_FILE_PREFIX):])
                    with open(response_file_path, 'r') as f:
                        response = str(f.read().strip())
            else:
                raise Exception('Response format is invalid')

        if response_template_vars and response:
            response_template = jinja_env.from_string(response)
            response = response_template.render(**response_template_vars)

        headers = test_case.get('headers')
        if headers:
            headers = {
                key.lower(): value for key, value in headers.items()
            }

        return TestData(
            name=test_name,
            url=test_case['url'],
            method=test_case['method'],
            headers=headers,
            cookies=test_case.get('cookies'),
            request_data=request,
            expected_status=test_case['status'],
            expected_response=response,
            expected_headers=test_case.get('response_headers'),
            allow_redirects=test_case.get('allow_redirects', True),
            file_path=test_cases_file_path
        )
