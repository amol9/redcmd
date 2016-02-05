
from .autocomp.filter import PathFilter


__all__ = ['Arg', 'PathArg', 'make_filter']


class Arg(object):
	def __init__(self, pos=True, opt=False, choices=None, default=None, nargs=None):
		if opt:
			pos = False

		self.pos 	= pos
		self.opt 	= opt
		self.choices 	= choices
		self.default 	= default
		self.nargs 	= nargs


class PathArg(Arg):
	def __init__(self, pos=True, opt=False, ext_list=[], regex_list=[], glob_list=[]):
		super(PathArg, self).__init__(pos=pos, opt=opt)

		self.ext_list	= ext_list
		self.regex_list	= regex_list
		self.glob_list	= glob_list


def make_filter(arg_obj):
	filter_obj = None

	if arg_obj.__class__ == Arg:
		pass

	elif arg_obj.__class__ == PathArg:
		filter_obj = PathFilter(path_arg_obj=arg_obj)

	return filter_obj

