from unittest import TestCase, main as ut_main

from redcmd.autocomplete import OptionTree, OptionTreeError, Node, apply_filters, GenError
from redcmd import CommandLine


def sort_by_name(nodelist):
	return sorted(nodelist, cmp=lambda x, y : cmp(x.name, y.name))


class TestOptionTree(TestCase):

	def test_tree_creation(self):
		ot = OptionTree()

		ot.add_node(Node('root'))
		ot.add_node(Node('level1-1'))
		ot.add_node(Node('level2-1'))
		ot.pop()
		ot.add_node(Node('level2-2'))
		ot.pop()
		ot.pop()
		ot.add_node(Node('level1-2'))
		ot.pop()
		ot.add_node(Node('level1-3'))
		ot.pop()
		ot.pop()

		self.assertRaises(OptionTreeError, ot.pop)
	
		root = ot._root
		self.assertEquals(root._name, 'root')

		l1 = root.children
		self.assertIsNotNone(l1)
		self.assertEquals(l1[0].name, 'level1-1')
		self.assertEquals(l1[1].name, 'level1-2')
		self.assertEquals(l1[2].name, 'level1-3')

		l2 = l1[0].children
		self.assertIsNotNone(l2)
		self.assertEquals(l2[0].name, 'level2-1')
		self.assertEquals(l2[1].name, 'level2-2')


	def test_subcmd_option_tree_creation(self):
		from redcmd.test.autocomplete import subcmd

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		cl.register_autocomplete()

		subcmd_names = ['db', 'display', 'math', 'search', 'search_config', 'set_engine', 'total']
		ot = cl._command_collection._optiontree
		root = ot._root

		self.assertEquals(root.name, 'subcmd')
		self.assertIsNotNone(root.children)
		
		cmp_nodes = lambda x, y : cmp(x.name, y.name) 
		sub = sorted(root.children, cmp=cmp_nodes)

		self.assertEquals([i.name for i in sub], subcmd_names)

		subsubmath = sorted(sub[2].children, cmp=cmp_nodes)
		self.assertEquals([i.name for i in subsubmath], ['add', 'div', 'mul', 'sub'])

		add_args = sorted(subsubmath[0].children, cmp=cmp_nodes)
		self.assertEquals(len(add_args), 2)
		self.assertEquals([i.name for i in add_args], ['a', 'b'])

		subsubdisplay = sorted(sub[1].children, cmp=cmp_nodes)
		self.assertEquals([i.name for i in subsubdisplay], ['platform', 'username'])

		search = sub[3]
		search_args = sorted(search.children, cmp=cmp_nodes)
		self.assertEquals(search_args[0].name, '-e')
		self.assertEquals(search_args[0].alias, '--engine')

		engine_choices = sorted(apply_filters('', search_args[0].filters))
		self.assertEquals(engine_choices, sorted(subcmd.search_engines))

		self.assertEquals(search_args[1].name, 'query')
		
		search_config = sub[4]

		search_config_args = sorted(search_config.children, cmp=cmp_nodes)
		self.assertEquals([(i.name, i.alias) for i in search_config_args], [('-e', '--engine'), ('-m', '--max_results')])
		self.assertEquals(apply_filters('', search_config_args[1].filters), ['10'])
		self.assertIsNone(search_config_args[0].children)

		db = sub[0]

		db_subs = sorted(db.children, cmp=cmp_nodes)
		self.assertEquals([i.name for i in db_subs], ['clear'])

		db_subsubs = db_subs[0].children
		self.assertEquals([i.name for i in sorted(db_subsubs, cmp=cmp_nodes)], ['all', 'instance'])

		all = db_subsubs[0]
		self.assertIsNone(all.children)

		clear = db_subsubs[1]
		self.assertEquals([i.name for i in sorted(clear.children, cmp=cmp_nodes)], ['id'])


	def test_gen(self):
		from redcmd.test.autocomplete import subcmd

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		cl.register_autocomplete()

		subcmd_names = ['db', 'display', 'math', 'search', 'search_config', 'set_engine', 'total']
		ot = cl._command_collection._optiontree
		subcmds = sort_by_name(ot._root.children)
		
		self.assertEquals(ot.gen('subcmd', ''), subcmd_names)
		self.assertRaises(GenError, ot.gen, 'not_reg', '')
		self.assertEquals(ot.gen('subcmd', 'd'), ['db', 'display'])
		self.assertEquals(ot.gen('subcmd', 'x'), [])
		self.assertEquals(ot.gen('subcmd', 'ma'), ['math'])

		self.assertRaises(GenError, ot.gen, 'subcmd engine', '')
		self.assertEquals(ot.gen('subcmd set_engine', 'g'), ['google'])
		self.assertEquals(ot.gen('subcmd set_engine', 'b'), ['bing'])
		self.assertEquals(ot.gen('subcmd set_engine', 'x'), [])

		self.assertEquals(ot.gen('subcmd search -', '-'), [])
		self.assertEquals(ot.gen('subcmd search', ''), [])
		self.assertEquals(ot.gen('subcmd search new', 'new'), [])

		self.assertEquals(ot.gen('subcmd search_config', 'search_config'), ['search_config'])
		self.assertEquals(ot.gen('subcmd search_config -', '-'), ['-e, --engine', '-m, --max_results'])
		self.assertEquals(ot.gen('subcmd search_config -e', '-e'), ['-e'])
		self.assertEquals(ot.gen('subcmd search_config --', '--'), ['--engine', '--max_results'])
		self.assertEquals(ot.gen('subcmd search_config --m', '--m'), ['--max_results'])
		self.assertEquals(ot.gen('subcmd search_config --x', '--x'), [])


		self.assertEquals(ot.gen('subcmd search -e google', 'google'), ['google'])	
		self.assertEquals(ot.gen('subcmd search query -e', ''), sorted(subcmd.search_engines))	
		self.assertEquals(ot.gen('subcmd search query -e g', 'g'), ['google'])	
		self.assertEquals(ot.gen('subcmd search query -', '-'), ['--engine'])	
		self.assertEquals(ot.gen('subcmd search -e google query -', '-'), [])	
		self.assertEquals(ot.gen('subcmd search -e google query -e', 'b'), ['bing'])	

		self.assertEquals(ot.gen('subcmd search_config -e bing -m 20 -', '-'), [])
		self.assertEquals(ot.gen('subcmd search_config -e bing -m 20 --e', '--e'), [])

		self.assertEquals(ot.gen('subcmd total', ''), [])
		self.assertEquals(ot.gen('subcmd total 10 20', ''), [])
		self.assertEquals(ot.gen('subcmd total 10 20 30', ''), ['--floating_point'])
		self.assertEquals(ot.gen('subcmd total -f true 10 20 30', ''), [])
		self.assertEquals(ot.gen('subcmd total 10 -f true 20 30', ''), [])
		self.assertEquals(ot.gen('subcmd total 10 20 30 -f', '-f'), ['-f'])


if __name__ == '__main__':
	ut_main()

