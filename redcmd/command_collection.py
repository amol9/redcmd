import inspect
from argparse import _SubParsersAction

from redlib.misc import Singleton, docstring

from .command_help_formatter import CommandHelpFormatter
from .commandparser import CommandParser
from .arg import Arg
from .cmdfunc import CmdFunc
from .maincommand import Maincommand
from .subcommand import Subcommand, InternalSubcommand
from .exc import CommandError, CommandCollectionError
from . import const
from .autocomp.option_tree import OptionTree, OptionTreeError
from .autocomp.node import Node
from .autocomp.filter import ListFilter
from .datastore import DataStore


# Notes
# -----
#
# -1-
# ArgumentParser::add_subparsers() assigns an instance of _ArgumentGroup to its member _subparsers,
# then, it adds an instance of _SubParsersAction to _subparsers using _ArgumentGroup::_add_action()
# and return that instance of _SubParsersAction.
# In this class, we just access that instance of _SubParsersAction using _subparsers._group_actions[0] as there is only one instance ever added. (Subsequent calls to add_subparsers() would raise an error).
#
# -2-
# General Logic:
# Main command: command line execution without any subcommands, if it is present, subcommands won't be added
# Subcommands: if one or more are added, main command won't be added
#
# Top level parser is an instance of CommandParser(ArgumentParser)
# If main command is to be added, we add it to top level parser.
# If a subcommand is to be added,
#   we call add_subparsers() on the parser (top level parser if no parent parser is mentioned) (_CommandCollection::add_subcommand)
#   then, we add a parser for the subcommand to the returned _SubParsersAction instance using add_parser() [see note 1]
#   (_CommandCollection::add_subcommand_to_spa)
#   finally, we add arguments to the parser using the provided function (_CommandCollection::add_args_to_parser)
#
# -3-
# _CommandCollection is an inner class. Not meant to be used directly.
# CommandCollection is the singleton that wraps a single instance of _CommandCollection.


