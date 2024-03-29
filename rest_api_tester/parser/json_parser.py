import os
import json
from typing import Any, Union, Dict

from rest_api_tester.test import TestData
from rest_api_tester.parser.base_parser import BaseParser
from rest_api_tester import utils

EXTERNAL_FILE_PREFIX = 'file::'


class JSONParser(BaseParser):

    @staticmethod
    def parse(
        path_to_scenarios_dir: str,
        path_to_test_cases: str,
        test_name: str,
        request_json_modifiers: Union[Dict[str, Any], None],
        response_json_modifiers: Union[Dict[str, Any], None],
        request_header_modifiers: Union[Dict[str, Any], None],
        response_header_modifiers: Union[Dict[str, Any], None],
    ) -> TestData:
        test_cases_file_path = os.path.join(path_to_scenarios_dir, path_to_test_cases)
        with open(test_cases_file_path, 'r') as f:
            test_cases = json.loads(f.read())

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
        if request is not None:
            if isinstance(request, (dict, list)):
                request = json.dumps(request)
            elif isinstance(request, str):
                if request.startswith(EXTERNAL_FILE_PREFIX):
                    request_file_path = os.path.join(path_to_scenarios_dir, request[len(EXTERNAL_FILE_PREFIX):])
                    with open(request_file_path, 'r') as f:
                        request = str(f.read().strip())
            else:
                raise Exception('Request format is invalid')

        if request_json_modifiers:
            request_json = json.loads(request or '{}')
            for path, value in request_json_modifiers.items():
                request_json = utils.json_update(j=request_json, path=path, value=value)
            request = json.dumps(request_json)

        if request_header_modifiers:
            headers = test_case.get('headers') or {}
            for path, value in request_header_modifiers.items():
                headers = utils.json_update(j=headers, path=path, value=value)
            test_case['headers'] = headers

        response = test_case.get('response')
        if response is not None:
            if isinstance(response, (dict, list)):
                response = json.dumps(response)
            elif isinstance(response, str):
                if response.startswith(EXTERNAL_FILE_PREFIX):
                    response_file_path = os.path.join(path_to_scenarios_dir, response[len(EXTERNAL_FILE_PREFIX):])
                    with open(response_file_path, 'r') as f:
                        response = str(f.read().strip())
            else:
                raise Exception('Response format is invalid')

        if response_json_modifiers:
            response_json = json.loads(response or '{}')
            for path, value in response_json_modifiers.items():
                response_json = utils.json_update(j=response_json, path=path, value=value)
            response = json.dumps(response_json)

        if response_header_modifiers:
            response_headers = test_case.get('response_headers') or {}
            for path, value in response_header_modifiers.items():
                response_headers = utils.json_update(j=response_headers, path=path, value=value)
            test_case['response_headers'] = response_headers

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
            file_path=test_cases_file_path,
            description=test_case.get('description')
        )
