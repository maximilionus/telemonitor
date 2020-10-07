#!/bin/sh
cd "$(dirname "$0")" # Change workdir to shell script location
cd ../../../..       # Change workdir to the root of Telemonitor project

# Startup command.
# Modify it if you have more than one python version installed on your system.
# Example for python3.7:
#     python3.7 -m poetry run telem --no-color
poetry run telem --no-color
