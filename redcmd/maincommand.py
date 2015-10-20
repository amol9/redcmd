import inspect

from . import CommandCollection
from .exc import MainCommandError


class Maincommand:
	def __init__(self):
		self.add_maincommand()
		self._maincommand_added = False


	def add_maincommand(self):
		subclasses = self.__class__.__subclasses__()

		if len(subclasses) > 1:
			raise MainCommandError('only one class should derive from MainCommand')
		elif len(subclasses) == 0:
			return

		maincmd_cls = subclasses[0]

		command_collection = CommandCollection()

		for member_name, member_val in inspect.getmembers(subcmd_cls, predicate=\
		lambda x : inspect.ismethod(x) or inspect.isfunction(x)):

			func = member_val
			if getattr(func, 'maincmd', None) is not None:
				if self._maincommand_added:
					raise MainCommandError('only one method in MainCommand derived class can be decorated @maincmd')
			
				command_collection.add_maincommand(func, cmd_class=maincmd_cls)
				self._maincommand_added = True

