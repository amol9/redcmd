from unittest import TestCase, main as ut_main

from redcmd.autocomp import ListFilter


class TestFilter(TestCase):

	def test_list_filter(self):
		filter = ListFilter(vlist=['blue', 'black', 'red', 'rose', 'green'])

		self.assertEquals(filter.match('bl'), ['blue', 'black'])
		self.assertEquals(filter.match('r'), ['red', 'rose'])
		self.assertEquals(filter.match('x'), [])


if __name__ == '__main__':
	ut_main()

