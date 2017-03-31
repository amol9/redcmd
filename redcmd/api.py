'''from redlib.api.misc import make_api, Move

moves = []

exclude = ['test', 'version', 'main', '__main__', '__init__']

make_api(__name__, __file__, exclude=exclude, moves=moves)

__path__ = []

__package__ = __name__  # see PEP 366 @ReservedAssignment
if globals().get("__spec__") is not None:
	 __spec__.submodule_search_locations = []  # PEP 451 @UndefinedVariable
'''
#-

from importlib import import_module

from .commandline import CommandLine

from .func import execute_commandline
cmdline = execute_commandline

from .subcommand import Subcommand

from .decorators import *

from .exc import*

from types import ModuleType
import sys

class completer:
    module = '.autocomp.completer.all'

class arg:
    module = '.arg'


def make_api(cls):
    source_module = cls.module
    m = import_module(source_module, 'redcmd')

    for i in m.__all__:
        setattr(cls, i, getattr(m, i))

    #current_module = sys.modules[__name__]
    #setattr(current_module, cls, new_module)

    #new_module.__file__ = __file__
    #new_module.__package__ = 'redcmd.api'
    #new_module.__builtins__ = m.__all__

make_api(completer)
make_api(arg)

