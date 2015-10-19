import sys

from .exc import CommandError
from . import CommandCollection


class CommandLine(object):
	'Command line handler.'

	def __init__(self, prog='program', description='A command line utility.', version='0.0.0'):
		self.commandcollection = CommandCollection(prog=prog, description=description, version=version)

		self.default_subcommand = None
		try:
			self.add_commands()
		except CommandCollectionError as e:
			print(e)
			raise CommandLineError()

	
	def execute(self):
		if self.default_subcommand is not None and len(sys.argv) == 1 :
			sys.argv.append(self.default_subcommand)

		args = self.argparser.parse_args()
		try:
			subcmd_func = args.subcmd_func
			subcmd_func.execute(args)
		except CommandError as e:
			sys.exit(1)

		sys.exit(0)


	def set_default_subcommand(self, name):
		self.default_subcommand = name

