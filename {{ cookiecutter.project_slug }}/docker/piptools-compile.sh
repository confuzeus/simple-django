#!/bin/bash

set -e

pip-compile --upgrade --generate-hashes --output-file base.txt base.in
pip-compile --upgrade --generate-hashes --output-file dev.txt dev.in
pip-compile --upgrade --generate-hashes --output-file prod.txt prod.in