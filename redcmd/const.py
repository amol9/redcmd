from os.path import join as joinpath, expanduser


subcmd_attr 		= '__subcmd__'
maincmd_attr 		= '__maincmd__'
subcmd_dest_suffix 	= 'subcommand'

prog			= 'program'
description		= 'A command line utility.'
version			= '0.0.0'

data_dir_name		= '.redcmd'
data_dir_path		= joinpath(expanduser('~'), data_dir_name)

internal_subcmd		= 'redcmdinternal'

