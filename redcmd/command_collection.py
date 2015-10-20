
from .mutils.misc import Singleton
from .command_help_formatter import CommandHelpFormatter
from .commandparser import CommandParser


class _CommandCollection:
	def __init__(self, prog=None, description=None, version=None):
		self.argparser = CommandParser(prog=prog, description=description, formatter_class=CommandHelpFormatter)
		self.argparser.add_argument('-v', '--version', action='version', version=version, help='print program version')
		

	def add_subcommand(self, func, parent=None, group_name=None, parser=None):
		subparsers = parent._subparsers

		if subparsers is None:
			if parent is None:
				subparsers = self.argparser.add_subparsers(group_name)
			else:
				if issubclass(parent, ArgumentParser):
					subparsers = parent.add_subparsers(group_name)
				elif type(parent) == str:
					#break the string, lookup the subparser and add to it
					parts = parent.split()
					parser = self.argparser
					for part in parts:
						if parser._subparsers is None:
							raise CommandCollectionError()

						parser = parser._subparsers._name_parser_map.get(part, None)
					
					if parser._subparsers is None:
						subparsers = parser.add_subparsers(parts[-1] + 'subcommand')
					else:
						subparsers = parser._subparsers

		return self.add_function(func, subparsers)
		
			

	def add_function(self, func, subparsers):
		if func.__name__ in parser._name_parser_map:
			raise CommandCollectionError('duplicate subcommand: %s'%func.__name__)

		funcdoc = func.__doc__ if func.__doc__ is not None else ''
		help_strings = docstring.extract_help(func)

		parser = subparsers.add_parser(func.__name__,
				prog=self.parser.prog + ' ' + func.__name__,
				formatter_class=self.parser.formatter_class,
				description=help_strings.get('help', None))
		subcmd = subcmd_cls(parser)

		argspec = inspect.getargspec(func)
		assert argspec.args[0] == 'self'
		del argspec.args[0]

		if argspec.defaults is not None:
			default_offset = len(argspec.args) - len(argspec.defaults)
		else:
			default_offset = len(argspec.args)


		for arg in argspec.args:
			arg_index = argspec.args.index(arg)

			default = None
			names 	= None
			choices = None
			nargs	= None
			if arg_index >= default_offset:
				default = argspec.defaults[arg_index - default_offset]
				names = ['-' + arg[0], '--' + arg]

				if default.__class__ == Choices:
					choices_obj = default
					choices = choices_obj.list
					default = choices_obj.default
					if default is None and not choices_obj.opt:
						names = [arg]
				elif default.__class__ == PositionalArg:
					nargs = default.nargs
					default = None
					names = [arg]

			else:
				names = [arg]

			kwargs = {
			'default'	: default,
			'choices'	: choices,
			'help'		: help_strings.get(arg, None)
			}

			if nargs is not None:
				kwargs['nargs'] = nargs
			parser.add_argument(*names, **kwargs)
			
			extrahelp = getattr(func, '__extrahelp__', None)
			if extrahelp is not None:
				parser.set_extrahelp(extrahelp)

		if not subcmd.subparsers:
			parser.set_defaults(subcmd_func=SubcmdFunc(subcmd, func, argspec.args))

	return parser


	def add_maincommand(self, func):
		pass


class CommandCollection(Singleton):
	classtype = _CommandCollection

