
from redcmd import CommandLine, Maincommand, maincmd


class AddCommand(Maincommand):

	@maincmd
	def add(self, a, b, c, floating_point=False):
		if not floating_point:
			print(int(a) + int(b) + int(c))
		else:
			print(float(a) + float(b) + float(c))


if __name__ == '__main__':
	cl = CommandLine()
	cl.execute()

