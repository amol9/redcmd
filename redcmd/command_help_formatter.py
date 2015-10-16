from argparse import HelpFormatter, _SubParsersAction, SUPPRESS
import os
import textwrap

from mutils.misc import docstring
from mutils.system import terminalsize


class CommandHelpFormatter(HelpFormatter):

	def __init__(self, *args, **kwargs):
		if 'extrahelp' in kwargs.keys():
			self._extrahelp = kwargs['extrahelp']
			del kwargs['extrahelp']

		super(CommandHelpFormatter, self).__init__(*args, **kwargs)


	def format_help(self):
		help = self._root_section.format_help()
		if help:
		    help = self._long_break_matcher.sub('\n\n', help)
		    help = help.strip('\n') + '\n'
		    pass
		return help

	
	def _format_usage(self, usage, actions, groups, prefix):
		help = ''
		usage = 'usage: ' + self._prog + ' '

		optionals = []
		positionals = []
		for action in actions:
			if action.option_strings:
				optionals.append(action)
			else:
				positionals.append(action)

		col1 = 15
		terminal_width, _ = terminalsize.get_terminal_size()
		col2 = terminal_width - col1
		
		def format_help_lines(lines):
			out = ''
			first_line = True
			at_least_one_line = False

			for line in lines:
				if first_line:
					out += line
					first_line = False
				else:
					out += ('{0:<%d}{1}'%col1).format('', line)
				out += os.linesep
				at_least_one_line = True

			if not at_least_one_line:
				out += os.linesep
			return out

		def format_action(name, helptext, choices, default):

			out = ''
			def wrap(text):
				lines = []
				if text is not None and len(text) > 0 :
					lines = textwrap.wrap(text, col2)
				return lines

			help_lines = []
			for help_line in helptext.split('\n'):
				help_lines += wrap(help_line.strip())

			if choices is not None:
				choices = 'choices: ' + ', '.join(choices)

			choices_lines = wrap(choices)

			if not default in [None, SUPPRESS] :
				default = 'default: ' + default
			else:
				default = None
			
			default_lines = wrap(default)

			out += ('{0:<%d}'%(col1)).format(name)			
			out += format_help_lines(help_lines + choices_lines + default_lines)

			return out


		for o in optionals:
			name = ', '.join(o.option_strings)
			help += format_action(name, o.help, o.choices, o.default)
			usage += '[%s] '%name

		for p in positionals:
			if p.__class__ == _SubParsersAction:
				help += os.linesep + 'subcommands:' + os.linesep
				for subcmd in p.choices.keys():
					help += format_action(subcmd, p.choices[subcmd].description, None, None)

				usage += 'subcommand [args...]'
		
			else:
				help += format_action(p.dest, p.help, p.choices, p.default)
				usage += '%s '%p.dest

			if self._extrahelp is not None:
				help += os.linesep + docstring.trim(self._extrahelp)

		usage += os.linesep + os.linesep
		if help == '':
			return None

		return usage + help


	def _format_text(self, text):
		return docstring.trim(text) + os.linesep

