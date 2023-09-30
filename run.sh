#!/bin/bash
pushd `dirname ${BASH_SOURCE[0]}` > /dev/null; HERE=`pwd`; popd > /dev/null
cd $HERE

pycmd="python"
[[ -z "$VIRTUAL_ENV" ]] && pycmd="poetry run python"

$pycmd -m dungeon.main
