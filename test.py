#!/usr/bin/env python
# -*- coding: utf-8 -*-

import server

import requests
import unittest

ADDRESS = 'localhost'
PORT = 8000


class SetupTest(unittest.TestCase):

    server = None

    def setUp(self):
        # Start test server before running any tests
        self.server = server.Server(8000)
        self.server.start_server()

    def test_request(self):
        # Simple example server test
        r = requests.get('http://{}:{}/index.html'.format(ADDRESS, PORT))
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
