import sys

from . import const
from .client.autocomp_subcommand import *
from .command_collection import CommandCollection
from .autocomp.installer import Installer, InstallError
from .exc import CommandCollectionError, CommandLineError
from .client.redcmd_internal_subcommand import RedcmdInternalSubcommand


__all__ = ['CommandLine']


class CommandLine(object):
	'Command line handler.'

	def __init__(self, prog=const.prog, description=const.description, version=const.version, 
			default_subcommand=None, namespace=None, _to_hyphen=False):

		self._command_collection = CommandCollection()
		self._command_collection.set_details(prog=prog, description=description, version=version, _to_hyphen=_to_hyphen)

		self._default_subcommand = default_subcommand
		self._namespace = namespace
		self._prog = prog

	
	def execute(self, args=None, namespace=None):
		if len(sys.argv) > 1 and sys.argv[1] == const.internal_subcmd:
			self.execute_internal(args, namespace)
			return

		try:
			subcmd_cls = None
			if sys.argv[0].endswith('redcmd'):
				subcmd_cls = RedcmdInternalSubcommand

			self._command_collection.add_commands(subcmd_cls=subcmd_cls)
		except CommandCollectionError as e:
			raise CommandLineError('error creating command line structure')

		#import pdb; pdb.set_trace()
		if self._default_subcommand is not None and len(sys.argv) == 1 :
			sys.argv.append(self._default_subcommand)

		if namespace is None:
			namespace = self._namespace
	
		try:
			self._command_collection.execute(args, namespace)
		except CommandCollectionError as e:
			raise CommandLineError(e)


	def execute_internal(self, args=None, namespace=None):
		try:
			self._command_collection.add_internal_commands()
		except CommandCollectionError as e:
			raise CommandLineError('error creating internal command line structure')

		try:
			self._command_collection.execute(args, namespace, internal=True)
		except CommandCollectionError as e:
			raise CommandLineError(e)


	def set_default_subcommand(self, name):
		self._default_subcommand = name


	'''def setup_autocomplete(self, command_name=None):
		installer = Installer()
		command_name = command_name if command_name is not None else self._prog

		try:
			installer.setup_cmd(command_name)
		except InstallError as e:
			print(e)


	def remove_autocomplete(self, command_name=None):
		installer = Installer()

		if command_name is None:
			command_name = self._prog

		try:
			installer.remove_cmd(command_name)
		except InstallError as e:
			print(e)'''

