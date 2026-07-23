#!/bin/bash
set -e

echo "=== Simple Django Project Setup ==="
echo

if [ ! -f appconfig.env ]; then
    echo "Creating appconfig.env from example..."
    cp appconfig.example.env appconfig.env

    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    sed -i "s|DJANGO_SECRET_KEY=secret|DJANGO_SECRET_KEY=$SECRET_KEY|" appconfig.env
    echo "Generated a random secret key and set it in appconfig.env."
else
    echo "appconfig.env already exists, skipping."
fi
echo

echo "Now we'll personalize the project for you."
./rename.sh

echo
read -p "Run 'just init' to initialize the project? [Y/n] " do_init
if [ "$do_init" != "n" ] && [ "$do_init" != "N" ]; then
    just init
fi

echo
echo "Done! Happy coding."
