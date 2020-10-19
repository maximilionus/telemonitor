#!/bin/bash

# This script works as a launcher for Telemonitor service
# It can start Telemonitor in 2 different ways
# Startup behaviour can be configured with passing input arguments
#
# Allowed input arguments:
# $1:
#    poetry - (default) launch Telemonitor with poetry
#    venv - launch Telemonitor with python virtual environment
# $2:
#    "path_to_venv" - (optional) !only if [ $1 == venv ]!
#                     absolute or relative path to python virtual environment location

startup_arg=$1
[ -z $startup_arg ] && startup_arg="poetry"

cd "$(dirname "$0")"
cd ../../../..

if [ $startup_arg == "poetry" ]; then
    poetry run telemonitor --no-color
elif [ $startup_arg == "venv" ]; then
    if [ -n "$2" ]; then
        source "$2"
        python -m telemonitor --no-color
    else
        echo "Virtual environment not stated"
    fi
else
    echo "Wrong input arguments"
fi
