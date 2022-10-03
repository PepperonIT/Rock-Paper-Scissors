#!/bin/bash

# Install Python SDK for pepper
wget -P ~/Downloads https://community-static.aldebaran.com/resources/2.5.10/Python%20SDK/pynaoqi-python2.7-2.5.7.1-linux64.tar.gz
mkdir -p ~/lib/python2/
tar -xf ~/Downloads/pynaoqi-python2.7-2.5.7.1-linux64.tar.gz -C ~/lib/python2
echo "export PYTHONPATH=${PYTHONPATH}:/root/lib/python2/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages" >> ~/.bashrc

# Install project dependencies
pipenv install --dev

echo "Finished installing dev tools"
