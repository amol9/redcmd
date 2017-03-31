from os.path import join as joinpath, dirname

from .. import const


ve = const.virtual_env


class bash:
    etc_dir = "/etc" if not ve else joinpath(const.virtual_env_root, "etc")
    
    profile_d_file 		= joinpath(etc_dir, "profile.d", "redcmd_autocomp.sh")
    bash_completion_d_dir	= joinpath(etc_dir, "bash_completion.d")
    user_bashrc_file	        = joinpath(const.user_home, ".bashrc")
    system_bashrc_file	        = joinpath(etc_dir, "bash.bashrc")

    id_prefix		= '__redcmd_autocomp_'
    user_script_file	= joinpath(const.script_dir, 'autocomp_func.sh')
    user_cmdlist_file	= joinpath(const.script_dir, 'autocomp_list.sh')

    script_template_file	= joinpath(dirname(__file__), 'scripts', 'bash_autocomp_function.sh')
    template_func_name	        = '_redcmd_autocomp_function'
    shebang			= '#!/bin/bash'

