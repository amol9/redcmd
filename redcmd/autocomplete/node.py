
class Node:

	def __init__(self, name, alias=None, filters=None):
		self._name 	= name
		self._alias	= alias
		self._children 	= None
		self._filters	= None


	def add_child(self, node):
		assert node.__class__ == Node
		assert self._filters is None		# presence of a match filter means it's a positional or optional arg
							# can add child only to a command or subcommand
		if self._children is None:
			self._children = []
		self._children.append(node)


	def get_name(self):
		return self._name


	def get_alias(self):
		return self._alias


	def get_children(self):
		return self._children


	name		= property(get_name)
	alias		= property(get_alias)
	children	= property(get_children)

