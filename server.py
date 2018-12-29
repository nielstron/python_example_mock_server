#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time

import http.server
import socketserver


class Server:

    def __init__(self, port=8000):
        self._port = port
        self._httpd = None
        self._server_started = False
        self._server_started_condition = None

    def _run_server(self):

        Handler = http.server.SimpleHTTPRequestHandler

        self._httpd = socketserver.TCPServer(("", self._port), Handler)
        print("serving at port", self._port)
        with self._server_started_condition:
            self._server_started = True
            # Notify starting thread of successful start
            self._server_started_condition.notify_all()
        self._httpd.serve_forever()
        # Here, server was stopped
        print("Server stopped")

    def stop_server(self):
        """
        Close server forcibly
        :return:
        """
        print("Stopping server")
        self._httpd.shutdown()

    def start_server(self, timeout=10):
        """
        Start server thread as daemon
        As such the program will automatically close the thread on exit of all non-daemon threads
        :return:
        """
        self._httpd = None
        self._server_started = False
        self._server_started_condition = threading.Condition()
        # start webserver as daemon => will automatically be closed when non-daemon threads are closed
        t = threading.Thread(target=self._run_server, daemon=True)
        t.start()
        # Start webserver
        with self._server_started_condition:
            while not self._server_started:
                # wait (non-busy) for successful start
                self._server_started_condition.wait(timeout=timeout)
