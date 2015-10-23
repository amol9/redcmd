
from redcmd import CommandLine, CommandLineError, Subcommand, subcmd


class MySubcommands(Subcommand):

	@subcmd
	def add(self, a, b):
		'''Add two numbers
		a: first number
		b: second number'''

		print('sum: ', a + b)


	@subcmd
	def subtract(self, a, b):
		'''Subtract two numbers
		a: first number
		b: second number'''

		print('diff: ', a - b)


if __name__ == '__main__':
	cmdline = CommandLine()
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

