import inspect

from mutils.misc import docstring

from .command import Command
from . import CommandCollection
from .exc import SubcommandError




class Subcommand:
	def __init__(self, parser):
		self.parser = parser
		self.add_subcommand_groups()
		self._subcommands = 0


	def add_subcommand_groups(self):
		for subcmd_cls in self.__class__.__subclasses__():
			self.add_subcommands(subcmd_cls)


	def add_subcommands(self, subcmd_cls):

		command_collection = CommandCollection()
		subcmd_parser = None

		for member_name, member_val in inspect.getmembers(subcmd_cls, predicate=\
		lambda x : inspect.ismethod(x) or inspect.isfunction(x)):

			if True or inspect.ismethod(member_val):
				func = member_val
				if getattr(func, 'subcmd', None) is not None:
					if not func.__name__ in subcmd_cls.__dict__.keys():
						continue

				
					subcmd_parser = command_collection.add_subcommand(
								func,
								cmd_class=subcmd_cls,
								parent=self.parser,
								group_name=self.__class__.__name__,
								parser=subcmd_parser)

					subcmd = subcmd_cls(subcmd_parser)
					self._subcommands += 1


	def subcommands_added(self):
		return self._subcommands > 0

