from os import access, getuid, linesep, chmod, lstat, W_OK, remove
from os.path import exists, join as joinpath, dirname
import stat

from zope.interface import implementer
from redlib.system.sys_command import sys_command
from redlib.misc.textpatch import TextPatch

from .shell_script_installer import IShellScriptInstaller
from .. import const
from ..datastore import DataStore


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


	def is_root(self):
		return getuid() == 0


	def base_setup(self, root=True, user=True):
		#rc, _ = sys_command('type %s'%const.autocomp_function)
		tpatch = TextPatch(self.user_bashrc_file)
		if root and user:
			return exists(self.profile_d_file) and tpatch.find_line(self.id_prefix + 'user_script') > 0
		elif root:
			return exists(self.profile_d_file) 
		else:
			return tpatch.find_line(self.id_prefix + 'user_script') > 0


	def completion_setup(self, cmdname):
		return False, 'a'	# temp
		rc, op = sys_command("bash -c 'complete | grep %s'"%cmdname)
		func = op.split()[-2] if rc == 0 else None

		return rc == 0, func


	def setup_base(self):
		if self.base_setup():
			print('BASH base scripts already setup')
			return

		script = None
		with open(self.script_template_file, 'r') as f:
			script = f.read()

		script = script.replace(self.template_func_name, const.autocomp_function)
		
		if self.is_root() and not self.base_setup(user=False):
			if not access(self.profile_d_dir, W_OK):
				raise ShellScriptInstallerError('cannot write to %s'%self.system_profile_dir)

			with open(self.profile_d_file, 'w') as f:
				f.write(script)


		if not self.base_setup(root=False):
			with open(self.user_script_file, 'w') as f:
				f.write(script + linesep)
				f.write('source %s'%self.user_cmdlist_file + linesep)

			chmod(self.user_script_file, lstat(self.user_script_file).st_mode | stat.S_IXUSR)

			with open(self.user_cmdlist_file, 'w') as f:
				pass

			chmod(self.user_cmdlist_file, lstat(self.user_cmdlist_file).st_mode | stat.S_IXUSR)

			tpatch = TextPatch(self.user_bashrc_file)
			id = self.id_prefix + 'user_script'

			count = tpatch.find_line(id)
			if count > 1:
				tpatch.remove_line(id, count=count-1)
			elif count == 0:
				tpatch.append_line("source \"%s\""%self.user_script_file, id=self.id_prefix + 'user_script')

		if self.is_root() or self.base_setup(user=False):
			print('BASH scripts have been setup for redcmd autocomplete.')
		else:
			print('BASH scripts have been setup for redcmd autocomplete for current user.\n' +
				'Note: if setup as root, then, autocompletion will be available system wide.')


		# export for current session
		# popen('bash -c source ' + self.user_script_file)


	def remove_base(self):
		if self.is_root() and self.base_setup(user=False):
			try:
				remove(self.profile_d_file)
			except OSError as e:
				raise ShellScriptInstallError(e.msg)
		
		if self.base_setup(root=False):
			tpatch = TextPatch(self.user_bashrc_file)
			tpatch.remove_line(self.id_prefix + 'user_script')

		if not self.is_root() and self.base_setup(user=False):
			print('Base script has been removed from ~/.bashrc, but not from %s.\n'%self.profile_d_dir +
					'Please execute as root to remove it.')

		# remove for current session
		sys_command('unset -f %s'%const.autocomp_function)


	def setup_cmd(self, cmdname):
		if not self.base_setup():
			self.setup_base()

		if self.completion_setup(cmdname)[0]:
			print('command: %s is already setup for autocomplete')
			return
		
		cmd = 'complete -F %s %s'%(const.autocomp_function, cmdname)

		if self.is_root():
			with open(joinpath(self.bash_completion_d_dir, cmdname), 'w') as f:
					f.write(cmd + linesep)
		else:
			tp = TextPatch(self.user_cmdlist_file)
			tp.append_line(cmd, id=self.id_prefix + cmdname)

		# export for current session
		# popen('bash -c cmd)


	def remove_cmd(self, cmdname):
		removed = False
		if self.is_root():
			filepath = joinpath(self.bash_completion_d_dir, cmdname)
			if exists(filepath):
				remove(filepath)
				removed = True

		tpatch = TextPatch(self.user_cmdlist_file)
		removed |= tpatch.remove_line(self.id_prefix + cmdname) > 0

		if not removed:
			print('command: %s is not registered for autocomplete'%cmdname)
		else:
			# remove for current session
			# sys_command('complete -r %s'%cmdname)

			print('autocomplete for %s removed'%cmdname)

