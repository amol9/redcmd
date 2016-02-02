
from redcmd.api import Maincommand, maincmd, Arg


class Curlcommand(Maincommand):
	def options(self, headers=None, user_agent=None, cookie_file=None):
		self.headers 		= headers
		self.user_agent 	= user_agent
		self.cookie_file 	= cookie_file


	def output(self, output_file=None, verbose_level=Arg(default=0, choices=[0, 1, 2 ,3], opt=True)):
		self.output_file = output_file
		self.verbose_level = verbose_level


	@maincmd(add=[options, output])
	def curl(self, url):
		self.url = url

