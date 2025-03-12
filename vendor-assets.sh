#!/bin/bash

set -e

export VENDORS_ROOT=node_modules

export STATIC_DEST=static

cp $VENDORS_ROOT/htmx.org/dist/htmx.min.js $STATIC_DEST/js/

unset VENDORS_ROOT
unset STATIC_DEST
