#!/bin/bash

set -e

echo

echo "What's your name?"

read name

echo "What's the name of the project?"

read project_name

echo "Project slug (No dashes):"

read project_slug

echo "What's your domain name?"

read domain_name

echo "What's your email?"

read email

find . \
    -type f \
    -not -path '*/venv/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/fonts/*' \
    -not -path '*pytest_cache*' \
    -not -path '*/static_collected/*' \
    -not -path '*git/*' \
    -not -name 'rename.sh' \
    -not -path '*/static/*' \
    -exec sed -i "s/Josh Michael Karamuth/$name/g" {} \;\
    -exec sed -i "s/Simple Django/$project_name/g" {} \;\
    -exec sed -i "s/example.com/$domain_name/g" {} \;\
    -exec sed -i "s/admin@$domain_name/$email/g" {} \;\
    -exec sed -i "s/simple_django/$project_slug/g" {} \; \
    -exec sed -i "s/simple-django/$project_slug/g" {} \;

mv simple_django/ $project_slug/
