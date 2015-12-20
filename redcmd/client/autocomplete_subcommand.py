
from .. import Subcommand, subcmd, CommandError
from ..compgen import CompGen, CompGenError


class AutoCompleteSubcommand(Subcommand):

	@subcmd
	def autocomplete(self):
		'Do various autocomplete actions.'
		pass


class AutoCompleteSubSubcommands(AutoCompleteSubcommand):

	@subcmd
	def install(self, command_name):
		'''Install autocomplete for a command.
		command_name: command name'''

		pass


	@subcmd
	def uninstall(self, command_name):
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

		pass

