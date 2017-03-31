import re
import shlex

from .filter import apply_filters
from .completer.base import get_completions
from ..datastore import DataStore, DataStoreError


class GenError(Exception):
	pass


class Generator:

	def __init__(self, cmdline, lastword):
		self._cmdline = cmdline
		self._lastword = lastword

		if self._cmdline is None or len(self._cmdline) < 1:
			raise GenError('invalid command line: %s'%self._cmdline)

		self._optiontree = None
                self.filter_cmdline()


        def filter_cmdline(self):
                if self._cmdline.startswith('./'):
                    self._cmdline = self._cmdline[2:]

	
	def load(self):
		cmdname = self._cmdline.split()[0]
		dstore = DataStore()
		try:
			self._optiontree = dstore.load_optiontree(cmdname)
		except DataStoreError as e:
			raise GenError(e)


	def gen(self):
		words = self._cmdline.split()
		lastword = self._lastword

		if words[-1] != lastword:
			words.append(lastword)

		if words[0] != self._optiontree.root.name:
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

		node = self._optiontree.root		# start at root node
		idx = 0
		for i in range(1, len(words) - 1):	# to find the innermost subcommand, just the main command if no subcommands are present
			if node.children is None:
				return []

			if not has_subcmds(node):
				idx = i - 1
				break			# innermost subcommand node found

			node = find_by_name(words[i], node.children)

			if node is None:
				return []

			idx += 1

		if node.children is None:
			return []
					
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

                w_started_with_qt = False
                w_ended_with_qt = False
                w_ended_with_bs = False

                pos_val = False         # True: positional arg value continued
                last_term = ''          # last argument full value (with whitespaces, if any)
                is_quote = lambda c : c in ['"', "'"]

		for w in words[idx + 1 : -1]:
                        w_started_with_qt = (w[0] == '"' and w[-1] != '"') or (w[0] == "'" and w[-1] != "'")
                        w_ended_with_qt = is_quote(w[-1])
                        w_ended_with_bs = w[-1] == '\\'

			if opt_val:
                            last_term += ' %s'%w
                            if not w_started_with_qt or w_ended_with_qt:
				opt_val = False
                                last_term = ''
			else:
                                if pos_val:
                                    last_term += ' %s'%w
                                    if w_ended_with_qt:
                                        pos_val = False
                                        pos_count += 1
                                        last_term = ''

                                else:
                                    opt_var = get_opt(w)
                                    opt_seen.append(opt_var)

                                    if opt_var is not None:
                                            opt_val = True
                                            last_term = w
                                    else:
                                            #pos_count += 1
                                            last_term = w
                                            if w_started_with_qt:
                                                pos_val = True
                                            else:
                                                pos_count += 1

			if pos_count > len(positionals):
				return []

                if len(last_term) > 1:
                    if is_quote(last_term[-1]):
                        return []   # nothing to complete, since, the user has ended the value with a quote

                    if is_quote(last_term[0]):
                        last_term = last_term[1:] + ' ' + lastword

                else:
                    last_term = lastword

		if opt_val:				# last word is an incomplete optional arg value
			return sorted(get_completions(last_term, opt_var.filters))

		elif pos_count < len(positionals):	# last word could be an incomplete positional arg value
			pos_var = positionals[pos_count]
			return sorted(get_completions(last_term, pos_var.filters))

		else:					# last word is an incomplete optional arg name
			opt_pairs = []
			for opt in sorted([o for o in optionals if o not in opt_seen], key=lambda n : n.name):
				name = opt.name if opt.name.startswith(lastword) else None
				alias = opt.alias if opt.alias.startswith(lastword) else None

				if name is not None or alias is not None:
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

