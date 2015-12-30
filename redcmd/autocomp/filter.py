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
class GlobFilter:

	def __init__(self, patterns):
		self._patterns = patterns

	def match(self, name):
		# get current dir contents
		# apply all globs
		# return those that match any of the globs
		pass


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

