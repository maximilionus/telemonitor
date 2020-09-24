#!/bin/sh
cd "$(dirname "$0")" # Change workdir to shell script location
cd ../../../..       # Change workdir to the root of Telemonitor project
poetry run telem
