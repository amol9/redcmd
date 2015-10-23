
class Arg:
	def __init__(self, pos=True, opt=False, choices=None, default=None, nargs=None):
		self.pos 	= pos
		self.opt 	= opt
		self.choices 	= choices
		self.default 	= default
		self.nargs 	= nargs

