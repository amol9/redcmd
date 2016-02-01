import os
from time import time

from redcmd.api import CommandLine, CommandLineError, Subcommand, subcmd


class MathSubcommands(Subcommand):

	def args(self, a, b):
		'''a: first number
		b: second number'''

		self.a = a
		self.b = b


	def more_args(self, c, d):
		'''c: third number
		d: fourth number'''

		self.c = c
		self.d = d


	@subcmd(add=[args])
	def add(self):
		'Add two numbers'

		print('sum: %d'%(int(self.a) + int(self.b)))


	@subcmd(add=[args])
	def subtract(self):
		'Subtract two numbers'

		print('diff: %d'%(int(self.a) - int(self.b)))


	@subcmd(add=[args, more_args])
	def add4(self):
		'Add 4 numbers.'

		print('sum: %d'%(int(self.a) + int(self.b) + int(self.c) + int(self.d)))


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
	cmdline = CommandLine(prog='subcmd', description='A program to test subcommand addition using subclassing.',
			version='1.0.0')
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

