from restmon.api import app
import unittest

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the response data
        self.assertEqual(result.data, '{"Hello": "World"}\n')

    def test_cpu_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/cpu')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cpu_percent_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/cpupercent')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_memory_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/memory')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_storage_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/storage')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_platform_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/platform')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)