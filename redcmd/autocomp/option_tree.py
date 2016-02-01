import re

from redlib.api.prnt import prints

from .node import Node
from .filter import apply_filters


class OptionTreeError(Exception):
	pass


class OptionTree(object):
	version = '1.0'

	def __init__(self):
		self._root = None
		self._stack = []



	def add_node(self, node):
		assert node.__class__ == Node

		if self._root is None:
			self._root = node
		else:
			if self._stack is None or len(self._stack) == 0:
				raise OptionTreeError('option tree creation error: stack empty')
				
			self._stack[-1].add_child(node)

		self.push(node)


	def add_common(self, node):
		if self._stack is None or len(self._stack) == 0:
			raise OptionTreeError('option tree creation error: stack empty')

		self._stack[-1].add_common(node)

		
	def push(self, node):
		self._stack.append(node)

	
	def pop(self):
		if len(self._stack) == 0:
			raise OptionTreeError('node stack empty, cannot pop')

		node = self._stack[-1]
		del self._stack[-1]
		return node

	
	def get_root(self):
		return self._root


	def __getstate__(self):
		return self._root


	def __setstate__(self, root):
		self._root = root


	def print_stack(self):
		prints('stack: ')
		print(', '.join([e.name for e in reversed(self._stack)]))


	root = property(get_root)

