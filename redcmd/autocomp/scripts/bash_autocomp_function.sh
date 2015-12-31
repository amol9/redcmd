#!/bin/bash

function _redcmd_autocomp_function()
{
	local comp_word=${COMP_WORDS[COMP_CWORD]}
	local comp_line=${COMP_LINE}

	if [[ "$comp_word" == -* ]]
	then
		comp_word=" $comp_word"
	fi

	COMPREPLY=($(redcmd autocomp gen "${comp_line}" "$comp_word"))
}

export -f _redcmd_autocomp_function

