import unittest
import timevis
import os.path
import json


# The folder holding the test data
test_path = os.path.dirname(__file__)


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.app = timevis.app.test_client()
        self.url = '/api/v2/experiment'

    def test_post(self):
        with open(test_path + '/post_exp.json') as file:
            obj = json.load(file)
            resp = self.app.post(self.url, data=json.dumps(obj),
                                 content_type='application/json')
        self.assertIsNotNone(resp.data)


if __name__ == '__main__':
    unittest.main()
