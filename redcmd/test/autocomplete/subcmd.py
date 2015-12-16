
from redcmd import Subcommand, subcmd


class MathSubcommand(Subcommand):
	@subcmd
	def math(self):
		pass

class MathSubSubcommands(MathSubcommand):
	@subcmd
	def add(self, a, b):
		pass
	@subcmd
	def sub(self, a, b):
		pass
	@subcmd
	def mul(self, a, b):
		pass
	@subcmd
	def div(self, a, b):
		pass

class DisplaySubcommand(Subcommand):
	@subcmd
	def display(self):
		pass


