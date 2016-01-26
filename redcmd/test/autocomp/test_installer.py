from unittest import TestCase, main as ut_main, skip
import os
from os.path import dirname, join as joinpath, exists
from os import remove

from redcmd.autocomp.installer import Installer, InstallError
from redcmd import const


@skip
class TestInstaller(TestCase):
	remove_files = True
	test_cmd = 'subcmd'

	@classmethod
	def setUpClass(cls):
		cls.saved_env_path = os.environ.get('PATH', '')
		os.environ['PATH'] = cls.saved_env_path + os.pathsep + dirname(__file__)


	@classmethod
	def tearDownClass(cls):
		os.environ['PATH'] = cls.saved_env_path


	def test_setup_cmd(self):
		installer = Installer()
		installer.setup_cmd(self.test_cmd)

		self.assertTrue(exists(joinpath(const.autocomp_dir, self.test_cmd)))
		
		if self.remove_files:
			try:
				remove(joinpath(self.autocomp_dir, self.test_cmd))
			except IOError:
				pass


	def test_remove_non_existant_cmd(self):
		installer = Installer()

		with self.assertRaises(InstallError) as e:
			installer.remove_cmd('gxafdsew323')


if __name__ == '__main__':
	TestInstaller.remove_files = False
	ut_main()

