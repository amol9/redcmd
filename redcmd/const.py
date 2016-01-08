from os.path import join as joinpath, expanduser
from os import getuid

from redlib.system.common import is_linux


subcmd_attr 		= '__subcmd__'
maincmd_attr 		= '__maincmd__'
subcmd_dest_suffix 	= 'subcommand'

prog			= 'program'
description		= 'A command line utility.'
version			= '0.0.0'

user_home		= expanduser('~')
data_dir_name		= '.redcmd'

data_dir		= None
autocomp_dir		= None
script_dir		= None
root_data_dir		= joinpath('/var/local', data_dir_name)

if is_linux() and getuid() == 0:
	data_dir		= root_data_dir
	autocomp_dir		= joinpath(data_dir, 'autocomp')
	script_dir		= joinpath(user_home, 'scripts')
else:
	data_dir		= joinpath(user_home, data_dir_name)
	autocomp_dir		= joinpath(data_dir, 'autocomp')
	script_dir		= joinpath(data_dir, 'scripts')

internal_subcmd		= 'redcmdinternal'
prog_name		= 'redcmd'

autocomp_function	= '__redcmd_autocomp'

