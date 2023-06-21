# Simple Django Project Template

This template contains everything you need to bootstrap a new Django project.

## Requirements

Install the following tools first.

1. [Poetry](https://python-poetry.org/)
2. [Docker](https://www.docker.com/)

## Quick start

Clone the project and clean up git.

Your can either delete .git or set the origin to your own repo:

```shell
git remote set-url origin <your-repo>
```

## Configuration

Copy the example app config file:

```shell
cp appconfig.example.env appconfig.env
```

Edit the file and change all the variables to your liking.

## Rename the project

Execute the script named `rename.sh` and it will ask you a bunch of
questions that will be used to baptise your new project.

## Start services

The docker-compose file services like database, caching, and mail testing
systems.

If you don't want to use Docker, you'll need to have these services running
on your own computer instead.

Start the containers like so:

```shell
docker-compose up -d
```

## Initialize project

Bootstrap the project with make:

```shell
make
```

Your project is now ready for you to ship features.

## License and Copyright

License is MIT

Copyright 2022 Josh Michael Karamuth
