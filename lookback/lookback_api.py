import json

import requests
from requests import exceptions


class LookbackApi(object):
    """
    This class is the client wrapper for Rally's Lookback API that can be used to run queries against the
    API and receive native Python objects in response.

    If you wanted to grab the schedule state and plan estimate for all stories, you can do something like::

        from lookback.lookback_api import LookbackApi

        client = LookbackApi("my_rally_username", "my_rally_password", "my_rally_workspace")
        response = client.query({
            "Project": 279050021
        }, ("ScheduleState", "PlanEstimate"))

    A query run with `LookbackApi` returns a `LookbackResponse` object. The response object contains a list of
    `LookbackSnapshot` objects.
    """
    username = ''
    password = ''
    api_url = ''

    def __init__(self, username, password, workspace):
        self.username = username
        self.password = password
        self.api_url = self.build_url(workspace)

    def query(self, find, fields):
        request_data = {
            'find': json.dumps(find),
            'fields': json.dumps(fields)
        }
        request_data.update({
            'limit': 20000
        })
        resp = requests.get(self.api_url, auth=(self.username, self.password),
            params=request_data)
        return self.handle_response_content(resp)

    def handle_response_content(self, resp):
        if self.is_auth_response(resp):
            raise exceptions.HTTPError("Authentication required")
        content = resp.json()
        if not resp.ok:
            raise exceptions.HTTPError(content['Errors'][0])
        return LookbackResponse(content)

    def build_url(self, workspace):
        return 'https://rally1.rallydev.com/analytics/v2.0/service/rally/workspace/' \
            '%s/artifact/snapshot/query.js' % workspace

    def is_auth_response(self, resp):
        return resp.status_code == 401 and 'www-authenticate' in resp.headers


class LookbackObject(object):
    raw_content = {}

    def get_class_name(self):
        return self.__class__.__name__

    def __getattr__(self, name):
        if name in self.raw_content:
            return self.raw_content[name]
        raise AttributeError('%s does not contain the %s attribute' % (self.get_class_name(), name))

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __dir__(self):
        return self.raw_content.keys()


class LookbackResponse(LookbackObject):
    snapshots = []

    def __init__(self, response):
        self.raw_content = response
        self.build_snapshots()

    def build_snapshots(self):
        results = self.raw_content['Results']
        self.snapshots = [Snapshot(snapshot_data) for snapshot_data in results]

    def __dir__(self):
        attrs = super(LookbackResponse, self).__dir__()
        attrs.append('snapshots')
        return attrs


class Snapshot(LookbackObject):
    def __init__(self, snapshot):
        self.raw_content = snapshot

    def __iter__(self):
        return self.raw_content.itervalues()
