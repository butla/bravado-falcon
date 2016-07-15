try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
import os

from bravado.client import SwaggerClient
from jsonschema.exceptions import ValidationError
import pytest
import yaml

from bravado_falcon import FalconHttpClient
import tests.service


@pytest.fixture
def client(swagger_spec):
    return SwaggerClient.from_spec(swagger_spec,
                                   http_client=FalconHttpClient(tests.service.api),
                                   config={'also_return_response': True})

@pytest.fixture(scope='session')
def swagger_spec():
    spec_file_path = os.path.join(os.path.dirname(__file__), 'api_spec.yaml')
    with open(spec_file_path) as spec_file:
        return yaml.load(spec_file)


def test_request_with_swagger(client):
    id = 'some-id'
    OperationRequest = client.get_model('OperationRequest')
    request_body = OperationRequest(name='some_name', repeats=3)

    resp_object, http_response = client.v1.submitOperation(body=request_body, id=id).result()

    assert http_response.reason == 'Accepted'
    assert 'application/json' in http_response.headers['Content-Type']
    assert '"state": "submitted"' in http_response.text
    assert resp_object.id == id
    assert resp_object.state == 'submitted'


def test_bravado_validation_works(client):
    OperationRequest = client.get_model('OperationRequest')
    request_body = OperationRequest(name='this will be missing repeats')

    with pytest.raises(ValidationError):
        client.v1.submitOperation(body=request_body, id='some_id').result()
