#!/usr/bin/env python
# -*- coding: utf-8 -*-

# general requirements
import unittest
import server_control

# For the server in this case
import http.server
import socketserver

# For the tests
import requests


ADDRESS = 'localhost'
PORT = 8000


class SetupTest(unittest.TestCase):

    server = None

    def setUp(self):
        # Create an arbitrary subclass of TCP Server as the server to be started
        # Here, it is an Simple HTTP file serving server
        Handler = http.server.SimpleHTTPRequestHandler

        self.server_control = server_control.Server(socketserver.TCPServer((ADDRESS, PORT), Handler))
        # Start test server before running any tests
        self.server_control.start_server()

    def test_request(self):
        # Simple example server test
        r = requests.get('http://{}:{}/index.html'.format(ADDRESS, PORT), timeout=10)
        self.assertEqual(r.status_code, 200)

    def tearDown(self):
        # possible but not necessary
        # self.server_control.stop_server()
        pass


if __name__ == "__main__":
    unittest.main()
