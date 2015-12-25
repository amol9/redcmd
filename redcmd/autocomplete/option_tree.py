from pickle import dump as pickledump, load as pickleload, PicklingError, UnpicklingError
import re

from .node import Node
from .filter import apply_filters


class OptionTreeError(Exception):
	pass


class GenError(Exception):
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

	
	def gen(self, cmd, word):
		words = cmd.split()
		if words[-1] != word:
			words.append(word)

		print 'words: ', ', '.join(words)

		if words[0] != self._root.name:
			raise GenError('command name: %s not valid for auto completion'%words[0])

		def has_subcmds(node):
			if node.children is None:
				return False

			if node.children[0].subcmd:
				return True
			return False

		def find_by_name(name, nodelist):
			for node in nodelist:
				if node.name == name:
					return node
			return None

		node = self._root
		args = None
		idx = 0
		for i in range(1, len(words) - 1):
			if node.children is None:
				return []

			if not has_subcmds(node):
				idx = i
				break		# innermost subcommand node found

			node = find_by_name(words[i], node.children)

			if node is None:
				raise GenError('bad subcommand name: %s'%words[i])
			idx += 1
					
		if len(words) - (idx + 1) > 1:		# start matching arguments
							# opt / pos-val / opt-val
			print 'more than 1'

			optionals = [n for n in node.children if n.name.startswith('-')]
			positionals = [n for n in node.children if not n.name.startswith('-')]

			valid_hyphenated_val_regex = re.compile("-\.?\d+")
			valid_hyphenated_val = lambda x : valid_hyphenated_val_regex.match(x) is not None

			def get_opt(name):
				for n in optionals:
					if n.name == name or n.alias == name:
						return n
				return None
			
			opt_val = False
			opt_var = None
			pos_count = 0
			for w in words[idx + 1 : -1]:
				if opt_val:
					opt_val = False
				else:
					opt_var = get_opt(w)
					if opt_var is not None:
						opt_val = True
					else:
						pos_count += 1
				if pos_count > len(positionals):
					return []

			if opt_val:
				return apply_filters(word, opt_var.filters)
			elif word.startswith('-'):
				options = []
				for opt in optionals:
					if opt.name.startswith(word) or opt.alias.startswith(word):
						options.append(opt.name + '' if opt.alias is None else ', %s'%opt.alias)
				return options
			else:		# positional
				if pos_count < len(positionals):
					pos_var = positionals[pos_count]
					return apply_filters(word, pos_var.filters)
				else:
					return []


		else:				# only 1, match incomp subcmd or opt arg name or pos arg filter
			print 'only 1'
			if node.children is None:
				return []

			if has_subcmds(node):
				return sorted([n.name for n in node.children if n.name.startswith(word)])

			positionals = [n for n in node.children if not n.name.startswith('-')]

			if len(positionals) > 0:
				return apply_filters(word, positionals[0].filters)

			options = []

			for optional in sorted(node.children, cmp=lambda x, y : cmp(x.name, y.name)):
				if optional.name.startswith(word):
					options.append(optional.name)

				if optional.alias.startswith(word):
					options.append(optional.alias)

			return options


	def print_stack(self):
		print 'stack: ',
		print(', '.join([e.name for e in reversed(self._stack)]))

