
from .. import subcmd, CommandError
from ..autocomp.generator import Generator, GenError
from ..autocomp.installer import Installer, InstallError
from .redcmd_internal_subcommand import RedcmdInternalSubcommand
from ..datastore import DataStore, DataStoreError


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

		self.exc_installer_method(Installer.setup_cmd, command_name)


	@subcmd
	def remove(self, command_name, confirm=True):
		'''Uninstall autocomplete for a command.
		command_name: command name'''

		self.exc_installer_method(Installer.remove_cmd, command_name)


	@subcmd
	def setupbase(self):
		'Install common base scripts for autocomplete.'
		
		self.exc_installer_method(Installer.setup_base)


	@subcmd
	def removebase(self):
		'''Uninstall common base scripts for autocomplete.
		Please note that all the commands setup for autocomplete will also be unregistered.'''

		self.exc_installer_method(Installer.remove_base)


	def exc_installer_method(self, method, *args, **kwargs):
		installer = Installer()
		try:
			method(installer, *args, **kwargs)
		except InstallError as e:
			print(e)
			raise CommandError()


	@subcmd
	def gen(self, command_line, comp_word):
		'''Generate autocomplete options for a command.
		command_line: 	command line so far
		comp_word: 	word to be auto-completed'''

		try:
			g = Generator(command_line, comp_word.strip())
			g.load()
			options = g.gen()

			for option in options:
				print(option)
		except GenError as e:
			print(e)
			raise CommandError()


	@subcmd
	def list(self):
		'List the commands registered for autocomplete.'

		try:
			dstore = DataStore()
			for name in dstore.list_optiontree():
				print(name)
		except DataStoreError as e:
			print(e)
			raise CommandError()
