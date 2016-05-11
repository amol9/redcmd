======
redcmd
======

A simple library to handle command line of an application with support for subcommands, as well as, automatic help text extraction from doc strings.


Supported platforms
===================

* python 2.7 / 3.4
* Linux / Windows


Features
========

* Decorator as well as subclass based command addition. 
* Custom help text formatter which improves upon the rather lousy default formatter.
* Automatic help text extraction from doc strings.
* Autocomplete support (Linux only).


Usage
=====
A simple case of just the main command (without any subcommands)::

        from redcmd.api import maincmd, execute_commandline

        @maincmd
        def main(a, b):
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

        execute_commandline() 

See examples directory in code for decorator and subclass based command handling.
[https://github.com/amol9/redcmd/tree/master/examples]


Download
========

* PyPI: http://pypi.python.org/pypi/redcmd
* Source: https://github.com/amol9/redcmd

