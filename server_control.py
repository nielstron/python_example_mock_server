#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import signal


class Server:

    def __init__(self, server):
        """
        Expects subclass of TCPServer as argument
        """
        self._server = server
        self._server_started_event = threading.Event()
        # make totally, really, absolutely sure we close our socket on interrupt (as python doesn't)
        signal.signal(signal.SIGTERM, self._cleanup_server)
        signal.signal(signal.SIGINT, self._cleanup_server)

    def _run_server(self):

        print("Server started")

        # notify about start
        self._server_started_event.set()

        try:
            self._server.serve_forever()
        finally:
            self._cleanup_server()

    def _cleanup_server(self):
        self._server.server_close()
        # Here, server was stopped
        print("Server stopped")

    def stop_server(self):
        """
        Close server forcibly
        :return:
        """
        print("Stopping server")
        self._server.shutdown()

    def start_server(self, timeout=10):
        """
        Start server thread as daemon
        As such the program will automatically close the thread on exit of all non-daemon threads
        :return:
        """
        self._server_started_event.clear()
        # start webserver as daemon => will automatically be closed when non-daemon threads are closed
        t = threading.Thread(target=self._run_server, daemon=True)
        # Start webserver
        t.start()
        # wait (non-busy) for successful start
        self._server_started_event.wait(timeout=timeout)
