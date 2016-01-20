import stat
from os.path import exists, join as joinpath, dirname
from os import access, getuid, linesep, chmod, lstat, W_OK, remove

from zope.interface import implementer
from redlib.api.misc import TextFile
from redlib.api.system import sys_command

from .. import const
from ..datastore import DataStore
from .shell_script_installer import IShellScriptInstaller, ShellScriptInstallError


@implementer(IShellScriptInstaller)
class BASHScriptInstaller:

	profile_d_dir		= '/etc/profile.d'
	profile_d_file 		= '/etc/profile.d/redcmd_autocomp.sh'
	bash_completion_d_dir	= '/etc/bash_completion.d'
	user_bashrc_file	= joinpath(const.user_home, '.bashrc')

	id_prefix		= '__redcmd_autocomp_'
	user_script_file	= joinpath(const.script_dir, 'autocomp_func.sh')
	user_cmdlist_file	= joinpath(const.script_dir, 'autocomp_list.sh')

	script_template_file	= joinpath(dirname(__file__), 'scripts', 'bash_autocomp_function.sh')
	template_func_name	= '_redcmd_autocomp_function'


	def __init__(self):
		dstore = DataStore()
		dstore.check_dir(script=True)


	def base_setup(self):
		tfile = TextFile(self.user_bashrc_file)

		user_setup = 	exists(self.user_script_file) and \
				(tfile.find_lines(self.id_prefix + 'user_script') > 0) and \
				exists(self.user_cmdlist_file)

		if getuid() == 0:
			return exists(self.profile_d_file) and user_setup
		else:
			return user_setup


	def completion_setup(self, cmdname):
		return False, 'a'	# temp
		rc, op = sys_command("bash -c 'complete | grep %s'"%cmdname)
		func = op.split()[-2] if rc == 0 else None

		return rc == 0, func


	def setup_base(self):
		script = None
		with open(self.script_template_file, 'r') as f:
			script = f.read()

		script = script.replace(self.template_func_name, const.autocomp_function)

		if getuid() == 0:
			if not access(self.profile_d_dir, W_OK):
				raise ShellScriptInstallerError('cannot write to %s'%self.system_profile_dir)

			with open(self.profile_d_file, 'w') as f:
				f.write(script)

		with open(self.user_script_file, 'w') as f:
			f.write(script + linesep)
			f.write('source %s'%self.user_cmdlist_file + linesep)

		chmod(self.user_script_file, lstat(self.user_script_file).st_mode | stat.S_IXUSR)

		if not exists(self.user_cmdlist_file):
			open(self.user_cmdlist_file, 'a').close()
			chmod(self.user_cmdlist_file, lstat(self.user_cmdlist_file).st_mode | stat.S_IXUSR)

		tfile = TextFile(self.user_bashrc_file)
		id = self.id_prefix + 'user_script'

		count = tfile.find_lines(id)
		if count > 1:
			tfile.remove_line(id, count=count-1)
		elif count == 0:
			tfile.append_line("source \"%s\""%self.user_script_file, id=self.id_prefix + 'user_script')

		if getuid() == 0:
			print('BASH scripts have been setup for redcmd autocomplete.')
		else:
			print('BASH scripts have been setup for redcmd autocomplete for current user.\n' +
				'Note: if setup as root, then, autocompletion will be available system wide.')


		# export for current session
		# popen('bash -c source ' + self.user_script_file)


	def remove_base(self):
		if getuid() == 0:
			try:
				remove(self.profile_d_file)
			except FileNotFoundError:
				pass
			except IOError as e:
				raise ShellScriptInstallError(str(e))
		
		tfile = TextFile(self.user_bashrc_file)
		tfile.remove_line(self.id_prefix + 'user_script')

		if getuid() != 0 and exists(self.profile_d_file):
			print('Base script has been removed from %s, but not from %s.\n'%(self.user_bashrc_file, self.profile_d_dir) +
				'Autocomplete supported by redcmd will still for commands setup for system wide autocomplete (i.e. as root).\n' +
				'Please execute as root to remove them.')
		else:
			print('Base scripts have been removed. Autocomplete supported by redcmd will no longer work.')

		# remove for current session
		#sys_command('unset -f %s'%const.autocomp_function)


	def setup_cmd(self, cmdname):
		if not self.base_setup():
			self.setup_base()

		cmd = 'complete -F %s %s'%(const.autocomp_function, cmdname)

		if getuid() == 0:
			with open(joinpath(self.bash_completion_d_dir, cmdname), 'w') as f:
					f.write(cmd + linesep)
		
		tp = TextFile(self.user_cmdlist_file)
		if not tp.find_lines(self.id_prefix + cmdname):
			tp.append_line(cmd, id=self.id_prefix + cmdname)

		# export for current session
		# popen('bash -c cmd)


	def remove_cmd(self, cmdname):
		if getuid() == 0:
			filepath = joinpath(self.bash_completion_d_dir, cmdname)
			if exists(filepath):
				try:
					remove(filepath)
				except OSError as e:
					print(e)

		try:
			tfile = TextFile(self.user_cmdlist_file)
			tfile.remove_line(self.id_prefix + cmdname)
		except textfileError as e:
			raise ShellScriptInstallerError(e)

		print('autocomplete for %s removed'%cmdname)

		# remove for current session
		# sys_command('complete -r %s'%cmdname)

