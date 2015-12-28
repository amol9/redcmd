from unittest import TestCase, main as ut_main

from redcmd.autocomp.generator import Generator, GenError
from redcmd import CommandLine


class TestGenerator(TestCase):

	def test_gen(self):
		from redcmd.test.autocomp import subcmd

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		cl.setup_autocomplete()

		subcmd_names = ['db', 'display', 'math', 'search', 'search_config', 'set_engine', 'total']
		ot = cl._command_collection._optiontree

		def gen(cmdline, lastword):
			gen = Generator(cmdline, lastword)
			gen._optiontree = ot
			return gen.gen()
		
		self.assertEquals(gen('subcmd', ''), subcmd_names)
		self.assertRaises(GenError, gen, 'not_reg', '')
		self.assertEquals(gen('subcmd', 'd'), ['db', 'display'])
		self.assertEquals(gen('subcmd', 'x'), [])
		self.assertEquals(gen('subcmd', 'ma'), ['math'])

		self.assertRaises(GenError, gen, 'subcmd engine', '')
		self.assertEquals(gen('subcmd set_engine', 'g'), ['google'])
		self.assertEquals(gen('subcmd set_engine', 'b'), ['bing'])
		self.assertEquals(gen('subcmd set_engine', 'x'), [])

		self.assertEquals(gen('subcmd search -', '-'), [])
		self.assertEquals(gen('subcmd search', ''), [])
		self.assertEquals(gen('subcmd search new', 'new'), [])

		self.assertEquals(gen('subcmd search_config', 'search_config'), ['search_config'])
		self.assertEquals(gen('subcmd search_config -', '-'), ['-e, --engine', '-m, --max_results'])
		self.assertEquals(gen('subcmd search_config -e', '-e'), ['-e'])
		self.assertEquals(gen('subcmd search_config --', '--'), ['--engine', '--max_results'])
		self.assertEquals(gen('subcmd search_config --m', '--m'), ['--max_results'])
		self.assertEquals(gen('subcmd search_config --x', '--x'), [])


		self.assertEquals(gen('subcmd search -e google', 'google'), ['google'])	
		self.assertEquals(gen('subcmd search query -e', ''), sorted(subcmd.search_engines))	
		self.assertEquals(gen('subcmd search query -e g', 'g'), ['google'])	
		self.assertEquals(gen('subcmd search query -', '-'), ['--engine'])	
		self.assertEquals(gen('subcmd search -e google query -', '-'), [])	
		self.assertEquals(gen('subcmd search -e google query -e', 'b'), ['bing'])	

		self.assertEquals(gen('subcmd search_config -e bing -m 20 -', '-'), [])
		self.assertEquals(gen('subcmd search_config -e bing -m 20 --e', '--e'), [])

		self.assertEquals(gen('subcmd total', ''), [])
		self.assertEquals(gen('subcmd total 10 20', ''), [])
		self.assertEquals(gen('subcmd total 10 20 30', ''), ['--floating_point'])
		self.assertEquals(gen('subcmd total -f true 10 20 30', ''), [])
		self.assertEquals(gen('subcmd total 10 -f true 20 30', ''), [])
		self.assertEquals(gen('subcmd total 10 20 30 -f', '-f'), ['-f'])


if __name__ == '__main__':
	ut_main()

