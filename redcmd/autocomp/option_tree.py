from pickle import dump as pickledump, load as pickleload, PicklingError, UnpicklingError
import re

from .node import Node
from .filter import apply_filters


class OptionTreeError(Exception):
	pass


class OptionTree:
	version = '1.0'

	def __init__(self):
		self._root = None
		self._stack = []


	def save(self, filepath):
		with open(filepath, 'w') as f:
			try:
				pickledump([version, self._root], f)
			except PicklingError as e:
				print(e)
				raise OptionTreeError('unable to save option tree')


	def load(self, filepath):
		with open(filepath, 'r') as f:
			try:
				data = pickleload(f)
			except UnpicklingError as e:
				log.error(str(e))

			version = data[0]
			if version > self.version:
				raise OptionTreeError('cannot load greater version, %s > %s'%(version, self.version))
			self._root = data[1]


	def add_node(self, node):
		assert node.__class__ == Node

		if self._root is None:
			self._root = node
		else:
			if self._stack is None or len(self._stack) == 0:
				raise OptionTreeError('option tree creation error: stack empty')
				
			self._stack[-1].add_child(node)

		self.push(node)

		
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


	def print_stack(self):
		print 'stack: ',
		print(', '.join([e.name for e in reversed(self._stack)]))


	root = property(get_root)

