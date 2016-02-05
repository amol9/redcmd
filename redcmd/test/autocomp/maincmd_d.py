
from redcmd.api import maincmd, Arg, PathArg


class args:
	pass


def options(headers=None, user_agent=None, cookie_file=PathArg(opt=True, ext_list=['txt'])):
	args.headers 		= headers
	args.user_agent 	= user_agent
	args.cookie_file 	= cookie_file


def output(output_file=None, verbose_level=Arg(default=0, choices=[0, 1, 2 ,3], opt=True)):
	args.output_file 	= output_file
	args.verbose_level 	= verbose_level


@maincmd(add=[options, output])
def curl(url):
	a = url

