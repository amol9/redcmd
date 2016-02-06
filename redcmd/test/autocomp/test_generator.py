from unittest import TestCase, main as ut_main
from fnmatch import fnmatch
from os.path import basename, join as joinpath, dirname

from redcmd.commandline import CommandLine
from redcmd.command_collection import CommandCollection
from redcmd.autocomp.generator import Generator, GenError
from redcmd.autocomp.filter import PathFilter

from redcmd.test.autocomp.dummy import DummyMaincommand, DummySubcommand


class TestGenerator(TestCase):
	flist = ['a.txt', 'b.txt', 'one.html', 'lib', 'bin', 'readme', 'INSTALL', 'notes.txt']

	@classmethod
	def setUpClass(cls):
		cls.saved_PathFilter_glob = PathFilter.glob
		mock_glob = lambda s, path, pat : [f for f in cls.flist if fnmatch(f, basename(pat))]
		PathFilter.glob = mock_glob


	@classmethod
	def tearDownClass(cls):
		PathFilter.glob = cls.saved_PathFilter_glob


	def tearDown(self):
		CommandCollection().instance_map.pop(CommandCollection.classtype, None)	# remove singleton


	def import_test_gen(self, d=False):
		if not d:
			from redcmd.test.autocomp import subcmd_s
			search_engines = subcmd_s.search_engines
		else:
			from redcmd.test.autocomp import subcmd_d
			search_engines = subcmd_d.search_engines

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		ot = cl._command_collection.make_option_tree(save=False, maincmd_cls=DummyMaincommand)

		subcmd_names = ['db', 'display', 'math', 'search', 'search_config', 'set_engine', 'total', 'userinfo', 'userpass']

		def gen(cmdline, lastword):
			gen = Generator(cmdline, lastword)
			gen._optiontree = ot
			return gen.gen()
		
		self.assertEqual(gen('subcmd', ''), subcmd_names)
		self.assertRaises(GenError, gen, 'not_reg', '')
		self.assertEqual(gen('subcmd', 'd'), ['db', 'display'])
		self.assertEqual(gen('subcmd', 'x'), [])
		self.assertEqual(gen('subcmd', 'ma'), ['math'])

		self.assertEqual(gen('subcmd engine', ''), [])
		self.assertEqual(gen('subcmd set_engine', 'g'), ['google'])
		self.assertEqual(gen('subcmd set_engine', 'b'), ['bing'])
		self.assertEqual(gen('subcmd set_engine', 'x'), [])

		self.assertEqual(gen('subcmd search -', '-'), [])
		self.assertEqual(gen('subcmd search', ''), [])
		self.assertEqual(gen('subcmd search new', 'new'), [])

		self.assertEqual(gen('subcmd search_config', 'search_config'), ['search_config'])
		self.assertEqual(gen('subcmd search_config -', '-'), ['-e, --engine', '-m, --max_results'])
		self.assertEqual(gen('subcmd search_config -e', '-e'), ['-e'])
		self.assertEqual(gen('subcmd search_config --', '--'), ['--engine', '--max_results'])
		self.assertEqual(gen('subcmd search_config --m', '--m'), ['--max_results'])
		self.assertEqual(gen('subcmd search_config --x', '--x'), [])


		self.assertEqual(gen('subcmd search -e google', 'google'), ['google'])	
		self.assertEqual(gen('subcmd search query -e', ''), sorted(search_engines))	
		self.assertEqual(gen('subcmd search query -e g', 'g'), ['google'])	
		self.assertEqual(gen('subcmd search query -', '-'), ['--engine'])	
		self.assertEqual(gen('subcmd search -e google query -', '-'), [])	
		self.assertEqual(gen('subcmd search -e google query -e', 'b'), ['bing'])	

		self.assertEqual(gen('subcmd search_config -e bing -m 20 -', '-'), [])
		self.assertEqual(gen('subcmd search_config -e bing -m 20 --e', '--e'), [])

		self.assertEqual(gen('subcmd total', ''), [])
		self.assertEqual(gen('subcmd total 10 20', ''), [])
		self.assertEqual(gen('subcmd total 10 20 30', ''), ['--floating_point'])
		self.assertEqual(gen('subcmd total -f true 10 20 30', ''), [])
		self.assertEqual(gen('subcmd total 10 -f true 20 30', ''), [])
		self.assertEqual(gen('subcmd total 10 20 30 -f', '-f'), ['-f'])

		self.assertEqual(gen('subcmd display platform', ''), [])
		self.assertEqual(gen('subcmd db search something', ''), [])
		self.assertEqual(gen('subcmd search_config -m 10 -', '-'), ['--engine'])
		self.assertEqual(gen('subcmd search_config -m 10 -x', '-x'), [])
		
		self.assertEqual(gen('subcmd userinfo ', ''), ['--username'])
		self.assertEqual(gen('subcmd userinfo -u ', ''), ['test'])

		self.assertEqual(gen('subcmd userpass ', ''), ['--username'])
		self.assertEqual(gen('subcmd userpass -u ', ''), ['test'])
		self.assertEqual(gen('subcmd userpass --username ', ''), ['test'])
		self.assertEqual(gen('subcmd userpass --username z', 'z'), [])
	
	
	def test_subcls_subcmd(self):
		self.import_test_gen(d=False)


	def test_decorator_subcmd(self):
		self.import_test_gen(d=True)


	def import_test_maincmd_gen(self, d=False):
		if not d:
			from redcmd.test.autocomp import maincmd_s
		else:
			from redcmd.test.autocomp import maincmd_d

		cl = CommandLine(prog='maincmd', description='none', version='1.0.0')
		ot = cl._command_collection.make_option_tree(save=False, subcmd_cls=DummySubcommand)

		def gen(cmdline, lastword):
			gen = Generator(cmdline, lastword)
			gen._optiontree = ot
			return gen.gen()
		
		self.assertEqual(gen('maincmd', ''), [])
		self.assertEqual(gen('maincmd some_url --u', '--u'), ['--user_agent'])
		self.assertEqual(gen('maincmd some_url -u Firefox --h', '--h'), ['--headers'])
		self.assertEqual(gen('maincmd some_url -u Firefox -x', '-x'), [])
		self.assertEqual(gen('maincmd some_url -h', '-h'), ['-he'])

		dirpath = '/home/user/'
		jp = lambda f : joinpath(dirname(dirpath), f)

		self.assertEqual(gen('maincmd some_url -c ', ''), [f for f in self.flist if f.endswith('.txt')])
		self.assertEqual(gen('maincmd some_url -c a', 'a'), ['a.txt'])
		self.assertEqual(gen('maincmd some_url -c /home/user/a', '/home/user/a'), [jp('a.txt')])


	def test_subcls_maincmd(self):
		self.import_test_maincmd_gen(d=False)


	def test_decorator_maincmd(self):
		self.import_test_maincmd_gen(d=True)


if __name__ == '__main__':
	ut_main()

