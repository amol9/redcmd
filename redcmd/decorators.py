import inspect

from .command_collection import CommandCollection
from .exc import CommandCollectionError, MaincommandError, SubcommandError, CommandLineError
from .maincommand import Maincommand
from .subcommand import Subcommand


def subcmd(parent=None):
	def subcmd_dec(func):
		if member_of_a_class(func): 
			func.subcmd = True
			return func

		command_collection = CommandCollection()
		try:
			command_collection.add_subcommand(func, parent=parent)
		except (SubcommandError, CommandCollectionError) as e:
			print(e)
			raise CommandLineError('error creating command line structure')

		return func
	return subcmd_dec


def member_of_a_class(func):
	argspec = inspect.getargspec(func)

	if len(argspec.args) == 0:
		return False

	return argspec.args[0] == 'self'


def maincmd(func):
	if member_of_a_class(func):
		func.maincmd = True
		return func

	command_collection = CommandCollection()
	try:
		command_collection.add_maincommand(func)
	except (MaincommandError, CommandCollectionError) as e:
		print(e)
		raise CommandLineError('error creating command line structure')

	return func
	
