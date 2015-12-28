
# print message if not root

@implementer(IShellSccriptInstaller)
class BASHScriptInstaller:

	def __init__(self):
		pass


	def setup_base(self):
		# copy source script to data dir
		# add source statement to .bashrc
		# or
		# copy source script to init~
		pass


	def setup_cmd(self, cmdname):
		# add to etc / source script
		pass


	def remove_base(self):
		pass


	def remove_cmd(self,cmdname):
		pass

