import unittest
import os
import os.path
import json

# The folder holding the test data
data_path = os.path.dirname(__file__)

# Set the temporal config for testing
os.environ['TIMEVIS_CONFIG'] = os.path.join(data_path, 'config.py')
import timevis


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.app = timevis.app.test_client()
        self.url = '/api/v2/experiment'

    def test_post(self):
        name = os.path.join(data_path, 'post_exp.json')
        with open(name) as file:
            obj = json.load(file)
            resp = self.app.post(self.url, data=json.dumps(obj),
                                 content_type='application/json')
        self.assertIsNotNone(resp.data)

    def test_get(self):
        resp = self.app.get(self.url)
        self.assertIsNotNone(resp.data)

    def test_put(self):
        name = os.path.join(data_path, 'put_exp.json')
        with open(name) as file:
            obj = json.load(file)
            resp = self.app.put(self.url, data=json.dumps(obj),
                                content_type='application/json')
        self.assertIsNotNone(resp.data)

if __name__ == '__main__':
    unittest.main()
