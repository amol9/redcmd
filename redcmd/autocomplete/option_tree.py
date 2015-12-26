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

	
	def gen(self, cmdline, lastword):
		words = cmdline.split()
		if words[-1] != lastword:
			words.append(lastword)

		if words[0] != self._root.name:
			raise GenError('command name: %s not valid for auto completion'%words[0])

		def has_subcmds(node):			# return true if given node has any subcommand
			if node.children is None:
				return False

			if node.children[0].subcmd:
				return True
			return False

		def find_by_name(name, nodelist):	# find a node by name in node list
			for node in nodelist:
				if node.name == name:
					return node
			return None

		node = self._root			# start at root node
		idx = 0
		for i in range(1, len(words) - 1):	# to find the innermost subcommand, just the main command if no subcommands are present
			if node.children is None:
				return []

			if not has_subcmds(node):
				idx = i - 1
				break			# innermost subcommand node found

			node = find_by_name(words[i], node.children)

			if node is None:
				raise GenError('bad subcommand name: %s'%words[i])
			idx += 1
					
		if has_subcmds(node):
			if len(words) - (idx + 1) > 1:
				raise GenError('bad subcommand name: %s'%words[idx + 1])
			else:
				return sorted([n.name for n in node.children if n.name.startswith(lastword)])

		optionals = [n for n in node.children if n.name.startswith('-')]
		positionals = [n for n in node.children if not n.name.startswith('-')]

		valid_hyphenated_val_regex = re.compile("-\.?\d+")	# some hyphenated values are valid argument values
		valid_hyphenated_val = lambda x : valid_hyphenated_val_regex.match(x) is not None

		def get_opt(name):	# get optional arg node by name or alias
			for n in optionals:
				if n.name == name or n.alias == name:
					return n
			return None
		
		opt_val = False		# True: last word is optional arg value
		opt_var = None		# last seen optional arg (node)
		pos_count = 0		# no. of positional arguments found (except last word)
		opt_seen = []		# optional args seen (so we don't suggest those again in autocomplete)
		for w in words[idx + 1 : -1]:
			if opt_val:
				opt_val = False
			else:
				opt_var = get_opt(w)
				opt_seen.append(opt_var)

				if opt_var is not None:
					opt_val = True
				else:
					pos_count += 1
			if pos_count > len(positionals):
				return []

		if opt_val:				# last word is an incomplete optional arg value
			return sorted(apply_filters(lastword, opt_var.filters))

		elif pos_count < len(positionals):	# last word could be an incomplete positional arg value
			pos_var = positionals[pos_count]
			return sorted(apply_filters(lastword, pos_var.filters))

		else:					# last word is an incomplete optional arg name
			opt_pairs = []
			for opt in sorted([o for o in optionals if o not in opt_seen], cmp=lambda x, y : cmp(x.name, y.name)):
				name = opt.name if opt.name.startswith(lastword) else None
				alias = opt.alias if opt.alias.startswith(lastword) else None

				opt_pairs.append((name, alias))

			options = []
			if len(opt_pairs) == 1:		# if only one optional arg is matching, just return its full name (-- prefixed name)
					name, alias = opt_pairs[0]
					if alias is None:
						return [name]
					else:
						return [alias]
			else:				# return "-o, --option_name" style pairs
				for name, alias in opt_pairs:
					if name is not None and alias is not None:
						options.append(name + ', ' + alias)
					elif name is not None:
						options.append(name)
					elif alias is not None:
						options.append(alias)

			return options
	

	def print_stack(self):
		print 'stack: ',
		print(', '.join([e.name for e in reversed(self._stack)]))

