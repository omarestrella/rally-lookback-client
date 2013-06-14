import os
import unittest

from lookback.lookback_api import LookbackApi

username = os.environ.get('RALLY_USERNAME', '')
password = os.environ.get('RALLY_PASSWORD', '')
workspace = os.environ.get('RALLY_WORKSPACE', '')


class TestLookbackApi(unittest.TestCase):
    client = None

    @classmethod
    def setup_class(cls):
        cls.client = LookbackApi(username=username, password=password, workspace=workspace)
        cls.default_find = {
            'Project': 279050021,
            '_ValidFrom': {
                '$gte': '2013-01-01T00:00:00.000Z',
                '$lte': '2013-02-01T00:00:00.000Z'
            }
        }
        cls.default_fields = ['ObjectID', 'ScheduleState', 'PlanEstimate']
        cls.default_response = cls.client.query(find=cls.default_find, fields=cls.default_fields)

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_access_to_fields_possible_as_attributes(self):
        snapshot = self.default_response.snapshots[0]
        self.assertEqual(snapshot.raw_content['ObjectID'], snapshot.ObjectID)
        self.assertEqual(snapshot.raw_content['ScheduleState'], snapshot.ScheduleState)
        self.assertEqual(snapshot.raw_content['PlanEstimate'], snapshot.PlanEstimate)

    def test_access_to_fields_possible_as_dictionary(self):
        snapshot = self.default_response.snapshots[0]
        for field in self.default_fields:
            self.assertEqual(snapshot.raw_content[field], snapshot[field])

    def test_access_to_requested_fields_in_a_snapshot(self):
        snapshot = self.default_response.snapshots[0]
        self.assertItemsEqual(snapshot.raw_content.keys(), self.default_fields)
