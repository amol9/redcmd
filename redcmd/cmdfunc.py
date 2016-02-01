import inspect

class CmdFunc:
	def __init__(self, cmd_cls, func, arg_names, add=None):
		self.cmd_cls 	= cmd_cls
		self.func 	= func
		self.arg_names	= arg_names
		self.add	= add

	
	def execute(self, args):
		if self.cmd_cls is not None:
			cmd_cls_instance = self.cmd_cls()

		if self.add is not None:
			for a in self.add:
				argspec = inspect.getargspec(a)
				if self.cmd_cls is not None:
					del argspec.args[0]
					arg_list = [getattr(args, name) for name in argspec.args]
					a(cmd_cls_instance, *arg_list)
				else:
					arg_list = [getattr(args, name) for name in argspec.args]
					a(*arg_list)

		arg_list = [getattr(args, name) for name in self.arg_names]
		if self.cmd_cls is not None:
			self.func(cmd_cls_instance, *arg_list)
		else:
			self.func(*arg_list)

