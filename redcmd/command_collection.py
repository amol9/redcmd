import inspect

from mutils.misc import Singleton, docstring

from .command_help_formatter import CommandHelpFormatter
from .commandparser import CommandParser
from .arg import Arg
from .cmdfunc import CmdFunc
from .maincommand import Maincommand
from .subcommand import Subcommand


class _CommandCollection:
	def __init__(self):
		self._cmdparser = CommandParser(formatter_class=CommandHelpFormatter)


	def set_details(self, prog=None, description=None, version=None):
		self._cmdparser.prog = prog
		self._cmdparser.description = description

		if version is not None:
			self._cmdparser.add_argument('-v', '--version', action='version', version=version, help='print program version')

	
	def add_commands(self):
		self.add_maincommand_class(Maincommand)
		self.add_subcommand_class(Subcommand, self._cmdparser)



	def add_subcommand_class(self, cls, parser):
		for subcmd_cls in cls.__subclasses__():
			self.add_subcommand_group(subcmd_cls, parser)


	def add_subcommand_group(self, subcmd_cls, parser):
		for member_name, member_val in inspect.getmembers(subcmd_cls, predicate=\
		lambda x : inspect.ismethod(x) or inspect.isfunction(x)):

			if True or inspect.ismethod(member_val):
				func = member_val
				if getattr(func, 'subcmd', None) is not None:
					if not func.__name__ in subcmd_cls.__dict__.keys():
						continue

					subcmd_parser = self.add_subcommand(
								func,
								cmd_class=subcmd_cls,
								parent=self.parser,
								group_name=self.__class__.__name__,
								parser=subcmd_parser)

					self.add_subcommand_class(subcmd_cls, subcmd_parser)
		

	def add_subcommand(self, func, cmd_cls=None, parent=None, group_name=None, parser=None):
		subparsers = parent._subparsers

		if subparsers is None:
			if parent is None:
				subparsers = self._cmdparser.add_subparsers(group_name)
			else:
				if issubclass(parent, ArgumentParser):
					subparsers = parent.add_subparsers(group_name)
				elif type(parent) == str:
					#break the string, lookup the subparser and add to it
					parts = parent.split()
					parser = self._cmdparser
					for part in parts:
						if parser._subparsers is None:
							raise CommandCollectionError()

						parser = parser._subparsers._name_parser_map.get(part, None)
					
					if parser._subparsers is None:
						subparsers = parser.add_subparsers(parts[-1] + 'subcommand')
					else:
						subparsers = parser._subparsers

		return self.add_function(func, cmd_cls, subparsers)


	def add_function_to_subparsers(self, func, cmd_cls, subparsers):
		if func.__name__ in parser._name_parser_map:
			raise CommandCollectionError('duplicate subcommand: %s'%func.__name__)
		
		help = docstring.extract_help(func)

		parser = subparsers.add_parser(func.__name__,
				prog=self.parser.prog + ' ' + func.__name__,
				formatter_class=self._cmdparser.formatter_class,
				description=help.get('short', None))

		self.add_function_to_parser(func, cmd_cls, parser)
			

	def add_function_to_parser(self, func, cmd_cls, parser):
		help = docstring.extract_help(func)

		argspec = inspect.getargspec(func)
		if cmd_cls is not None:
			del argspec.args[0]

		if argspec.defaults is not None:
			defaults_offset = len(argspec.args) - len(argspec.defaults)
		else:
			defaults_offset = len(argspec.args)

		for arg in argspec.args:
			arg_index = argspec.args.index(arg)

			default = None				#add auto shortening
			names 	= None				
			choices = None				
			nargs	= None
			if arg_index >= defaults_offset:
				arg_default = argspec.defaults[arg_index - defaults_offset]
				names = ['-' + arg[0], '--' + arg]

				if arg_default.__class__ == Arg:
					choices = arg_default.choices
					default = arg_default.default
					nargs 	= arg_default.nargs

					if (default is None and not arg_default.opt) or arg_default.pos:
						names = [arg]

			else:
				names = [arg]		#positional argument

			kwargs = {
				'default'	: default,
				'choices'	: choices,
				'help'		: help.get(arg, None)
			}

			if nargs is not None:
				kwargs['nargs'] = nargs
			parser.add_argument(*names, **kwargs)
			
			extrahelp = help.get('extra', None)
			if extrahelp is not None:
				parser.set_extrahelp(extrahelp)

		#if not subcmd.subparsers:
		parser.set_defaults(cmd_func=CmdFunc(cmd_cls, func, argspec.args))

		return parser


	def add_maincommand_class(self, cls):
		subclasses = cls.__subclasses__()

		if len(subclasses) > 1:
			raise MainCommandError('only one class should derive from MainCommand')
		elif len(subclasses) == 0:
			return

		maincmd_cls = subclasses[0]

		for member_name, member_val in inspect.getmembers(maincmd_cls, predicate=\
		lambda x : inspect.ismethod(x) or inspect.isfunction(x)):

			func = member_val
			if getattr(func, 'maincmd', None) is not None:
				self.add_maincommand(func, cmd_cls=maincmd_cls)


	def add_maincommand(self, func, cmd_cls=None):
		if self._cmdparser._subparsers is not None:
			raise CommandCollectionError('cannot add main command when subcommands are also added')

		if self._cmdparser.get_default('cmd_func') is not None:
			raise CommandCollectionError('main command already added')

		self.add_function_to_parser(func, cmd_cls, self._cmdparser)


	def execute(self):
		args = self._cmdparser.parse_args()
		try:
			cmd_func = args.cmd_func
			cmd_func.execute(args)
		except AttributeError as e:
			print(e)


class CommandCollection(Singleton):
	classtype = _CommandCollection

