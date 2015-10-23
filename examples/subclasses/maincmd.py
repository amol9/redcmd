
from redcmd import CommandLine, CommandLineError, Maincommand, maincmd


class MyMainCommand(Maincommand):

	@maincmd
	def main(self, a, b):
		print('sum: ', a + b)


if __name__ == '__main__':
	cmdline = CommandLine()
	try:
		cmdline.execute()
	except CommandLineError as e:
		print(e)

