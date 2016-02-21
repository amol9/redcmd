from importlib import import_module
import sys

from . import const
from .commandline import CommandLine
from .exc import CommandLineError
from .autocomp.installer import Installer, InstallError


__all__ = ['setup_autocomp', 'remove_autocomp', 'commandline_execute', 'remove_base']


def setup_autocomp(commands_module, command_name=None, _to_hyphen=False):
	success = False
	print('installing redcmd autocomplete support...')
	try:
		import_module(commands_module)
	except ImportError as e:
		print(e)
		return

	try:
		installer = Installer()
		installer.setup_cmd(command_name, _to_hyphen=_to_hyphen)
		success = True
	except InstallError as e:
		print(e)

	return success


def remove_autocomp(command_name):
	installer = Installer()	
	installer.remove_cmd(command_name)


def commandline_execute(**kwargs):
	cl = CommandLine(**kwargs)
	try:
		cl.execute()
	except CommandLineError:
		sys.exit(const.commandline_exc_exit_code)

	sys.exit(0)


def remove_base():
	print('removing redcmd autocomplete support...')
	try:
		installer = Installer()
		installer.remove_base()
	except InstallError as e:
		print(e)

