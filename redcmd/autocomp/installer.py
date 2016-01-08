from os.path import exists, join as joinpath
from os import makedirs, remove

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
		command_collection = CommandCollection()
		command_collection.make_option_tree()

		self._shell_script_installer.setup_cmd(cmdname)


	def remove_cmd(self, cmdname):
		dstore = DataStore()
		dstore.remove_optiontree(cmdname)

		self._shell_script_installer.remove_cmd(cmdname)


	def remove_all(self):
		dstore = DataStore()
		dstore.remove_all_optiontrees()

