import inspect


class CmdFunc:
	def __init__(self, cmd_cls, func, add=None):
		self.cmd_cls 	= cmd_cls		# command class
		self.func 	= func			# function to call
		self.add	= add			# additional functions (for common args)

		self._cmd_cls_instance = None

	
	def execute(self, args):
		if self.cmd_cls is not None:
			cmd_cls_instance = self.cmd_cls()

		if self.add is not None:
			for add_func in self.add:
				add_func(*self.get_arg_list(add_func, args))

		return self.func(*self.get_arg_list(self.func, args))


	def get_arg_list(self, func, args):
		argspec = inspect.getargspec(func)
		arg_list = []

		if len(argspec.args) > 0 and argspec.args[0] == 'self':
			del argspec.args[0]
			
			if self._cmd_cls_instance is None:
				self._cmd_cls_instance = self.cmd_cls()
			arg_list.append(self._cmd_cls_instance)

		arg_list.extend([getattr(args, name) for name in argspec.args])
		return arg_list

