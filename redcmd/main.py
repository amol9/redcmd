import sys

from . import CommandLine, CommandLineError
from . import const
from .version import __version__


def main():
	commandline = CommandLine(prog=const.prog_name, description='Client for redcmd package.', 
			version=__version__, _to_hyphen=True)
	try:
		commandline.execute()
	except CommandLineError as e:
		print(e)
		sys.exit(1)

	sys.exit(0)

