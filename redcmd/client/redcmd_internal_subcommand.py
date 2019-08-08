
from ..decorators import subcmd
from ..subcommand import RedcmdInternalSubcommand


class RedcmdInternal(RedcmdInternalSubcommand):

	@subcmd
	def redcmdinternal(self):
		'redcmd internal commands'
		pass