class _CommandCollection:

	def __init__(self):
		self._cmdparser 		= CommandParser(formatter_class=CommandHelpFormatter)
		self._internal_cmdparser 	= None
		self._optiontree 		= None


	def set_details(self, prog=None, description=None, version=None, _to_hyphen=False):
		self._cmdparser.prog 		= prog
		self._cmdparser.description 	= description
		self._to_hyphen 		= _to_hyphen

		if version is not None:
			self._cmdparser.add_argument('-v', '--version', action='version', version=version, help='print program version')


	def make_option_tree(self, command_name=None):
		command_name = self._cmdparser.prog if command_name is None else command_name

		if command_name is None:
			raise CommandCollectionError('cannot create option tree without a command name')

		self._optiontree = OptionTree()
		self._optiontree.add_node(Node(command_name))
		self.add_commands()

		dstore = DataStore()
		dstore.save_optiontree(self._optiontree, command_name)

	
	def add_commands(self, maincmd_cls=None, subcmd_cls=None):			# to be called from class CommandLine to add
		maincmd_cls = Maincommand if maincmd_cls is None else maincmd_cls	# subclass members of Maincommand and Subcommand
		subcmd_cls = Subcommand if subcmd_cls is None else subcmd_cls

		self.add_maincommand_class(maincmd_cls)
		self.add_subcommand_classes(subcmd_cls, self._cmdparser)


	def add_internal_commands(self):
		self._internal_cmdparser = CommandParser(formatter_class=CommandHelpFormatter)
		self.add_subcommand_classes(InternalSubcommand, self._internal_cmdparser)


	def add_subcommand_classes(self, cls, parser):
		subcmd_added = False
		for subcmd_cls in cls.__subclasses__():
			subcmd_added |= self.add_subcommand_group(subcmd_cls, parser)
		return subcmd_added


	def add_subcommand_group(self, subcmd_cls, parser):
		subcmd_added = False
		for member_name, member_val in inspect.getmembers(subcmd_cls, predicate=\
		lambda x : inspect.ismethod(x) or inspect.isfunction(x)):

			if True or inspect.ismethod(member_val):
				func = member_val
				if getattr(func, const.subcmd_attr, None) is not None:
					if not func.__name__ in subcmd_cls.__dict__.keys():
						continue

					if self._optiontree is not None:
						self._optiontree.add_node(Node(func.__name__, subcmd=True))

					subcmd_parser = self.add_subcommand(
								func,
								cmd_cls=subcmd_cls,
								parent=parser,
								group_name=subcmd_cls.__name__.lower())
					subcmd_added = True

					self.add_subcommand_classes(subcmd_cls, subcmd_parser)

					if self._optiontree is not None:
						self._optiontree.pop()

		return subcmd_added
		

	# Adds a subcommand to a parent subcommand.
	#
	# func: 	function to be added as subcommand target
	# cmd_cls:	Subcommand subclass of which func is a member, just passed along to another method
	# parent:	parent subcommand
	# group_name: 	dest name for adding subparsers memeber to parent
	# 
	# if parent=None, add it to top level parser
	#
	# if parent type is string,
	#   it has to be of the form 'subcommand subcommand ...'
	#   e.g. if it is 'math add', then,
	#   this subcommand will be added as a child to 'add' subcommand which in turn is a child of 'math' subcommand
	#
	# if cmd_cls=None, it means subcommand is being added using decorator only (not subclassing of Subcommand)
	# if group_name=None, cmd_cls is also None, that is, decorator only addition
	#   so, we use parent subcommand name + 'subcommand' as group_name
	#
	def add_subcommand(self, func, cmd_cls=None, parent=None, group_name=None):
		if parent is None:
			parent = self._cmdparser
			group_name = const.subcmd_dest_suffix

		elif issubclass(parent.__class__, CommandParser):
			pass

		elif type(parent) == str:
			parts = parent.split()
			parent = self._cmdparser
			for part in parts:
				if parent._subparsers is None:
					raise CommandCollectionError('trying to add subcommands to a non-existant subcommand')

				parent = parent._subparsers._group_actions[0]._name_parser_map.get(part, None)

				if parent is None:
					raise CommandCollectionError('no such subcommand: %s'%' '.join(parts))
			group_name = parts[-1] + const.subcmd_dest_suffix
			
		subparsers = parent._subparsers
		spa = None
		
		if subparsers is None:
			spa = parent.add_subparsers(dest=group_name)
			spa.required = True

			if parent._defaults.get('cmd_func', None) is not None:	# if parent has a default, subcommands will use that
				del parent._defaults['cmd_func']

		else:
			spa = subparsers._group_actions[0]	
	
		return self.add_subcommand_to_spa(func, cmd_cls, spa)


	def add_subcommand_to_spa(self, func, cmd_cls, spa):		# add subcommand parser to _SubParsersAction instance
		assert spa.__class__ == _SubParsersAction

		subcmd_name = self.utoh(func.__name__)

		if subcmd_name in spa._name_parser_map:
			raise CommandCollectionError('duplicate subcommand: %s'%func.__name__)
		
		help = docstring.extract_help(func)

		parser = spa.add_parser(subcmd_name,			# add parser for subcommand
				prog=self._cmdparser.prog + ' ' + func.__name__,
				formatter_class=self._cmdparser.formatter_class,
				description=help.get('short', None))

		self.add_args_to_parser(func, cmd_cls, parser)

		return parser
			

	def add_args_to_parser(self, func, cmd_cls, parser):		# extract function argument information
		help = docstring.extract_help(func)			# and add them to parser,
									# extract help and add it to parser
		argspec = inspect.getargspec(func)
		if cmd_cls is not None:
			del argspec.args[0]				# remove arg: self in case of a class method

		if argspec.defaults is not None:			# find the offset at which arguments with default values start
			defaults_offset = len(argspec.args) - len(argspec.defaults)
		else:
			defaults_offset = len(argspec.args)

		used_short_names = []					# store used short names for arguments so as not to repeat them

		for arg in argspec.args:
			arg_index = argspec.args.index(arg)
			default = names = choices = nargs = action = None	

			if arg_index >= defaults_offset:		# argument has a default value
				arg_default = argspec.defaults[arg_index - defaults_offset]
				short = self.shorten_arg_name(arg, used_short_names)
				used_short_names.append(short)

				names = ['-' + short, '--' + arg]

				if arg_default.__class__ == Arg:
					choices = arg_default.choices
					default = arg_default.default
					nargs 	= arg_default.nargs

					if (default is None and not arg_default.opt) or arg_default.pos:
						names = [arg]		# positional argument
				else:
					if type(arg_default) == bool:
						if arg_default:
							action = 'store_false'
						else:
							action = 'store_true'
					else:
						default = arg_default

			else:
				names = [arg]				# positional argument

			if action is None:
				kwargs = {
					'default'	: default,
					'choices'	: choices,
					'help'		: help.get(arg, None)
				}
				if nargs is not None:
					kwargs['nargs'] = nargs
			else:
				kwargs = {
					'action'	: action,
					'help'		: help.get(arg, None)
				}

			names = [self.utoh(n) for n in names]
			parser.add_argument(*names, **kwargs)
			self.add_to_optiontree(names, default, choices)
		# end: for loop
			
		longhelp = help.get('long', None)	

		if longhelp is not None and len(longhelp) > 0:
			parser.set_extrahelp(longhelp)

		parser.set_defaults(cmd_func=CmdFunc(cmd_cls, func, argspec.args))	# set class and function to be called for execution


	def add_to_optiontree(self, names, default, choices):
		if self._optiontree is None:
			return

		name = names[0]
		alias = names[1] if len(names) > 1 else None

		filters = []
		if choices is not None:
			filters.append(ListFilter([str(c) for c in choices]))
		elif default is not None:
			filters.append(ListFilter([str(default)]))

		self._optiontree.add_node(Node(name, alias=alias, filters=filters))
		self._optiontree.pop()


	def shorten_arg_name(self, arg_name, used):
		char_count = 0
		short = None

		while short in used or short is None:
			char_count += 1
			short = arg_name[0 : char_count]

		return short


	def utoh(self, name):
		if self._to_hyphen:
			return name.replace('_', '-')
		else:
			return name
			

	def add_maincommand_class(self, cls):		# find a subclass of Maincommand, find any method decorated by @maincmd
		subclasses = cls.__subclasses__()	# and add it as main command

		if len(subclasses) > 1:
			raise MainCommandError('only one class should derive from MainCommand')
		elif len(subclasses) == 0:
			return		# it's ok, main command may have been added via decorator or not added at all

		maincmd_cls = subclasses[0]

		for member_name, member_val in inspect.getmembers(maincmd_cls, predicate=\
			lambda x : inspect.ismethod(x) or inspect.isfunction(x)):

			func = member_val
			if getattr(func, const.maincmd_attr, None) is not None:
				self.add_maincommand(func, cmd_cls=maincmd_cls)


	def add_maincommand(self, func, cmd_cls=None):		# add func as main command, if cmd_cls = None, func is a non-member
		if self._cmdparser._subparsers is not None:	# function, else, it is a member of a Maincommand subclass
			raise CommandCollectionError('cannot add main command when subcommands are also added')

		if self._cmdparser.get_default('cmd_func') is not None:
			raise CommandCollectionError('main command already added')

		self.add_args_to_parser(func, cmd_cls, self._cmdparser)


	def execute(self, args, namespace, internal=False):	# to be called for execution of command line
		args = None

		if not internal:
			args = self._cmdparser.parse_args(args, namespace)
		else:
			args = self._internal_cmdparser.parse_args(args, namespace)

		cmd_func = getattr(args, 'cmd_func', None)
		if cmd_func is None:
			raise CommandCollectionError('target function for command not found')

		try:
			cmd_func.execute(args)
		except CommandError as e:
			raise CommandCollectionError(e)


class CommandCollection(Singleton):
	classtype = _CommandCollection

