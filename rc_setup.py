from importlib import import_module
import sys


def setup_autocomp(commands_module, command_name, _to_hyphen=False):
	args = sys.argv

	if len(args) > 1 and args[1] == 'install':
		rc_api = None
		try:
			rc_api = import_module('redcmd.api')
		except ImportError as e:
			print('cannot setup autocomplete for %s'%command_name)
			return
		
		success = rc_api.setup_autocomp(commands_module, command_name, _to_hyphen=_to_hyphen)
		if success:
			print('autocomplete setup for %s'%command_name)


def remove_base():
	args = sys.argv

	if len(args) > 1 and args[1] == 'install':
		rc_api = None
		try:
			rc_api = import_module('redcmd.api')
		except ImportError as e:
			return
		
		rc_api.remove_base()

