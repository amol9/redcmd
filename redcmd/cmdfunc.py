

class CmdFunc:
	def __init__(self, cmd_cls, func, arg_names, add=None):
		self.cmd_cls 	= cmd_cls
		self.func 	= func
		self.arg_names	= arg_names
		self.add	= add

	
	def execute(self, args):
		if self.add is not None:
			for a in add:
				add.execute(args)

		arg_list = [getattr(args, name) for name in self.arg_names]

		if self.cmd_cls is not None:
			self.func(self.cmd_cls(), *arg_list)
		else:
			self.func(*arg_list)

