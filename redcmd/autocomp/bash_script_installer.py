from os import access, getuid
from os.path import exists, join as joinpath, dirname

from zope.interface import implementer

from .shell_script_installer import IShellScriptInstaller
from .. import const

# print message if not root

@implementer(IShellScriptInstaller)
class BASHScriptInstaller:

	profile_d_dir		= '/etc/profile.d'
	profile_d_file 		= '/etc/profile.d/redcmd_autocomp.sh'
	bash_completion_d_dir	= '/etc/bash_completion.d'
	user_bashrc_file	= '.bashrc'

	id_prefix		= '__redcmd_autocomp_'
	user_script_file	= joinpath(const.script_dir, 'autocomp_func.sh')
	user_cmdlist_file	= joinpath(const.script_dir, 'autocomp_list.sh')

	script_template_file	= joinpath(dirname(__file__), 'scripts', 'bash_autocomp_function.sh')
	template_func_name	= '_redcmd_autocomp_function'


	def __init__(self):
		pass


	def is_root(self):
		return getuid() == 0


	def base_setup(self):
		rc, _ = sys_command('type %s'%const.autocomp_function)
		return rc == 0


	def completion_setup(self, cmdname):
		rc, op = sys_command('complete | grep %s'%cmdname)
		func = op.split()[-2] if rc == 0 else None

		return rc == 0, func


	def setup_base(self):
		if self.base_setup():
			print('BASH base script already setup')
			return

		script = None
		with open(self.script_template_file, 'r') as f:
			script = f.read()

		script = script.replace(self.template_func_name, const.autocomp_function)
		
		if self.is_root():
			if not access(self.profile_d_dir, w_OK):
				raise ShellScriptInstallerError('cannot write to %s'%self.system_profile_dir)

			with open(self.profile_d_file, 'w') as f:
				f.write(script)

	
		with open(self.user_script_file, 'w') as f:
			f.write(script + linesep)
			f.write('source %s'%self.user_cmdlist_file + linesep)

		with open(self.user_cmdlist_file, 'w') as f:
			pass

		tpatch = TextPatch(self.user_bashrc_file)
		tpatch.append_line("source \"%s\""%self.user_script_file, id=self.id_prefix + 'user_script')

		print('Setup BASH script for redcmd autocompletion for current user.\n\
			Note: if setup as root, then, autocompletion will be available system wide.')


		# export for current session
		sys_command(script)


	def remove_base(self):
		if not self.base_setup():
			print('base scripts for BASH are not setup')

		if is_root():
			try:
				remove(self.profile_d_file)
			except OSError as e:
				raise ShellScriptInstallError(e.msg)
		
		tpatch = TextPatch(self.user_bashrc_file)
		tpatch.remove_line(self.id_prefix + 'user_script')

		# remove for current session
		sys_command('unset -f %s'%const.autocomp_function)


	def setup_cmd(self, cmdname):
		if not self.base_setup():
			self.setup_base()

		if self.completion_setup(cmdname) == (True, _):
			print('command: %s is already setup for autocomplete')
			return
		
		cmd = 'complete -F %s %s'%s(const.autocomp_function, cmdname)

		if is_root():
			# add file to bash.autocomp dir
			with open(joinpath(self.bash_completion_d_dir, cmdname), 'w') as f:
					f.write(cmd + linesep)
		else:
			# add st to own script-2
			tp = TextPatch(self.user_cmdlist_file)
			tp.append_line(cmd, id=self.id_prefix + cmdname)

		# export for current session
		sys_command(cmd)


	def remove_cmd(self, cmdname):
		removed = False
		if is_root():
			filepath = joinpath(self.bash_completion_d_dir, cmdname)
			if exists(filepath):
				remove(filepath)

		tpatch = TextPatch(self.user_cmdlist_file)
		removed |= tpatch.remove_line(self.id_prefix + cmdname)

		if not removed:
			print('command: %s is not registered for autocomplete'%cmdname)
		else:
			# remove for current session
			sys_command('complete -r %s'%cmdname)

		print('autocomplete for %s removed'%cmdname)

