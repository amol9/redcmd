
from zope.interface import Interface


class IShellScriptInstaller(Interface):

	def setup_base():
		pass


	def setup_cmd(cmdname):
		pass


	def remove_base():
		pass


	def remove_cmd(cmdname):
		pass

