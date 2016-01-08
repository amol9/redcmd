from unittest import TestCase, main as ut_main

from redcmd.autocomp.generator import Generator, GenError
from redcmd import CommandLine


class TestGenerator(TestCase):

	def test_gen(self):
		from redcmd.test.autocomp import subcmd

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		cl._command_collection.make_option_tree()
		ot = cl._command_collection._optiontree

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
		self.assertEqual(gen('subcmd search query -e', ''), sorted(subcmd.search_engines))	
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


if __name__ == '__main__':
	ut_main()

