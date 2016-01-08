from unittest import TestCase, main as ut_main

from redcmd.autocomp.filter import ListFilter


class TestFilter(TestCase):

	def test_list_filter(self):
		filter = ListFilter(vlist=['blue', 'black', 'red', 'rose', 'green'])

		self.assertEqual(filter.match('bl'), ['blue', 'black'])
		self.assertEqual(filter.match('r'), ['red', 'rose'])
		self.assertEqual(filter.match('x'), [])


if __name__ == '__main__':
	ut_main()

