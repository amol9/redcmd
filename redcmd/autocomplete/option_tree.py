from pickle import dump as pickledump, load as pickleload, PicklingError, UnpicklingError


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
		assert type(node) == Node

		if self._root is None:
			self._root = node
			self.push(node)

		
	def push(self, node):
		self._stack.append(node)

	
	def pop(self):
		node = self._stack[-1]
		del self._stack[-1]
		return node

	
	def gen(self, cmd, word):
		pass

