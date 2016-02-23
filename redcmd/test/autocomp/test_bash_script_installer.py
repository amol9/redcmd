from unittest import TestCase, main as ut_main, skip
import os
import sys
from shutil import copy, copytree, rmtree
from os import makedirs, mkdir, rmdir, remove, getuid
from os.path import exists, join as joinpath, basename, expanduser as eu, dirname

from redlib.api.misc import TextFile

from redcmd import const
from redcmd.autocomp.bash_script_installer import BASHScriptInstaller


# ***WARNING*** 
# the tests in this file will modify system files / dirs such as /etc/profile.d, /etc/bash_completion.d, ~/.bashrc
# backup these files / dirs first if you need to run these tests
# or, don't run these tests, they were added to aid the development
# the functions they test are rather trivial
# -


@skip
class TestBASHScriptInstaller(TestCase):

	test_home 	= './home'
	backup_path 	= eu('~/rcbackup')
	backup_dirs 	= ['/etc/profile.d', '/etc/bash_completion.d']
	backup_files 	= [eu('~/.bashrc')]
	test_cmd	= 'subcmd'


	@classmethod
	def setUpClass(cls):
		if exists (cls.test_home):
			rmdir(cls.test_home)
		mkdir(cls.test_home)

		cls.saved_user_home = const.user_home
		const.user_home = cls.test_home

		cls.saved_env_path = os.environ.get('PATH', '')
		os.environ['PATH'] = cls.saved_env_path + os.pathsep + dirname(__file__)


	@classmethod
	def tearDownClass(cls):
		if exists (cls.test_home):
			rmdir(cls.test_home)

		const.user_home = cls.saved_user_home
		os.environ['PATH'] = cls.saved_env_path


	@classmethod
	def backup(cls):
		if exists (cls.backup_path):
			rmtree(cls.backup_path)

		makedirs(cls.backup_path)

		for d in cls.backup_dirs:
			copytree(d, joinpath(cls.backup_path, basename(d)))

		for f in cls.backup_files:
			copy(f, cls.backup_path)

		print('backup created in %s'%cls.backup_path)


	def test_setup_base(self):
		bsi = BASHScriptInstaller()
		bsi.setup_base()

		if getuid() == 0:
			tf = TextFile(bsi.system_bashrc_file)
			self.assertTrue(tf.find_section(bsi.id_prefix + 'autocomplete_function'))

		self.assertTrue(exists(bsi.user_script_file))
		self.assertTrue(exists(bsi.user_cmdlist_file))

		tf = TextFile(bsi.user_bashrc_file)
		self.assertEqual(tf.find_lines(bsi.id_prefix + 'user_script'), 1)


	def test_remove_base(self):
		bsi = BASHScriptInstaller()
		bsi.remove_base()

		if getuid() == 0:
			tf = TextFile(bsi.system_bashrc_file)
			self.assertFalse(tf.find_section(bsi.id_prefix + 'autocomplete_function'))

		self.assertFalse(exists(bsi.user_script_file))
		self.assertTrue(exists(bsi.user_cmdlist_file))

		tf = TextFile(bsi.user_bashrc_file)
		self.assertEqual(tf.find_lines(bsi.id_prefix + 'user_script'), 0)


	def test_setup_cmd(self):
		bsi = BASHScriptInstaller()
		cmdname = self.test_cmd 
		bsi.setup_cmd(cmdname)

				
	def test_remove_cmd(self):
		bsi = BASHScriptInstaller()
		cmdname = self.test_cmd 
		bsi.remove_cmd(cmdname)


if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'backup':
		TestBASHScriptInstaller.backup()
	else:
		ut_main()

