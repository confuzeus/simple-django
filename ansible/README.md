# Ansible Playbook for Ubuntu Web Application Server

This project contains an Ansible playbook to automate the provisioning and configuration of a secure Ubuntu server designed to host a Django web application. It leverages a containerized approach with Docker and uses Caddy as a reverse proxy with automatic HTTPS.

## Overview

The playbook is designed to be idempotent and modular. It automates everything from initial server hardening and package installation to the deployment of a full application stack. The goal is to create a repeatable, secure, and production-ready environment with minimal manual intervention.

The core application stack deployed by this playbook includes:

- **Django Application**: Running in a Docker container via Gunicorn.
- **Huey Worker**: A background task queue worker running in a separate container.
- **Caddy**: A modern web server that acts as a reverse proxy and automatically provisions and renews SSL/TLS certificates.
- **Litestream**: Provides real-time, continuous backups of the application's SQLite database to a Backblaze B2 bucket for disaster recovery.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following software installed on your local machine (from which you will run Ansible):

- Ansible
- [Just](https://github.com/casey/just) - a command runner

### Setup Instructions

1.  **Install Ansible Collections:**
    This project requires several Ansible collections. You can install them using the provided `just` command:

    ```sh
    just collections
    ```

2.  **Configure Inventory:**
    Edit the `hosts` file to include the hostname or IP address of the server you wish to provision.

3.  **Configure Variables:**
    All server-specific and sensitive variables are managed in `group_vars/all.yml`. This file is encrypted using Ansible Vault. To configure your variables:

    - Decrypt the file: `just decrypt`
    - Edit `group_vars/all.yml` to set your hostname, admin user, SMTP credentials, Backblaze keys, etc.
    - Re-encrypt the file: `just encrypt`

4.  **Provide Passwords:**
    - **Vault Password:** Create a file named `.vault` in the project root and place your Ansible Vault password in it.
    - **Sudo Password:** Create a file named `.become` in the project root and place the sudo password for the remote user in it.

## Ansible Roles

This playbook is organized into several roles, each responsible for a specific aspect of the server configuration.

| Role       | Description                                                                                                                                                                                                                                                |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `packages` | Ensures all necessary system packages (like `ufw`, `fail2ban`, `msmtp`) are installed and that the system is fully up-to-date.                                                                                                                             |
| `basics`   | Handles fundamental server setup, including setting the hostname, creating an admin user with sudo privileges, and configuring SSH key access. It also configures a daily systemd timer to email administrators about pending package updates.             |
| `security` | Hardens the server by configuring UFW (Uncomplicated Firewall) to block incoming traffic by default, setting up Fail2Ban to prevent SSH brute-force attacks, and applying a secure SSH configuration that disables root login and password authentication. |
| `django`   | Deploys the Django application stack using Docker Compose. It sets up the required users, directories, and configuration files for the web, worker, Caddy, and Litestream services.                                                                        |

## Usage

A `justfile` is included to provide simple commands for running the playbook and performing common tasks.

- **Run the full playbook:**
  This will execute all roles except for `maintenance`.

  ```sh
  just
  ```

- **Run a specific part of the playbook:**
  You can run a specific role by using its tag.

  ```sh
  # Run only the security role
  just security

  # Run only the Django application deployment
  just django
  ```

- **Available Commands:**
  - `just packages`: Update and install system packages.
  - `just basics`: Apply basic server configuration.
  - `just security`: Apply security hardening configurations.
  - `just django`: Deploy or update the Django application stack.
  - `just maintenance`: Run maintenance tasks.
  - `just reboot`: Reboot the server.

### Secrets Management

Sensitive data like API keys and passwords should be stored in `group_vars/all.yml` and `roles/django/files/appconfig.env`. These files are encrypted using Ansible Vault.

- **To encrypt the files after editing:**

  ```sh
  just encrypt
  ```

- **To decrypt the files for editing:**
  ```sh
  just decrypt
  ```
