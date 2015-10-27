from redcmd import maincmd, CommandLine, CommandLineError

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


cmdline = CommandLine()
try:
        cmdline.execute()
except CommandLineError as e:
        print(e)


