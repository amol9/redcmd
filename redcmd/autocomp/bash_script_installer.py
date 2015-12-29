from os import access
from os.path exists, join as joinpath


# print message if not root

@implementer(IShellSccriptInstaller)
class BASHScriptInstaller:
	system_profile_dir 	= '/etc/profile.d'
	system_profile_file 	= 'redcmd_autocomp.sh'
	user_profile_dir	= const.user_home
	user_bashrc_file	= '.bashrc'

	user_profile_id		= 'redcmd_autocomp_script'


	def __init__(self):
		pass


	def is_root(self):
		return getguid() == 0


	def base_setup(self):
		rc, _ = sys_command('type %s'%const.autocomp_function)
		return rc == 0


	def completion_setup(self, cmdname):
		rc, op = sys_command('complete | grep %s'%cmdname)
		func = op.split()[-2] if rc == 0 else None

		return rc == 0, func


	def setup_base(self):
		# copy source script to data dir
		# add source statement to .bashrc
		# or
		# copy source script to init~
		if self.base_setup():
			print('BASH base script already setup')
			return

		# load script
		# replace func name
		
		if self.is_root():
			if not access(self.system_profile_dir, w_OK):
				raise ShellScriptInstallerError('cannot write to %s'%self.system_profile_dir)

			with open(joinpath(self.system_profile_dir, self.system_profile_file), 'w') as f:
				f.write(script)

			# export??
		else:
			dstore = DataStore()
			script_path = None
			try:
				script_path = dstore.create_script(script)
			except DataStoreError as e:
				raise ShellScriptInstallerError(e.msg)

			tpatch = TextPatch()
			tpatch.append_line("source \"%s\""%script_path, id=self.user_profile_id)

			print('Setup BASH script for redcmd autocompletion for current user.\n\
				Note: if setup as root, then, autocompletion will be available system wide.')




	def setup_cmd(self, cmdname):
		if not base_setup():
			self.setup_base()

		if is_root():
			# add file to bash.autocomp dir
			# export
		else:
			# add st to own script-2
			# export for current session


	def remove_base(self):
		pass


	def remove_cmd(self,cmdname):
		pass

