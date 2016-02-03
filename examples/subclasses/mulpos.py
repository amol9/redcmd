
from redcmd.api import Maincommand, maincmd, commandline_execute


class AddCommand(Maincommand):

	def common(self, a, b, msg=None):
		'''
		msg: 	message to be printed
		a: 	first number
		b: 	second number
		'''

		self.a = a
		self.b = b
		self.msg = msg


	@maincmd(add=[common])
	def add(self, c, d, floating_point=False):
		'''Add numbers.

		c: 		third number
		d: 		fourth number
		floating_point: perform a floating point addition.'''

		if self.msg is not None:
			print(self.msg)

		if not floating_point:
			print(int(self.a) + int(self.b) + int(c) + int(d))
		else:
			print(float(self.a) + float(self.b) + float(c) + float(d))


if __name__ == '__main__':
	commandline_execute(prog='test', description='add four numbers')

