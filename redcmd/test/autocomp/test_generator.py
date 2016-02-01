from unittest import TestCase, main as ut_main

from redcmd.commandline import CommandLine
from redcmd.command_collection import CommandCollection
from redcmd.autocomp.generator import Generator, GenError


class TestGenerator(TestCase):

	def tearDown(self):
		CommandCollection().instance_map.pop(CommandCollection.classtype, None)	# remove singleton


	def import_test_gen(self, dec=False):
		if not dec:
			from redcmd.test.autocomp import subcmd
			search_engines = subcmd.search_engines
		else:
			from redcmd.test.autocomp import subcmd_dec
			search_engines = subcmd_dec.search_engines

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		ot = cl._command_collection.make_option_tree(save=False)

		subcmd_names = ['db', 'display', 'math', 'search', 'search_config', 'set_engine', 'total']

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


	def test_subcls_subcmd(self):
		self.import_test_gen(dec=False)


	def test_dec_subcmd(self):
		self.import_test_gen(dec=True)


if __name__ == '__main__':
	ut_main()

