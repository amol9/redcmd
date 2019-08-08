
from ..decorators import subcmd
from ..subcommand import InternalSubcommand
from ..init.map import Map
from ..arg import Arg


class InitSubcommand(InternalSubcommand):


    @subcmd
    def init(self, filename, design=Arg(choices=Map.init_types.keys())):
        '''initialize idiomatic redcmd cli handler code

        design:
        filename:
        '''

        init_map = Map()
        init_map.run(design, filename)


'''
class InitSubSubcommands(InitSubcommand):

    @subcmd
'''
