import os
from time import time

from redcmd import CommandLine, CommandLineError, Subcommand, subcmd


class MathSubcommands(Subcommand):

	@subcmd
	def add(self, a, b):
		'''Add two numbers
		a: first number
		b: second number'''

		print('sum: %d'%(int(a) + int(b)))


	@subcmd
	def subtract(self, a, b):
		'''Subtract two numbers
		a: first number
		b: second number'''

		print('diff: %d'%(int(a) - int(b)))


class DisplaySubcommand(Subcommand):

	@subcmd
	def display(self):
		'Display various attrbutes like, timestamp, username, etc.'
		pass		# body of this function will never be executed


class DisplaySubSubcommands(DisplaySubcommand):

	@subcmd
	def timestamp(self):
		'Print current timestamp.'

		print(time())	

	
	@subcmd
	def username(self):
		'Print logged in user\'s name.'

		print(os.getlogin())


if __name__ == '__main__':
	print('subcmd')
	cmdline = CommandLine(prog='subcmd', description='A program to test subcommand addition using subclassing.',
			version='1.0.0')
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

