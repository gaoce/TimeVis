import unittest
import timevis


class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.app = timevis.app.test_client()

    def test_api(self):
        resp = self.app.get('/api/v2/experiment')
        self.assertIsNotNone(resp.data)


if __name__ == '__main__':
    unittest.main()
