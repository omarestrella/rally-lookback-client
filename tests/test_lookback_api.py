import unittest

from lookback.lookback_api import LookbackApi


class TestLookbackApi(unittest.TestCase):
    client = None

    @classmethod
    def setup_class(cls):
        cls.client = LookbackApi(username="", password="", workspace="")
        cls.default_find = {
            "Project": 279050021,
            "_ValidFrom": {
                "$gte": "2013-01-01T00:00:00.000Z",
                "$lte": "2013-02-01T00:00:00.000Z"
            }
        }
        cls.default_fields = ["ObjectID", "ScheduleState", "PlanEstimate"]

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_access_to_fields_possible_as_dictionary(self):
        pass

    def test_access_to_requested_fields_in_a_snapshot(self):
        response = self.client.query(find=self.default_find, fields=self.default_fields)
        snapshot = response.snapshots[0]
        self.assertItemsEqual(snapshot.raw_content.keys(), self.default_fields)