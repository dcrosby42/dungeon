#!/bin/bash
pushd `dirname ${BASH_SOURCE[0]}` > /dev/null; HERE=`pwd`; popd > /dev/null
cd $HERE

export PYTHONPATH=.

prefix=""
[[ -z "$VIRTUAL_ENV" ]] && prefix="poetry run "

echo Running mypy...
${prefix}mypy dungeon

echo Running pytest...
${prefix}pytest tests
