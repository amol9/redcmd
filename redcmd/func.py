from importlib import import_module

from .autocomp.installer import Installer
from . import const


__all__ = ['setup_redcmd_autocomp']


def setup_redcmd_autocomp(commands_module, command_name=None):
	if setup:
		try:
			import_module(commands_module)
		except ImportError as e:
			print(e)

		installer = Installer()	
		installer.setup_cmd(const.internal_dummy_cmdname)

	else:
		installer = Installer()	
		installer.remove_cmd(command_name)

