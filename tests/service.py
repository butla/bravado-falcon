import json
import falcon


class ServiceResource(object):
    def on_put(self, req, resp, id):
        req_json = json.loads(req.stream.read().decode())

        req_json['id'] = id
        req_json['state'] = 'submitted'

        resp.body = json.dumps(req_json)
        resp.status = falcon.HTTP_ACCEPTED


api = falcon.API()
api.add_route('/v1/operation/{id}', ServiceResource())