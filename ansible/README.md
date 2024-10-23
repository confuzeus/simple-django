# Ansible playbook

This playbook will configure an Ubuntu 24.04 server for hosting this Django project.

## Required ansible collections

You need to install the following modules:

1. community.general
2. community.crypto
3. community.docker

Install them with _ansible-galaxy_:

```shell
ansible-galaxy collection install <collection-name>
```

Or by running `just collections`.

## User Guide

1. Configure variables in _group_vars/all.yml_. See [this page](https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module) to learn how to
   generate the password hash for the admin user.

1. Open _roles/basics/files/admin_authorized_keys_. Add all the SSH public keys (one per line) that you will use to
   login as the admin user on this box.

1. Add environment variables for Django in _roles/django/files/appconfig.env_.

1. Open _roles/letsencrypt/files/certificates.sh_. Enter all the domain names for which you'd like to create SSL certificates.

1. Create virtual hosts files for your domains in _roles/nginx/files/_. For example, create a file called _mydomain.com.conf_. Use the same format as the provided _example.com.conf_. Just replace _example.com_ wherever it appears.

1. Open _roles/nginx/tasks/main.yml_. In the task _Copy virtual hosts_, edit the list below the _loop_ instruction.
   Remove _example.com.conf_ and add all the virtual host files you created above.

1. Create a file called _hosts_. Add the IP address(es) of the server(s) that will be configured.
   You can also use hostnames as defined in your ssh config instead of IP addresses.

1. Run the playbook by typing `just`.

## Encryption

If you run `just encrypt`, it will encrypt the variables file as well as the _appconfig.env_ so that you can safely
commit them to your Git repository.

First, you need to create a file called _.vault_ inside the _ansible_ directory. Put the password you want to use
in this file on a single line. This file is ignored by Git. After that, run `just encrypt` to encrypt everything.
Be sure to add and commit the changes to Git.

## Deployment

The _django_ role contains an example deployment scenario. Modify it to fit your needs.
