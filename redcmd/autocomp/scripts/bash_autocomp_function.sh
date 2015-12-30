#!/bin/bash

function _redcmd_autocomp_function()
{
	local cmd="${1##*/}"
	local word=${COMP_WORDS[COMP_CWORD]}
	local line=${COMP_LINE}

	COMPREPLY=($(redcmd autocomp gen "${line}" "${word}"))
}

export -f _redcmd_autocomp_function

