import os
from time import time

from redcmd import CommandLine, CommandLineError, subcmd, Arg


@subcmd
def add(a, b):
	'''Add two numbers
	a: first number
	b: second number'''

	print('sum: %d'%(int(a) + int(b)))


@subcmd
def subtract(a, b):
	'''Subtract two numbers
	a: first number
	b: second number'''

	print('diff: %d'%(int(a) - int(b)))


@subcmd
def display():
	'Display various attrbutes like, timestamp, username, etc.'
	pass		# body of this function will never be executed


@subcmd(parent='display')
def timestamp():
	'Print current timestamp.'

	print(time())	


@subcmd(parent='display')
def username():
	'Print logged in user\'s name.'

	print(os.getlogin())


if __name__ == '__main__':
	cmdline = CommandLine(prog='subcmd', description='A program to test subcommand addition using decorators.',
			version='1.0.0')
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

