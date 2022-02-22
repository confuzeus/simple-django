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
cp appconfig.example.ini appconfig.ini
```

Edit the file and change all the variables to your liking.

Bootstrap the project with make:

```shell
make
```
