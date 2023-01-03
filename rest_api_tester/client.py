import os
import requests
from typing import Any, Union, Dict


class BaseTestClient:

    __test__ = False

    def get(
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        raise NotImplementedError

    def post(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        raise NotImplementedError

    def put(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        raise NotImplementedError

    def patch(
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        raise NotImplementedError

    def delete(
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        raise NotImplementedError


class TestClient(BaseTestClient):

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> requests.Response:
        url = os.path.join(self.base_url, url)
        return requests.get(
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
        url = os.path.join(self.base_url, url)
        return requests.post(
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
        url = os.path.join(self.base_url, url)
        return requests.put(
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
        url = os.path.join(self.base_url, url)
        return requests.patch(
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
        url = os.path.join(self.base_url, url)
        return requests.delete(
            url=url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
