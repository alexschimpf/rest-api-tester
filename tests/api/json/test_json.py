import os
import string
import random
import ujson
from typing import Union, Any, Dict, cast
from fastapi import FastAPI, Header
from fastapi.responses import Response, PlainTextResponse, RedirectResponse
from pydantic import BaseModel

from rest_api_tester.test import TestCase, TestData, TestResult
from rest_api_tester.runner import TestCaseRunner

from tests.api.fastapi_test_client import FastAPITestClient


class Item(BaseModel):
    name: Union[str, None]


class TestJSON(TestCase):

    def setUp(self) -> None:
        self.items: Dict[Any, Any] = {}
        self.app = FastAPI()

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

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        self.runner = TestCaseRunner(
            client=FastAPITestClient(app=self.app),
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_get_status__200(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_get_status__200'
        )
        self.verify_test_result(result=result)

    def test_get_protected__200(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_get_protected__200'
        )
        self.verify_test_result(result=result)

    def test_get_protected__401(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_get_protected__401'
        )
        self.verify_test_result(result=result)

    def test_get_google__301(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_get_google__301'
        )
        self.verify_test_result(result=result)

    def test_get_items__200_empty(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_get_items__200_empty'
        )
        self.verify_test_result(result=result)

    def test_get_items__200_one_item(self) -> None:
        self.items[1] = "item1"
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
                test_name='test_get_items__200_one_item'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_get_items__200_with_custom_verifier(self) -> None:
        self.items[1] = "item1"
        self.items[2] = "item2"
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
                test_name='test_get_items__200_with_custom_verifier',
            )
            self.verify_test_result(result=result, verifier=self.custom_verifier)
        finally:
            self.items.clear()

    def test_create_item__200(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
                test_name='test_create_item__200'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_with_external_files(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
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
                path_to_test_cases='test_json.json',
                test_name='test_create_item__200_with_test_data_modifier',
                test_data_modifier=modifier
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_create_item__200_no_name(self) -> None:
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
                test_name='test_create_item__200_no_name'
            )
            result.test_data = self._modify_expected_response(
                test_data=result.test_data,
                id=max(self.items.keys()),
                name=result.response.json()['name']
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_get_item__200(self) -> None:
        self.items[1] = "item1"
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
                test_name='test_get_item__200'
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_get_item__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_get_item__404'
        )
        self.verify_test_result(result=result)

    def test_delete_item__200(self) -> None:
        self.items[1] = "item1"
        try:
            result = self.runner.run(
                path_to_test_cases='test_json.json',
                test_name='test_delete_item__200',
                url_params={'item_id': 1}
            )
            self.verify_test_result(result=result)
        finally:
            self.items.clear()

    def test_delete_item__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_json.json',
            test_name='test_delete_item__404',
            url_params={'item_id': 1}
        )
        self.verify_test_result(result=result)

    def custom_verifier(self, result: TestResult) -> None:
        expected_response = ujson.loads(cast(str, result.test_data.expected_response))
        actual_response = result.response.json()

        # Only check names
        self.assertListEqual(
            list(sorted(item['name'] for item in expected_response['items'])),
            list(sorted(item['name'] for item in actual_response['items'])),
        )

    @staticmethod
    def _modify_expected_response(test_data: TestData, **kwargs: Dict[str, Any]) -> TestData:
        expected_response_dict = ujson.loads(cast(str, test_data.expected_response))
        expected_response_dict.update(**kwargs)
        test_data.expected_response = ujson.dumps(expected_response_dict)
        return test_data
