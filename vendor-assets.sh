#!/bin/bash

set -e

export VENDORS_ROOT=node_modules

export STATIC_DEST=static

cp $VENDORS_ROOT/bootstrap-icons/bootstrap-icons.svg $STATIC_DEST/images/
cp $VENDORS_ROOT/smooth-scroll/dist/smooth-scroll.polyfills.js $STATIC_DEST/js/

unset VENDORS_ROOT
unset STATIC_DEST
