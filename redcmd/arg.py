

class Choices:
	def __init__(self, list, default=None, opt=False):
		self.list = list
		assert default is None or self.list.index(default) >= 0
		self.default = default
		self.opt = opt

	
class PositionalArg:
	def __init__(self, nargs=None):
		self.nargs = nargs


