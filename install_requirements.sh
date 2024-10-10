#!/bin/bash

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Update package list
apt-get update

# Install Python 3 and pip
apt-get install -y python3 python3-pip

# Install the keyboard library using pip
pip3 install keyboard

echo "Python 3, pip, and the keyboard library have been installed successfully."