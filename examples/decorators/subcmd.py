import os
from time import time
import platform as pf

from redcmd import CommandLine, CommandLineError, subcmd, Arg


@subcmd
def add(a, b):
	'''Add two numbers.
	a: first number
	b: second number'''

	print('sum: %d'%(int(a) + int(b)))


@subcmd
def subtract(a, b):
	'''Subtract second number from the first.
	a: first number
	b: second number'''

	print('diff: %d'%(int(a) - int(b)))


@subcmd
def display():
	'Display various attrbutes like, timestamp, username, etc.'
	pass						# body of this function will never be executed


@subcmd(parent='display')				# e.g. >subcmd display timestamp
def timestamp():
	'Display current timestamp.'

	print(time())	


@subcmd(parent='display')
def username():
	'Display logged in user\'s name.'

	print(os.getlogin())


@subcmd(parent='display')
def platform():
	'Display platform related information.'
	pass


@subcmd(parent='display platform')			# e.g. >subcmd display platform machine
def machine():
	'''Display machine type.
	e.g. i386'''

	print(pf.machine())


@subcmd(parent='display platform')			# e.g. >subcmd display platform platform -a true -t true
def platform(aliased=False, terse=False):
	'''Display information about the platform in a single string.
	aliased: use alias for platform name
	terse: display only the absolute minimum information'''

	print(pf.platform(aliased=1 if aliased else 0, terse=1 if terse else 0))

	
if __name__ == '__main__':
	cmdline = CommandLine(prog='subcmd', description='A program to test subcommand addition using decorators.',
			version='1.0.0')
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

