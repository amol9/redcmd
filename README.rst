======
redcmd
======

A library to manage command line interface for an application.


Supported platforms
===================

* python 2.7 or python 3.x
* Linux


Features
========

* Decorator as well as subclassing based command addition. 
* Custom help text formatter which improves upon the rather sucky default formatter.
* Automatic help text extraction from doc string.


Usage
=====
A simple case of just the main command (without any subcommands)::

        @maincmd
	def main(self, a, b):
		'''Add two numbers.
		a: 	first number
		b: 	second number

		This is where extra help text goes.
		It can be more than one line.'''

		try:
			print('sum: %d'%(int(a) + int(b)))
		except ValueError:
			print('bad integer')
			raise CommandError()

        cmdline = CommandLine()
        try:
                cmdline.execute()
        except CommandLineError as e:
                print(e)


See examples directory in code for decorator and subclass based command handling.


Download
========
* PyPI: http://pypi.python.org/pypi/redcmd
* Source: https://github.com/amol9/redcmd

