#!/bin/bash
pushd `dirname ${BASH_SOURCE[0]}` > /dev/null; HERE=`pwd`; popd > /dev/null
cd $HERE

export PYTHONPATH=.

if [ -z "$VIRTUAL_ENV" ]; then
  poetry run pytest
else
  pytest
fi
