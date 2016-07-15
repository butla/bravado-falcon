bravado-falcon
==============

.. image:: https://snap-ci.com/butla/bravado-falcon/branch/master/build_image
    :target: https://snap-ci.com/butla/bravado-falcon/branch/master
.. image:: https://coveralls.io/repos/butla/bravado-falcon/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/butla/bravado-falcon?branch=master
.. image:: https://requires.io/github/butla/bravado-falcon/requirements.svg?branch=master
    :target: https://requires.io/github/butla/bravado-falcon/requirements/?branch=master

Integration of Falcon API unit tests with Bravado. For testing your application's contract.

You can easily implement Bravado integrations for other frameworks' unit tests (e.g. Flask's) based
on this code.

This library doesn't do much, but it's actually feature-complete (there weren't that many features
to implement...).

One thing that can be changed in the future is the way Falcon requests are simulated.
Right now it's done with `pytest-falcon <https://github.com/yohanboniface/pytest-falcon>`_, but you
don't have to use Pytest in your tests (but it's great and you probably should at least check
it out).

Usage
-----

.. code-block:: python

    from bravado.client import SwaggerClient
    from bravado_falcon import FalconHttpClient

    api = get_falcon_api() # get a falcon.API
    swagger_spec = get_swagger_spec() # dict created by loading a YAML or JSON from a file

    client = SwaggerClient.from_spec(swagger_spec,
                                     http_client=FalconHttpClient(api))

    # "v1" is the first part of a path (e.g. "/v1/shopping/lists")
    # "getList" is the "operationId" element for an endpoint from Swagger
    # "id" is a path parameter (let's say from "/v1/shopping/lists/{id}")
    # See Bravado docs for more information.
    list_object = client.v1.getList(id='list-id').result()

    # now make assertions about the returned object
