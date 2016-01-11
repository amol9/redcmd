from unittest import TestCase, main as ut_main
import os
from os.path import dirname, join as joinpath, exists
from os import remove

from redcmd.autocomp.installer import Installer, InstallError
from redcmd import const


class TestInstaller(TestCase):

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


if __name__ == '__main__':
	ut_main()

