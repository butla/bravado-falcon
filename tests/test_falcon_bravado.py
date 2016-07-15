try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
import os

from bravado.client import SwaggerClient
import pytest
import yaml

from bravado_falcon import FalconTestHttpClient
import tests.service


@pytest.fixture
def api():
    return tests.service.get_app()


@pytest.fixture
def swagger_spec():
    spec_file_path = os.path.join(os.path.dirname(__file__), 'api_spec.yaml')
    with open(spec_file_path) as spec_file:
        return yaml.load(spec_file)


def test_request_with_swagger(api, swagger_spec):
    id = 'some-id'
    client = SwaggerClient.from_spec(swagger_spec,
                                     http_client=FalconTestHttpClient(api))
    OperationRequest = client.get_model('OperationRequest')
    request_body = OperationRequest(name='some_name', repeats=3)

    resp_object = client.v1.submitOperation(body=request_body, id=id).result()

    assert resp_object.id == id
    assert resp_object.state == 'submitted'
