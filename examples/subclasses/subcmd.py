import os
from time import time
import glob
from os.path import basename

from redcmd.api import CommandLine, CommandLineError, Subcommand, subcmd, PathArg


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


class DirSubcommand(Subcommand):

	@subcmd
	def ls(self, dirpath=PathArg()):
		'ls the dirpath.'

		for p in glob.glob(dirpath + os.sep + '*'):
			print(basename(p))


	@subcmd
	def cat(self, filepath=PathArg(ext_list=['txt'])):
		'cat the file.'

		with open(filepath, 'r') as f:
			print(f.read())


if __name__ == '__main__':
	cmdline = CommandLine(prog='subcmd', description='A program to test subcommand addition using subclassing.',
			version='1.0.0')
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

