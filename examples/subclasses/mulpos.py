
from redcmd import CommandLine, Maincommand, maincmd


class AddCommand(Maincommand):

	@maincmd
	def add(self, a, b, c, floating_point=False):
		'''Add numbers.

		floating_point: Perform a floating point addition.'''

		if not floating_point:
			print(int(a) + int(b) + int(c))
		else:
			print(float(a) + float(b) + float(c))


if __name__ == '__main__':
	cl = CommandLine(_to_hyphen=True)
	cl.execute()

