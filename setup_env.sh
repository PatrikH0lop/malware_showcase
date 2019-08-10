#!/bin/sh
# This script automates the creation of Python virtual environment.

if [ -d "virtualenv" ]; then
    echo "Virtual environment 'virtualenv' found, activating it."
else
    echo "Virtual environment not found, creating new 'virtualenv'."
    python3 -m venv virtualenv
    if [ $? -eq 0 ]; then
        echo "Virtual environment was successfully created."
    else
        echo "Virtual environment was NOT created, aborting."
        exit 1
    fi
fi

source virtualenv/bin/activate
if [ $? -eq 0 ]; then
    echo "Virtual environment is successfully activated."
else
    echo "Virtual environment was NOT activated, aborting."
    exit 1
fi

echo "Installing required packages."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "All requirements were successfully installed."
else
    echo "Requirements were NOT installed properly, aborting."
    exit 1
fi

echo "Done."
