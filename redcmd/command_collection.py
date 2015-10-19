
from .mutils.misc import Singleton
from .command_help_formatter import CommandHelpFormatter
from .commandparser import CommandParser


class CommandCollectionError(Exception):
	pass


class _CommandCollection:
	def __init__(self, prog=None, description=None, version=None):
		self.argparser = CommandParser(prog=prog, description=description, formatter_class=CommandHelpFormatter)
		self.argparser.add_argument('-v', '--version', action='version', version=version, help='print program version')


	def add_commands(self):

	def add_subcommand(self, func, parent=None):
		pass


	def add_maincommand(self, func):
		pass


class CommandCollection(Singleton):
	classtype = _CommandCollection

