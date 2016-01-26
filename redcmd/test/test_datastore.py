from unittest import TestCase, main as ut_main, skip

from redcmd.autocomp.option_tree import OptionTree, OptionTreeError
from redcmd.autocomp.node import Node
from redcmd.datastore import DataStore


class TestDataStore(TestCase):

	def test_save_load_optiontree(self):
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

		ds = DataStore()
		ds.save_optiontree(ot, 'test')
	
		ot2 = ds.load_optiontree('test')
		root = ot2._root
		self.assertEqual(root._name, 'root')


	@skip('improve')
	def test_list(self):
		ds = DataStore()
		commands = ds.list_optiontree()

		for c in commands:
			print(c)


if __name__ == '__main__':
	ut_main()

