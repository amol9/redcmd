
from redcmd import CommandLine, CommandLineError, maincmd, CommandError, Arg


@maincmd
def main(a, b, color=Arg(choices=['red', 'blue', 'green'])):
	'''Add two numbers. 
	a: 	first number
	b: 	second number
	color: 	color name
		please specify one

	This is where extra help text goes.
	It can be more than one line.'''

	try:
		print('sum: %d'%(int(a) + int(b)))
	except ValueError:
		print('bad integer')
		raise CommandError()

	print(color)


if __name__ == '__main__':
	cmdline = CommandLine()
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

