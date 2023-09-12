import os
import string
import random
import ujson
from typing import Union, Any, Dict
from fastapi import FastAPI, Header
from fastapi.responses import Response, PlainTextResponse, RedirectResponse
from pydantic import BaseModel

from rest_api_tester.test import TestCase, TestData, TestResult
from rest_api_tester.runner import TestCaseRunner

from tests.api.fastapi.fastapi_test_client import FastAPITestClient


class Item(BaseModel):
    name: Union[str, None]


class TestJSON(TestCase):

    def setUp(self) -> None:
        self.items: Dict[Any, Any] = {}
        self.app = FastAPI()
        self.update_scenarios_on_fail = False

        @self.app.get('/status', response_class=PlainTextResponse)
        def get_status() -> Any:
            return 'OK'

        @self.app.get('/protected', response_class=PlainTextResponse)
        def get_protected(secret: str = Header()) -> Any:
            if secret != 's3cr3t!':
                return Response(status_code=401)
            return PlainTextResponse(
                content='OK',
                headers={
                    'test': 't3st'
                }
            )

        @self.app.get('/google', response_class=RedirectResponse)
        def get_google() -> Any:
            return RedirectResponse(
                url='https://google.com',
                status_code=301
            )

        @self.app.get('/items')
        def get_items() -> Any:
            return {
                'items': [
                    {'id': item_id, 'name': item_name}
                    for (item_id, item_name) in self.items.items()
                ]
            }

        @self.app.get('/items/{item_id}')
        def get_item(item_id: int) -> Any:
            if item_id not in self.items:
                return Response(
                    status_code=404
                )
            return {
                'id': item_id,
                'name': self.items[item_id]
            }

        @self.app.post('/items')
        def create_item(item: Item) -> Any:
            item_id = max(self.items.keys() or [0]) + 1
            self.items[item_id] = item.name or ''.join(random.choice(string.digits) for _ in range(8))
            return {
                'id': item_id,
                'name': item.name
            }

        @self.app.delete('/items/{item_id}')
        def delete_item(item_id: int) -> Any:
            if item_id not in self.items:
                return Response(
                    status_code=404
                )
            self.items.pop(item_id)
            return {
                'items': [
                    {'id': item_id, 'name': item_name}
                    for (item_id, item_name) in self.items.items()
                ]
            }

        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.runner = TestCaseRunner(
            client=FastAPITestClient(app=self.app),
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )

    def test_get_status__200(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_get_status__200'
        )
        self.verify_test_result(result=result)

    def test_get_protected__200(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_get_protected__200'
        )
        self.verify_test_result(result=result)

    def test_get_protected__401(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_get_protected__401'
        )
        self.verify_test_result(result=result)

    def test_get_google__301(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_get_google__301'
        )
        self.verify_test_result(result=result)

    def test_get_items__200_empty(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_get_items__200_empty'
        )
        self.verify_test_result(result=result)

    def test_get_items__200_one_item(self) -> None:
        self.items[1] = 'item1'
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_get_items__200_one_item'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_get_items__200_with_custom_verifier(self) -> None:
        self.items[1] = 'item1'
        self.items[2] = 'item2'
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_get_items__200_with_custom_verifier',
            )
            self.verify_test_result(result=result, verifier=self.custom_verifier)
        finally:
            self.items.clear()

    def test_create_item__200(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_create_item__200'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_with_external_files(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_create_item__200_with_external_files'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_with_test_data_modifier(self) -> None:
        def modifier(test_data: TestData) -> TestData:
            test_data.request_data = ujson.dumps({'name': 'blah'})
            return test_data

        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_create_item__200_with_test_data_modifier',
                test_data_modifier=modifier
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_no_name(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_create_item__200_no_name'
            )
            result.test_data = self._modify_expected_response(
                test_data=result.test_data,
                id=max(self.items.keys()),
                name=result.response.json['name']
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_template_vars(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_create_item__200_template_vars',
                request_json_modifiers={
                    'name': 'alex'
                },
                response_json_modifiers={
                    'id': 1,
                    'name': 'alex'
                }
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_excluded_response_paths(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_create_item__200_excluded_response_paths'
            )
            self.verify_test_result(
                result=result,
                excluded_response_paths=['id']
            )
        finally:
            self.items.clear()

    def test_get_item__200(self) -> None:
        self.items[1] = 'item1'
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_get_item__200'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_get_item__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_get_item__404'
        )
        self.verify_test_result(result=result)

    def test_delete_item__200(self) -> None:
        self.items[1] = 'item1'
        try:
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_delete_item__200',
                url_params={'item_id': 1}
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_delete_item__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_fastapi.json',
            test_name='test_delete_item__404',
            url_params={'item_id': 1}
        )
        self.verify_test_result(result=result)

    def test_update_scenarios_on_fail(self) -> None:
        scenario_file_path = os.path.join(self.runner.path_to_scenarios_dir, 'test_fastapi.json')
        with open(scenario_file_path, 'r') as f:
            original_scenario_file_content = f.read()

        with self.assertRaises(Exception):
            result = self.runner.run(
                path_to_test_cases='test_fastapi.json',
                test_name='test_update_scenarios_on_fail'
            )
            self.verify_test_result(result=result, update_scenarios_on_fail=True)

        try:
            with open(scenario_file_path, 'r') as f:
                scenario_dict = ujson.loads(f.read())
                self.assertDictEqual(
                    scenario_dict['test_get_protected__200'],
                    scenario_dict['test_update_scenarios_on_fail']
                )
        except Exception:
            with open(scenario_file_path, 'w+') as f:
                f.write(original_scenario_file_content)
            raise
        else:
            with open(scenario_file_path, 'w+') as f:
                f.write(original_scenario_file_content)

    def custom_verifier(self, result: TestResult) -> None:
        # Only check names
        self.assertListEqual(
            sorted(item['name'] for item in result.test_data.expected_response_json['items']),
            sorted(item['name'] for item in result.response.json['items'])
        )

    @staticmethod
    def _modify_expected_response(test_data: TestData, **kwargs: Dict[str, Any]) -> TestData:
        expected_response_json = test_data.expected_response_json
        expected_response_json.update(**kwargs)
        test_data.expected_response = ujson.dumps(expected_response_json)
        return test_data
