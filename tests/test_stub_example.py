from flask_restful import Resource
import unittest

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        hello_world = HelloWorld()
        response = hello_world.get()
        self.assertEqual(response, {'hello': 'world'})

if __name__ == '__main__':
    unittest.main()