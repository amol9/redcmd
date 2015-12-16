from unittest import TestCase, main as ut_main

from redcmd.autocomplte.option_tree import OptionTree, OptionTreeError
from redcmd import CommandLine


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

		self.assertRaises(OptionTreeError, ot.pop, ())
	
		root = ot._root
		self.assertEquals(root._name, 'root')

		l1 = root._children
		self.assertEquals(l1[0]._name, 'level1-1')
		self.assertEquals(l1[0]._name, 'level1-2')
		self.assertEquals(l1[0]._name, 'level1-3')

		l2 = l1[0]._children
		self.assertEquals(l2[0]._name, 'level2-1')
		self.assertEquals(l2[1]._name, 'level2-2')


	#add defaults, choices, opt args
	def test_subcmd_option_tree_creation(self):
		from . import subcmd

		cl = CommandLine(prog='subcmd', description='none', version='1.0.0')
		cl.make_option_tree()

		ot = cl._command_collection._optiontree
		root = ot._root

		self.assertEquals(root._name, 'subcmd')
		
		cmp = lambda x, y : cmp(x._name, y._name) 
		sub = sorted(root._children, cmp=cmp)

		self.assertEquals([i._name for i in sub], ['display', 'math'])

		subsubmath = sorted(l1[1]._children, cmp=cmp)
		self.assertEquals([i._name for i in subsubmath], ['add', 'div', 'mul', 'sub'])

		add = subsubmath[0]
		#add arg tests


if __name__ == '__main__':
	ut_main()

