from importlib import import_module

from .autocomp.installer import Installer
from . import const


__all__ = ['setup_autocomp', 'remove_autocomp']


def setup_autocomp(commands_module, command_name=None, _to_hyphen=False):
	try:
		import_module(commands_module)
	except ImportError as e:
		print(e)
		return

	installer = Installer()	
	installer.setup_cmd(command_name, _to_hyphen=_to_hyphen)


def remove_autocomp(command_name):
	installer = Installer()	
	installer.remove_cmd(command_name)

