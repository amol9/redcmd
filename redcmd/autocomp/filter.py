import re
import glob
from os import sep
from os.path import dirname, basename, expanduser
from zope.interface import Interface, Attribute, implementer


class IFilter(Interface):

	def match(name):
		'Match a name / value against the filter.'
		

@implementer(IFilter)
class RegexFilter:

	def __init__(self, regexes):
		self._regexes = regexes

	
	def match(self, name):
		pass


@implementer(IFilter)
class PathFilter:

	def __init__(self, ext_list=[], regex_list=[], glob_list=[], path_arg_obj=None):
		if path_arg_obj is not None:
			self.ext_list 	= path_arg_obj.ext_list
			self.regex_list	= path_arg_obj.regex_list
			self.glob_list	= path_arg_obj.glob_list
		else:
			self.ext_list	= ext_list
			self.regex_list	= regex_list
			self.glob_list	= glob_list


	def match(self, name):
		dirpath = expanduser(dirname(name))
		if dirpath == '':
			dirpath = '.'

		if not any([len(i) > 0 for i in [self.ext_list, self.regex_list, self.glob_list]]):
			self.glob_list.append('*')		# no filters, return all

		ext_matches = []
		for e in self.ext_list:
			ext_matches.extend(self.glob(dirpath + sep + '*.' + e))

		glob_matches = []
		for p in self.glob_list:
			glob_matches.extend(self.glob(dirpath + sep + p))

		regex_matches = []
		if len(self.regex_list) > 0:
			allf = self.glob(dirpath + sep + '*')
			for r in self.regex_list:
				cr = re.compile(r)
				for p in allf:
					if cr.match(basename(p)) is not None:
						regex_matches.append(p)
		
		nodups = list(set(ext_matches + glob_matches + regex_matches))

		prefix = basename(name)
		if prefix != '':
			lf = ListFilter(nodups)
			return lf.match(prefix)
		else:
			return nodups


	def glob(self, path):
		return [basename(p) for p in glob.glob(path)]


	def __getstate__(self):
		return [self.ext_list, self.regex_list, self.glob_list]


	def __setstate__(self, data):
		self.ext_list 	= data[0]
		self.regex_list	= data[1]
		self.glob_list	= data[2]


	def __del__(self):
		del self.ext_list[:]
		del self.regex_list[:]
		del self.glob_list[:]


@implementer(IFilter)
class CommandFilter:

	def __init__(self, command, filter=None):
		self._command = command
		self._filter = filter

	def match(self, name):
		# evaluate command, apply filter to its output
		pass


@implementer(IFilter)
class RangeFilter:

	def match(self, name):
		pass


@implementer(IFilter)
class ListFilter:

	def __init__(self, vlist=None):
		self._vlist = vlist


	def match(self, name):
		if self._vlist is None:
			return [name]

		return [s for s in self._vlist if s.startswith(name)]


	def __getstate__(self):
		return self._vlist


	def __setstate__(self, vlist):
		self._vlist = vlist


def apply_filters(name, filters):
	matches = []

	if filters is None:
		return matches

	for filter in filters:
		matches.extend(filter.match(name))

	return matches

