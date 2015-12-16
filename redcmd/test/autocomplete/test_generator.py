from unittest import TestCase, main as ut_main

from redcmd.autocomplte.option_tree import OptionTree, OptionTreeError
from redcmd import CommandLine


class TestGenerator(TestCase):

	def test_gen(self):
		from . import subcmd

		
