from os.path import exists, join as joinpath
from os import makedirs, remove

from redlib.api.system import sys_command

from .. import const
from ..command_collection import CommandCollection, CommandCollectionError
from .shell_script_installer_factory import get_shell_script_installer
from ..datastore import DataStore


class InstallError(Exception):
	pass


class Installer:

	def __init__(self):
		self._shell_script_installer = get_shell_script_installer()


	def setup_base(self):
		self._shell_script_installer.setup_base()


	def remove_base(self):
		self._shell_script_installer.remove_base()


	def setup_cmd(self, cmdname):
		if cmdname == const.internal_dummy_cmdname:
			command_collection = CommandCollection()
			cmdname = command_collection.prog

			try:
				command_collection.make_option_tree()
			except CommandCollectionError as e:
				raise InstallError(e)

			try:
				self._shell_script_installer.setup_cmd(cmdname)
			except ShellScriptInstallError as e:
				raise InstallError(e)
		else:
			cmd = cmdname + ' ' + const.internal_subcmd + ' autocomp setup ' + const.internal_dummy_cmdname
			print(cmd)
			rc, op = sys_command(cmd)
			print(op)
			if rc != 0:
				raise InstallError(op)


	def remove_cmd(self, cmdname):
		dstore = DataStore()
		dstore.remove_optiontree(cmdname)

		self._shell_script_installer.remove_cmd(cmdname)


	def remove_all(self):
		dstore = DataStore()
		dstore.remove_all_optiontrees()

