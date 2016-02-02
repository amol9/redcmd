
from redcmd.api import subcmd, Arg


@subcmd
def math():
	pass


@subcmd(parent='math')
def add(a, b):
	pass

@subcmd(parent='math')
def sub(a, b):
	pass

@subcmd(parent='math')
def mul(a, b):
	pass

@subcmd(parent='math')
def div(a, b):
	pass


@subcmd
def display():
	pass


@subcmd(parent='display')
def username():
	pass

@subcmd(parent='display')
def platform():
	pass


search_engines = ['google', 'bing', 'yahoo', 'duckduckgo']

@subcmd
def search(query, engine=Arg(opt=True, choices=search_engines, default='google')):
	pass

@subcmd
def search_config(max_results=10, engine=None):
	pass

@subcmd
def set_engine(engine=Arg(choices=search_engines)):
	pass


@subcmd
def db():
	pass


@subcmd(parent='db')
def clear():
	pass


@subcmd(parent='db clear')
def all():
	pass

@subcmd(parent='db clear')
def instance(id):
	pass


@subcmd
def total(a, b, c, floating_point=False):
	pass


def common(username='test'):
	pass

@subcmd(add=[common])
def userpass():
	pass

@subcmd(add=[common])
def userinfo():
	pass

