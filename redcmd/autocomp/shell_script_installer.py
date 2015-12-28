
from redlib.system.common import is_linux, is_windows

from .bash_script_installer import BASHScriptInstaller
from .posh_script_installer import PoshScriptInstaller


class ShellScriptInstaller(Interface):

	def setup_base():
		pass


	def setup_cmd(cmdname):
		pass


	def remove_base():
		pass


	def remove_cmd(cmdname):
		pass


def get_script_installer():
	if is_linux():
		shell = os.environ.get('SHELL', None)

		if shell is None or shell.find('bash') == -1:
			raise ShellScriptInstallError('shell not supported (currently supported: BASH)')

		return BASHScriptInstaller()

	elif is_windows():
		return PoshScriptInstaller()

	else:
		raise ShellScriptInstallError('platform not supported')

