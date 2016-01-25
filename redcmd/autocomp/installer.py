from os.path import exists, join as joinpath
from os import makedirs, remove

from redlib.api.system import sys_command

from .. import const
from ..command_collection import CommandCollection, CommandCollectionError
from .shell_script_installer_factory import get_shell_script_installer
from ..datastore import DataStore, DataStoreError
from ..client.redcmd_internal_subcommand import RedcmdInternalSubcommand


class InstallError(Exception):
	pass


class Installer:

	def __init__(self):
		self._shell_script_installer = get_shell_script_installer()


	def setup_base(self):
		self._shell_script_installer.setup_base()


	def remove_base(self):
		self._shell_script_installer.remove_base()


	def setup_cmd_by_exe(self, cmdname, _to_hyphen=False):
		if cmdname == const.internal_dummy_cmdname:
			cmdname = CommandCollection().prog
			self.setup_cmd(cmdname, _to_hyphen=_to_hyphen)
		else:
			cmd = cmdname + ' ' + const.internal_subcmd + ' autocomp setup ' + const.internal_dummy_cmdname
			rc, op = sys_command(cmd)
			print(op)
			if rc != 0:
				raise InstallError(op)


	def setup_cmd(self, cmdname, _to_hyphen=False):
		try:
			command_collection = CommandCollection()
			command_collection.set_details(prog=cmdname, _to_hyphen=_to_hyphen)

			subcmd_cls = RedcmdInternalSubcommand if cmdname == 'redcmd' else None
			command_collection.make_option_tree(subcmd_cls=subcmd_cls, command_name=cmdname)
		except CommandCollectionError as e:
			raise InstallError(e)

		try:
			self._shell_script_installer.setup_cmd(cmdname)
		except ShellScriptInstallError as e:
			raise InstallError(e)


	def remove_cmd(self, cmdname):
		dstore = DataStore()

		try:
			dstore.remove_optiontree(cmdname, exc=True)
		except DataStoreError as e:
			if e.reason == DataStoreError.FILE_NOT_FOUND:
				raise InstallError('%s is not setup for current user'%cmdname)
			else:
				raise InstallError(e)
			

		self._shell_script_installer.remove_cmd(cmdname)


	def remove_all(self):
		dstore = DataStore()
		dstore.remove_all_optiontrees()

