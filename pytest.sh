#!/bin/bash
pushd `dirname ${BASH_SOURCE[0]}` > /dev/null; HERE=`pwd`; popd > /dev/null
cd $HERE

export PYTHONPATH=.

prefix=""
[[ -z "$VIRTUAL_ENV" ]] && prefix="poetry run "

set -e
if [ -z "SKIP_MYPY" ]; then
  ${prefix}mypy dungeon lethal 
fi
${prefix}pytest tests
