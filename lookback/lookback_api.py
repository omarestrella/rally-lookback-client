import json

import requests
from requests import exceptions


class LookbackApi(object):
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
            raise exceptions.RequestException("Authentication required")
        content = resp.json()
        if not resp.ok:
            raise exceptions.RequestException(content['Errors'][0])
        return LookbackResponse(content)

    def build_url(self, workspace):
        return 'https://rally1.rallydev.com/analytics/v2.0/service/rally/workspace/' \
            '%s/artifact/snapshot/query.js' % workspace

    def is_auth_response(self, resp):
        return resp.status_code == 401 and 'www-authenticate' in resp.headers


class LookbackResponse(object):
    raw_response = {}
    snapshots = []

    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.build_snapshots()

    def build_snapshots(self):
        results = self.raw_response['Results']
        self.snapshots = [Snapshot(snapshot_data) for snapshot_data in results]


class Snapshot(object):
    snapshot_data = {}

    def __init__(self, snapshot):
        self.snapshot_data = snapshot

    def __iter__(self):
        return self.snapshot_data.itervalues()

    def __getattr__(self, name):
        if name in self.snapshot_data:
            return self.snapshot_data[name]
        raise AttributeError('Snapshot does not contain the %s attribute' % name)

    def __getitem__(self, key):
        return self.__getattr__(key)
