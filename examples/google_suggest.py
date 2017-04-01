#!/home/amol/code/projects/redcmd/ve/redcmd_p2.7/bin/python

from redcmd.api import maincmd, CommandLine, completer as cmpl, arg, CommandLineError

@maincmd
def main(term=arg.Arg(completer=cmpl.GoogleSuggest())):
	'''List Google autocomplete suggestions.
        term: search term
	'''
        print('search term: %s'%term)


cmdline = CommandLine(prog='google_suggest.py')
try:
        cmdline.execute()
except CommandLineError as e:
        print(e)

