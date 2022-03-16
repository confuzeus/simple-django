# Simple Django Project Template

This template contains everything you need to bootstrap a new Django project.

## Quick start

Clone the project and clean up git.

Your can either delete .git or set the origin to your own repo:

```shell
git remote set-url origin <your-repo>
```

Create and activate a virtual environment:

```shell
virtualenv venv
source venv/bin/activate
```

Install `pip-tools`:

```shell
pip install pip-tools
```

Copy the example app config file:

```shell
cp appconfig.example.env appconfig.env
```

Edit the file and change all the variables to your liking.

You should also rename the project now unless you really
like the name *Simple Django*.

To rename, simply execute the script named `rename.py`.

Bootstrap the project with make:

```shell
make
```

## License and Copyright

License is MIT

Copyright 2022 Josh Michael Karamuth
