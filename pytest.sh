#!/bin/bash
pushd `dirname ${BASH_SOURCE[0]}` > /dev/null; HERE=`pwd`; popd > /dev/null
cd $HERE

export PYTHONPATH=.

prefix=""
[[ -z "$VIRTUAL_ENV" ]] && prefix="poetry run "

# ${prefix}mypy dungeon lethal && ${prefix}pytest tests
${prefix}mypy dungeon && ${prefix}pytest tests
