from unittest import TestCase, main as ut_main

from redcmd.autocomp.option_tree import OptionTree, OptionTreeError
from redcmd.autocomp.node import Node
from redcmd.autocomp.filter import apply_filters
from redcmd.command_collection import CommandCollection
from redcmd import const

from redcmd.test.autocomp.dummy import DummyMaincommand, DummySubcommand


def sort_by_name(nodelist):
	return sorted(nodelist, cmp=lambda x, y : cmp(x.name, y.name))


class TestOptionTree(TestCase):

	def tearDown(self):
		CommandCollection().instance_map.pop(CommandCollection.classtype, None)	# remove singleton


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
		self.assertEqual(root._name, 'root')

		l1 = root.children
		self.assertIsNotNone(l1)
		self.assertEqual(l1[0].name, 'level1-1')
		self.assertEqual(l1[1].name, 'level1-2')
		self.assertEqual(l1[2].name, 'level1-3')

		l2 = l1[0].children
		self.assertIsNotNone(l2)
		self.assertEqual(l2[0].name, 'level2-1')
		self.assertEqual(l2[1].name, 'level2-2')


	def create_test_subcmd_ot(self, d=False):
		if not d:
			from redcmd.test.autocomp import subcmd_s
			search_engines = subcmd_s.search_engines
		else:
			from redcmd.test.autocomp import subcmd_d
			search_engines = subcmd_d.search_engines

		cc = CommandCollection()
		cc.set_details(prog='subcmd', description='none', version='1.0.0', _to_hyphen=False)
		ot = cc.make_option_tree(save=False, maincmd_cls=DummyMaincommand)

		subcmd_names = ['db', 'display', 'math', 'search', 'search_config', 'set_engine', 'total', 'userinfo', 'userpass']
		root = ot._root

		self.assertEqual(root.name, 'subcmd')
		self.assertIsNotNone(root.children)
		
		key_node = lambda n : n.name
		sub = sorted(root.children, key=key_node)

		self.assertEqual([i.name for i in sub], subcmd_names)

		subsubmath = sorted(sub[2].children, key=key_node)
		self.assertEqual([i.name for i in subsubmath], ['add', 'div', 'mul', 'sub'])

		add_args = sorted(subsubmath[0].children, key=key_node)
		self.assertEqual(len(add_args), 2)
		self.assertEqual([i.name for i in add_args], ['a', 'b'])

		subsubdisplay = sorted(sub[1].children, key=key_node)
		self.assertEqual([i.name for i in subsubdisplay], ['platform', 'username'])

		search = sub[3]
		search_args = sorted(search.children, key=key_node)
		self.assertEqual(search_args[0].name, '-e')
		self.assertEqual(search_args[0].alias, '--engine')

		engine_choices = sorted(apply_filters('', search_args[0].filters))
		self.assertEqual(engine_choices, sorted(search_engines))

		self.assertEqual(search_args[1].name, 'query')
		
		search_config = sub[4]

		search_config_args = sorted(search_config.children, key=key_node)
		self.assertEqual([(i.name, i.alias) for i in search_config_args], [('-e', '--engine'), ('-m', '--max_results')])
		self.assertEqual(apply_filters('', search_config_args[1].filters), ['10'])
		self.assertIsNone(search_config_args[0].children)

		db = sub[0]

		db_subs = sorted(db.children, key=key_node)
		self.assertEqual([i.name for i in db_subs], ['clear'])

		db_subsubs = db_subs[0].children
		self.assertEqual([i.name for i in sorted(db_subsubs, key=key_node)], ['all', 'instance'])

		all = db_subsubs[0]
		self.assertIsNone(all.children)

		clear = db_subsubs[1]
		self.assertEqual([i.name for i in sorted(clear.children, key=key_node)], ['id'])

		userinfo = sub[7]
		userinfo_args = userinfo.children
		self.assertEqual([(i.name, i.alias) for i in userinfo_args], [('-u', '--username')])
		
		userpass = sub[8]

		self.assertEqual(len(userpass.children), 1)
		userpass_args = userpass.children
		self.assertEqual([(i.name, i.alias) for i in userpass_args], [('-u', '--username')])



	def test_subcls_subcmd(self):
		self.create_test_subcmd_ot(d=False)


	def test_decorator_subcmd(self):
		self.create_test_subcmd_ot(d=True)


	def create_test_maincmd_ot(self, d=False):
		if not d:
			from redcmd.test.autocomp import maincmd_s
		else:
			from redcmd.test.autocomp import maincmd_d

		cc = CommandCollection()
		cc.set_details(prog='maincmd', description='none', version='1.0.0', _to_hyphen=False)
		ot = cc.make_option_tree(save=False, subcmd_cls=DummySubcommand)

		root = ot._root
		#import pdb; pdb.set_trace()
		self.assertEqual(root.name, 'maincmd')
		self.assertIsNotNone(root.children)

		args = sorted(['--headers', '--user_agent', '--cookie_file', '--output_file', '--verbose_level', 'url'])
		
		key = lambda n : n.name if n.alias is None else n.alias
		args_found = sorted(root.children, key=key)

		self.assertEqual(args, [key(n) for n in args_found])
		
	
	def test_subcls_maincmd(self):
		self.create_test_maincmd_ot(d=False)


	def test_decorator_maincmd(self):
		self.create_test_maincmd_ot(d=True)




if __name__ == '__main__':
	ut_main()

