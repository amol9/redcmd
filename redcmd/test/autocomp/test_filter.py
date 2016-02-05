from unittest import TestCase, main as ut_main
from fnmatch import fnmatch
from os.path import basename
import re

from redcmd.autocomp.filter import ListFilter, PathFilter


class TestFilter(TestCase):
	flist = ['a.txt', 'b.txt', 'one.html', 'lib', 'bin', 'asot.mp3', 'armin.mp3', 'readme', 'INSTALL', 'notes.txt']

	@classmethod
	def setUpClass(cls):
		cls.saved_PathFilter_glob = PathFilter.glob
		mock_glob = lambda s, p : [f for f in cls.flist if fnmatch(f, basename(p))]
		PathFilter.glob = mock_glob


	@classmethod
	def tearDownClass(cls):
		PathFilter.glob = cls.saved_PathFilter_glob


	def test_list_filter(self):
		filter = ListFilter(vlist=['blue', 'black', 'red', 'rose', 'green'])

		self.assertEqual(filter.match('bl'), ['blue', 'black'])
		self.assertEqual(filter.match('r'), ['red', 'rose'])
		self.assertEqual(filter.match('x'), [])


	def test_path_filter(self):
		dirpath = '/home/user/'

		pf = PathFilter(ext_list=['txt'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if f.endswith('.txt')])

		pf = PathFilter(ext_list=['txt', 'html'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if f.endswith('.txt') or f.endswith('.html')])

		pf = PathFilter()
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist])

		txt_filter = lambda x : re.match('^.{1}\.txt$', x) is not None
		pf = PathFilter(glob_list=['?.txt'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if txt_filter(f)])

		regex = '.*me.*'
		me_filter = lambda x : re.match(regex, x) is not None
		pf = PathFilter(regex_list=[regex])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if me_filter(f)])

		pf = PathFilter(regex_list=[regex], glob_list=['?.txt'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if me_filter(f) or txt_filter(f)])

		pf = PathFilter(regex_list=[regex], glob_list=['?.txt'], ext_list=['html'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if me_filter(f) or txt_filter(f) or f.endswith('.html')])
		
		dirpath = '/home/user/a'
		pf = PathFilter(ext_list=['txt'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if f.startswith('a') and f.endswith('.txt')])

		dirpath = '/home/user/ab'
		pf = PathFilter(ext_list=['txt'])
		self.assertItemsEqual(pf.match(dirpath), [f for f in self.flist if f.startswith('ab') and f.endswith('.txt')])


if __name__ == '__main__':
	ut_main()

