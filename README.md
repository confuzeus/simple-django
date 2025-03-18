# Simple Django Project Template

This template contains everything you need to bootstrap a new Django project.

## Features

- Styling with [TailwindCSS](https://tailwindcss.com)
- Javascript bundling and minifying with [esbuild](https://esbuild.github.io/)
- Modern Javascript stack with [htmx](https://htmx.org) and [AlpineJS](https://alpinejs.dev/)
- Live reload using [Browsersync](https://browsersync.io/)
- Project management with [uv](https://docs.astral.sh/uv/)
- Automated production server configuration with [Ansible](https://docs.ansible.com/).
- Automated [Docker](https://www.docker.com/) image deployment.

## Requirements

Install the following tools first.

1. [uv](https://astral.sh)
2. [pnpm](https://pnpm.io/)
3. [just](https://just.systems/man/en/introduction.html)
4. [Docker](https://www.docker.com/)

## Quick start

Clone the project and clean up git.

Your can either delete .git or set the origin to your own repo:

```shell
git remote set-url origin <your-repo>
```

### Configuration

Copy the example app config file:

```shell
cp appconfig.example.env appconfig.env
```

Edit the file and change all the variables to your liking.

### Rename the project

Execute the script named `rename.sh` and it will ask you a bunch of
questions that will be used to baptise your new project.

### Initialize project

Run `just` to bootstrap the project. See the _justfile_ for details.

Your project is now ready for you to ship features.

### Deployment

Executing the `deploy.py` script will do the following:

1. Build a Docker image containing the source code.
2. Optionally make an tar archive of this image, and upload it to your server.

Configure this deployment script by creating a `deploy.toml` file. See the `deploy.example.toml` file for details.

I wrote a post about [how to deploy a Django app without a container
registry](https://joshkaramuth.com/blog/deploy-container-no-registry/). Read it more details on how to setup your server to make this work.

Inside the ansible directory, you'll find the _django_ role where there's automation for this.

## License and Copyright

License is MIT

Copyright 2022 Josh Karamuth
