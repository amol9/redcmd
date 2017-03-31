import stat
from os.path import exists, join as joinpath, dirname
from os import access, linesep, chmod, lstat, W_OK, remove

from zope.interface import implementer
from redlib.api.misc import TextFile, TextFileError
from redlib.api.system import sys_command

from .. import const
from ..datastore import DataStore
from .shell_script_installer import IShellScriptInstaller, ShellScriptInstallError
from ..const import getuid
from .installer_const import bash


@implementer(IShellScriptInstaller)
class BASHScriptInstaller:
        '''
	profile_d_file 		= '/etc/profile.d/redcmd_autocomp.sh'
	bash_completion_d_dir	= '/etc/bash_completion.d'
	user_bashrc_file	= joinpath(const.user_home, '.bashrc')
	system_bashrc_file	= '/etc/bash.bashrc'

	id_prefix		= '__redcmd_autocomp_'
	user_script_file	= joinpath(const.script_dir, 'autocomp_func.sh')
	user_cmdlist_file	= joinpath(const.script_dir, 'autocomp_list.sh')

	script_template_file	= joinpath(dirname(__file__), 'scripts', 'bash_autocomp_function.sh')
	template_func_name	= '_redcmd_autocomp_function'
	shebang			= '#!/bin/bash'
        '''

	def __init__(self):
		dstore = DataStore()
		dstore.check_dir(script=True)


	def base_setup(self):
		tfile = TextFile(bash.user_bashrc_file)

		user_setup = 	exists(bash.user_script_file) and \
				(tfile.find_lines(bash.id_prefix + 'user_script') > 0) and \
				exists(bash.user_cmdlist_file)

		if getuid() == 0:
			tfile = TextFile(bash.system_bashrc_file)
			try:
				return tfile.find_section(bash.id_prefix + 'autocomplete_function') and user_setup
			except TextFileError as e:
				return False
		else:
			return user_setup


	def completion_setup(self, cmdname):
		return False, 'a'	# temp
		rc, op = sys_command("bash -c 'complete | grep %s'"%cmdname)
		func = op.split()[-2] if rc == 0 else None

		return rc == 0, func


	def setup_base(self):
		script = None
		with open(bash.script_template_file, 'r') as f:
			script = f.read()

		script = script.replace(bash.template_func_name, const.autocomp_function)

		if getuid() == 0:

			if not exists(bash.system_bashrc_file):
				print('%s does not exist, system wide redcmd autocomplete will not be available'%bash.system_bashrc_file)

			else:
				if not access(bash.system_bashrc_file, W_OK):
					raise ShellScriptInstallerError('cannot write to %s'%bash.system_bashrc_file)

				tfile = TextFile(bash.system_bashrc_file)
				tfile.append_section(script , id=bash.id_prefix + 'autocomplete_function')

		with open(bash.user_script_file, 'w') as f:
			f.write(bash.shebang + linesep)
			f.write(script + linesep)
			f.write('source %s'%bash.user_cmdlist_file + linesep)

		chmod(bash.user_script_file, lstat(bash.user_script_file).st_mode | stat.S_IXUSR)

		if not exists(bash.user_cmdlist_file):
			open(bash.user_cmdlist_file, 'a').close()
			chmod(bash.user_cmdlist_file, lstat(bash.user_cmdlist_file).st_mode | stat.S_IXUSR)

		tfile = TextFile(bash.user_bashrc_file)
		id = bash.id_prefix + 'user_script'

		count = tfile.find_lines(id)
		if count > 1:
			tfile.remove_lines(id, count=count-1)
		elif count == 0:
			tfile.append_line("source \"%s\""%bash.user_script_file, id=bash.id_prefix + 'user_script')

		if getuid() == 0:
			print('BASH scripts have been setup for redcmd autocomplete.')
		else:
			print('BASH scripts have been setup for redcmd autocomplete for current user.\n' +
				'Note: if setup as root, then, autocompletion will be available system wide.')


		# export for current session
		# popen('bash -c source ' + bash.user_script_file)


	def remove_base(self):
		tfile_system_bashrc = TextFile(bash.system_bashrc_file)
		err_msg = ''
		failed = False


		if getuid() == 0:
			self.remove_old_base()
			try:
				tfile_system_bashrc.remove_section(bash.id_prefix + 'autocomplete_function')
			except TextFileError as e:
				err_msg += str(e) + linesep
				failed = True
			except IOError as e:
				raise ShellScriptInstallError(str(e))
	
		try:
			tfile_user_bashrc = TextFile(bash.user_bashrc_file)
			tfile_user_bashrc.remove_lines(bash.id_prefix + 'user_script')
		except TextFileError as e:
			err_msg += str(e) + linesep
			failed= True

		if exists(bash.user_script_file):
			try:
				remove(bash.user_script_file)
			except (OSError, IOError) as e:
				err_msg += str(e) + linesep

		if len(err_msg) > 0:
			print(err_msg)

		if not failed and getuid() != 0 and tfile_system_bashrc.find_section(bash.id_prefix + 'autocomplete_function'):
			print('Base script has been removed from %s, but not from %s.\n'%(bash.user_bashrc_file, bash.system_bashrc_file) +
				'Autocomplete supported by redcmd will still for commands setup for system wide autocomplete (i.e. as root).\n' +
				'Please execute as root to remove them.')
		elif not failed:
			print('Base scripts have been removed. Autocomplete supported by redcmd will no longer work.')
		else:
			raise ShellScriptInstallError('Failed to remove base scripts.')

		# remove for current session
		#sys_command('unset -f %s'%const.autocomp_function)


	def remove_old_base(self):
		if exists(bash.profile_d_file):
			try:
				remove(bash.profile_d_file)
			except (OSError, IOError) as e:
				print(e + linesep + 'could not remove %s, please remove it manually'%bash.profile_d_file)


	def setup_cmd(self, cmdname):
		if not self.base_setup():
			self.setup_base()

		cmd = 'complete -F %s %s'%(const.autocomp_function, cmdname)

		if getuid() == 0:
			with open(joinpath(bash.bash_completion_d_dir, cmdname), 'w') as f:
					f.write(cmd + linesep)
		
		tp = TextFile(bash.user_cmdlist_file)
		if not tp.find_lines(bash.id_prefix + cmdname):
			tp.append_line(cmd, id=bash.id_prefix + cmdname)

		# export for current session
		# popen('bash -c cmd)


	def remove_cmd(self, cmdname):
		if getuid() == 0:
			filepath = joinpath(bash.bash_completion_d_dir, cmdname)
			if exists(filepath):
				try:
					remove(filepath)
				except OSError as e:
					print(e)

		try:
			tfile = TextFile(bash.user_cmdlist_file)
			tfile.remove_lines(bash.id_prefix + cmdname)
		except TextFileError as e:
			raise ShellScriptInstallerError(e)

		print('autocomplete for %s removed'%cmdname)

		# remove for current session
		# sys_command('complete -r %s'%cmdname)

