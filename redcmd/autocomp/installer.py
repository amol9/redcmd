from os.path import exists, join as joinpath
from os import makedirs, remove

from .. import const
from ..command_collection import CommandCollection, CommandCollectionError
from .shell_script_installer_factory import get_shell_script_installer


class InstallError(Exception):
	pass


class Installer:

	def __init__(self):
		self._shell_script_installer = get_shell_script_installer()


	def setup(self, command_name):
		if not exists(const.autocomp_dir_path):
			makedirs(const.autocomp_dir_path)

		command_collection = CommandCollection()
		command_collection.make_option_tree()
		

	#add confirmation prompt
	def remove(self, command_name):
		if not exists(const.autocomp_dir_path):
			raise InstallError('autocomplete data dir not found: %s'%const.autocomp_dir_path)

		filepath = joinpath(const.autocomp_dir_path, command_name)

		if not exists(filepath):
			raise InstallError('no command named %s is setup for autocomplete'%command_name)

		try:
			remove(filepath)
		except OSError as e:
			print(e)
			raise InstallError('unable to remove autocomplete data for %s'%command_name)


	def base_installed(self):
		return self._shell_script_installer.base_installed()


	def setup_base(self):
		self._shell_script_installer.setup_base()


	def remove_base(self):
		self._shell_script_installer.remove_base()


	def setup_cmd(self, cmdname):
		self._shell_script_installer.setup_cmd(cmdname)


	def remove_cmd(self, cmdname):
		self._shell_script_installer.remove_cmd(cmdname)



