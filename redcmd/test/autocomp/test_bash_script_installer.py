from unittest import TestCase, main as ut_main
from shutil import copy, copytree, rmtree
import sys
from os import makedirs, mkdir, rmdir, remove, getuid
from os.path import exists, join as joinpath, basename, expanduser as eu

from redlib.misc.textpatch import TextPatch

from redcmd.autocomp.bash_script_installer import BASHScriptInstaller
from redcmd import const


# ***WARNING*** 
# the tests in this file will modify system files / dirs such as /etc/profile.d, /etc/bash_completion.d, ~/.bashrc
# backup these files / dirs first if you need to run these tests
# or, don't run these tests, they were added to aid the development
# the functions they test are rather trivial
# -

class TestBASHScriptInstaller(TestCase):
	test_home = './home'
	backup_path = eu('~/rcbackup')
	backup_dirs = ['/etc/profile.d', '/etc/bash_completion.d']
	backup_files = [eu('~/.bashrc')]

	@classmethod
	def setUpClass(cls):
		if exists (cls.test_home):
			rmdir(cls.test_home)
		mkdir(cls.test_home)

		cls.saved_user_home = const.user_home
		const.user_home = cls.test_home


	@classmethod
	def tearDownClass(cls):
		if exists (cls.test_home):
			rmdir(cls.test_home)

		const.user_home = cls.saved_user_home


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
			self.assertTrue(exists(bsi.profile_d_file))

		self.assertTrue(exists(bsi.user_script_file))
		self.assertTrue(exists(bsi.user_cmdlist_file))

		tp = TextPatch(bsi.user_bashrc_file)
		self.assertEqual(tp.find_line(bsi.id_prefix + 'user_script'), 1)


	def test_remove_base(self):
		bsi = BASHScriptInstaller()
		bsi.remove_base()

		if getuid() == 0:
			self.assertFalse(exists(bsi.profile_d_file))

		self.assertTrue(exists(bsi.user_script_file))
		self.assertTrue(exists(bsi.user_cmdlist_file))

		tp = TextPatch(bsi.user_bashrc_file)
		self.assertEqual(tp.find_line(bsi.id_prefix + 'user_script'), 0)


	def test_setup_cmd(self):
		bsi = BASHScriptInstaller()
		cmdname = 'subcmd' #'testcommand123'
		bsi.setup_cmd(cmdname)

				
	def test_remove_cmd(self):
		bsi = BASHScriptInstaller()
		cmdname = 'subcmd' #'testcommand123'
		bsi.remove_cmd(cmdname)


if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'backup':
		TestBASHScriptInstaller.backup()
	else:
		ut_main()

