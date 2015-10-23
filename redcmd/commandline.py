import sys

from .exc import CommandError, CommandCollectionError
from .command_collection import CommandCollection


class CommandLine(object):
	'Command line handler.'

	def __init__(self, prog='program', description='A command line utility.', version='0.0.0', default_subcommand=None):
		self.commandcollection = CommandCollection()
		self.commandcollection.set_details(prog=prog, description=description, version=version)

		self.default_subcommand = default_subcommand

		try:
			self.commandcollection.add_commands()
		except CommandCollectionError as e:
			raise CommandLineError('error creating command line structure')

	
	def execute(self):
		if self.default_subcommand is not None and len(sys.argv) == 1 :
			sys.argv.append(self.default_subcommand)
	
		try:
			self.commandcollection.execute()
		except CommandError as e:
			print(e)
			sys.exit(1)

		sys.exit(0)


	def set_default_subcommand(self, name):
		self.default_subcommand = name

