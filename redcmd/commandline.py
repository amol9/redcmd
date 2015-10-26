import sys

from .exc import CommandError, CommandCollectionError
from .command_collection import CommandCollection
import const


class CommandLine(object):
	'Command line handler.'

	def __init__(self, prog=const.prog, description=const.description, version=const.version, default_subcommand=None):
		self._command_collection = CommandCollection()
		self._command_collection.set_details(prog=prog, description=description, version=version)

		self._default_subcommand = default_subcommand

		try:
			self._command_collection.add_commands()
		except CommandCollectionError as e:
			raise CommandLineError('error creating command line structure')

	
	def execute(self):
		if self._default_subcommand is not None and len(sys.argv) == 1 :
			sys.argv.append(self._default_subcommand)
	
		try:
			self._command_collection.execute()
		except CommandError as e:
			print(e)
			sys.exit(1)

		sys.exit(0)


	def set_default_subcommand(self, name):
		self._default_subcommand = name

