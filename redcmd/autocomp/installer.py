from os.path import exists, join as joinpath
from os import makedirs, remove

from .. import const
from ..command_collection import CommandCollection, CommandCollectionError


class InstallError(Exception):
	pass


class Installer:

	def __init__(self):
		pass


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
