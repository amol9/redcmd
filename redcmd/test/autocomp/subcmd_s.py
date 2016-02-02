
from redcmd.api import Subcommand, subcmd, Arg


class MathSubcommand(Subcommand):
	@subcmd
	def math(self):
		pass


class MathSubSubcommands(MathSubcommand):
	@subcmd
	def add(self, a, b):
		pass
	@subcmd
	def sub(self, a, b):
		pass
	@subcmd
	def mul(self, a, b):
		pass
	@subcmd
	def div(self, a, b):
		pass


class DisplaySubcommand(Subcommand):
	@subcmd
	def display(self):
		pass


class DisplaySubSubcommands(DisplaySubcommand):
	@subcmd
	def username(self):
		pass

	@subcmd
	def platform(self):
		pass


search_engines = ['google', 'bing', 'yahoo', 'duckduckgo']

class SearchSubcommand(Subcommand):

	@subcmd
	def search(self, query, engine=Arg(opt=True, choices=search_engines, default='google')):
		pass


	@subcmd
	def search_config(self, max_results=10, engine=None):
		pass


	@subcmd
	def set_engine(self, engine=Arg(choices=search_engines)):
		pass


class DbSubcommand(Subcommand):
	@subcmd
	def db(self):
		pass


class DbSubSubcommand(DbSubcommand):
	@subcmd
	def clear(self):
		pass


class ClearSubcommands(DbSubSubcommand):
	@subcmd
	def all(self):
		pass

	@subcmd
	def instance(self, id):
		pass


class TotalSubcommand(Subcommand):
	@subcmd
	def total(self, a, b, c, floating_point=False):
		pass


class UserSubcommand(Subcommand):
	def common(self, username='test'):
		pass

	@subcmd(add=[common])
	def userpass(self):
		pass
	
	@subcmd(add=[common])
	def userinfo(self):
		pass
