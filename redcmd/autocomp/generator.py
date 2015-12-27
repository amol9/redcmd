
class GeneratorError(Exception):
	pass


class Generator:

	def __init__(self, command_line, word):
		self._command_line = command_line
		self._word = word


	def validate_command_line(self):
		if self._command_line is None or len(self._command_line) < 1:
			raise CompGenError('invalid command line: %s'%self._command_line)

	
	def gen(self):
		command_name = self._command_line.split()[0]
		ot_filepath = joinpath(const.autocomp_dir_path, command_name)

		if not exists(ot_filepath):
			raise CompGenError('%s is not registered for redcmd autocomplete'%command_name)

		optiontree = OptionTree()
		optiontree.load(ot_filepath)
		options = optiontree.gen(self._command_line, self._word)

		for option in options:
			print(option)

