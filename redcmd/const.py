from os.path import join as joinpath, expanduser


subcmd_attr 		= '__subcmd__'
maincmd_attr 		= '__maincmd__'
subcmd_dest_suffix 	= 'subcommand'

prog			= 'program'
description		= 'A command line utility.'
version			= '0.0.0'

user_home		= '~'
data_dir_name		= '.redcmd'
data_dir_path		= joinpath(expanduser(user_home), data_dir_name)
autocomp_dir_path	= joinpath(data_dir_path, 'autocomp')

internal_subcmd		= 'redcmdinternal'
prog_name		= 'redcmd'

