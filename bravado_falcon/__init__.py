"""
Classes necessary for doing Falcon unit tests through Bravado.
"""

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import bravado.http_client
import bravado.http_future
import bravado_core.response
from pytest_falcon.plugin import Client


class FalconHttpClient(bravado.http_client.HttpClient):
    """Bravado HTTP client implementation that can be used in Falcon unit tests.
    It doesn't actually call anything through HTTP, it just simulates those calls.

    Args:
        api (`falcon.API`): API object to send the requests to.
    """

    def __init__(self, falcon_api):
        self._api = falcon_api

    def request(self, request_params, operation=None, response_callbacks=None,
                also_return_response=False):
        """Taken from `bravado.http_client.HttpClient`.

        Args:
            request_params (dict): complete request data. e.g. url, method, headers, body, params,
                connect_timeout, timeout, etc.
            operation (`bravado_core.operation.Operation`): operation that this http request
                is for. Defaults to None - in which case, we're obviously just retrieving a Swagger
                Spec.
            response_callbacks: List of callables to post-process the incoming response.
                Expects args incoming_response and operation.
            also_return_response: Consult the constructor documentation for
                `bravado.http_future.HttpFuture`.

        Returns:
            `bravado_core.http_future.HttpFuture`: HTTP Future object
        """
        falcon_test_future = FalconTestFutureAdapter(request_params, self._api)

        return bravado.http_future.HttpFuture(
            falcon_test_future,
            FalconTestResponseAdapter,
            operation,
            response_callbacks,
            also_return_response)


class FalconTestFutureAdapter:
    """Mimics a :class:`concurrent.futures.Future` for the purposes of making it work with
    Bravado's :class:`bravado.http_future.HttpFuture` when simulating calls to a Falcon API.
    Those calls will be validated by Bravado.

    Args:
        request_params (dict): Request parameters provided to
            :class:`bravado.http_client.HttpClient` interface.
        falcon_api (`falcon.API`): API object to send the request to.
        response_encoding (str): Encoding that will be used to decode response's body.
            If set to None then the body won't be decoded.
    """

    def __init__(self, request_params, falcon_api, response_encoding='utf-8'):
        self._falcon_api = falcon_api
        self._request_params = request_params
        self._response_encoding = response_encoding
        self._client = Client(falcon_api)


    def result(self, **_):
        """
        Args:
            **_: Ignore all the keyword arguments (right now it's just timeout) passed by Bravado.
        """
        # Bravado will create the URL by appending request path to 'http://localhost'
        path = self._request_params['url'].replace('http://localhost', '')
        query_string = urlencode(self._request_params.get('params', {}))
        return self._client.fake_request(path=path,
                                         query_string=query_string,
                                         headers=self._request_params.get('headers'),
                                         body=self._request_params.get('data'),
                                         method=self._request_params.get('method'))


class FalconTestResponseAdapter(bravado_core.response.IncomingResponse):
    """Wraps a response from Falcon test client to provide a uniform interface
    expected by Bravado's :class:`bravado.http_future.HttpFuture`.

    Args:
        falcon_test_response: Response to a call simulated with `pytest_falcon`.
    """

    def __init__(self, falcon_test_response):
        self._response = falcon_test_response

    @property
    def status_code(self):
        """
        Returns:
            int: HTTP status code
        """
        return self._response.status_code

    @property
    def text(self):
        """
        Returns:
            str: Textual representation of the response's body.
        """
        return self._response.body

    @property
    def reason(self):
        """
        Returns:
            str: Reason-phrase of the HTTP response (e.g. "OK", or "Not Found")
        """
        # status codes from Falcon look like this: "200 OK"
        return self._response.status[4:]

    @property
    def headers(self):
        """
        Returns:
            dict: Headers attached to the response.
        """
        return self._response.headers

    def json(self, **kwargs):
        """
        Args:
            **kwargs: This is a part of the interface, but we don't do anything with it.

        Returns:
            dict: JSON representation of the response's body.
        """
        return self._response.json
