import requests
from typing import Union, Dict, Any
from fastapi import FastAPI, testclient

from rest_api_tester.client import BaseTestClient


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
    ) -> requests.Response:
        return self.fastapi_test_client.get(
            url=url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def post(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        return self.fastapi_test_client.post(
            url=url,
            data=data,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def put(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        return self.fastapi_test_client.put(
            url=url,
            data=data,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def patch(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        return self.fastapi_test_client.patch(
            url=url,
            data=data,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def delete(
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        return self.fastapi_test_client.delete(
            url=url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
