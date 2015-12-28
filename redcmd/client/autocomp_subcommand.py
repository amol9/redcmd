
from .. import subcmd, CommandError
from ..autocomp.generator import Generator, GeneratorError
from ..autocomp.installer import Installer
from .redcmd_internal_subcommand import RedcmdInternalSubcommand


class AutocompSubcommand(RedcmdInternalSubcommand):

	@subcmd
	def autocomp(self):
		'Do various autocomplete actions.'
		pass


class AutocompSubSubcommands(AutocompSubcommand):

	@subcmd
	def setup(self, command_name):
		'''Install autocomplete for a command.
		command_name: command name'''

		pass


	@subcmd
	def remove(self, command_name, confirm=True):
		'''Uninstall autocomplete for a command.
		command_name: command name'''

		pass


	@subcmd
	def gen(self, command_line, word):
		'''Generate autocomplete options for a command.
		command_line: command line so far
		word: word to be auto-completed'''

		try:
			compgen = CompGen(command_line, word)
			compgen.gen()
		except CompGenError as e:
			print(e)
			raise CommandError()


	@subcmd
	def list(self):
		'List the commands registered for autocomplete.'

		print('no list yet')

