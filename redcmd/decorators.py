import inspect

from . import CommandCollection
from .exc import CommandCollectionError, MaincommandError, SubcommandError, CommandLineError


def subcmd(parent=None):
	def subcmd_dec(func):
		cls = get_class_from_func(func)

		if issubclass(cls, Subcommand):
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


def get_class_from_func(func):
	for cls in inspect.getmro(func.im_class):
		if func.__name__ in cls.__dict__:
			return cls
	return None


def maincmd(func):
	cls = get_class_from_func(func)

	if issubclass(cls, Maincommand):
		func.maincmd = True
		return func

	command_collection = CommandCollection()
	try:
		command_collection.add_maincommand(func)
	except (MaincommandError, CommandCollectionError) as e:
		print(e)
		raise CommandLineError('error creating command line structure')

	return func
	
