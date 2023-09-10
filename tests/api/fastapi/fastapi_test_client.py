import httpx
from typing import Union, Any, Dict
from fastapi import FastAPI, testclient

from rest_api_tester.client.base_client import BaseTestClient
from rest_api_tester.client.response_data import ResponseData


class FastAPITestClient(BaseTestClient):

    def __init__(self, app: FastAPI):
        self.fastapi_test_client = testclient.TestClient(app)

    def get(
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> ResponseData:
        response = self.fastapi_test_client.get(
            url=url,
            timeout=timeout,
            follow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
        return self._extract_response_data(response=response)

    def post(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> ResponseData:
        response = self.fastapi_test_client.post(
            url=url,
            content=data,
            timeout=timeout,
            follow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
        return self._extract_response_data(response=response)

    def put(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> ResponseData:
        response = self.fastapi_test_client.put(
            url=url,
            content=data,
            timeout=timeout,
            follow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
        return self._extract_response_data(response=response)

    def patch(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> ResponseData:
        response = self.fastapi_test_client.patch(
            url=url,
            content=data,
            timeout=timeout,
            follow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
        return self._extract_response_data(response=response)

    def delete(
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> ResponseData:
        response = self.fastapi_test_client.delete(
            url=url,
            timeout=timeout,
            follow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
        return self._extract_response_data(response=response)

    @staticmethod
    def _extract_response_data(response: httpx.Response) -> ResponseData:
        return ResponseData(
            text=response.text,
            headers={key.lower(): value for key, value in response.headers.items()},
            status_code=response.status_code
        )
