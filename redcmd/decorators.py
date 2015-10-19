import inspect


def subcmd(parent=None):
	def subcmd_dec(func):
		func.subcmd = True

		cls = get_class_from_func(func)
		if issubclass(cls, Subcommand):
			return func

		
		return func
	return subcmd_dec


def get_class_from_func(func):
	for cls in inspect.getmro(func.im_class):
		if func.__name__ in cls.__dict__:
			return cls
	return None


def maincmd():
	pass
