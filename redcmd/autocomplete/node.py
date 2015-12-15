
class Node:

	def __init__(self, name, alias=None):
		self.name 	= name
		self.alias	= alias
		self.children 	= None


	def add_child(self, node):
		assert type(node) == Node

		if self.children is None:
			self.children = []
		self.children.append(node)

