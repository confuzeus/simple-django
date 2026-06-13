# basics

Part of the [`ansible/playbook.yml`](../../playbook.yml). Tag: `basics`

This role handles foundational server setup including:

- **Sudo group** — ensures the `sudo` group exists
- **Admin user** — creates the admin user (configurable via `admin_username`), sets password hash, grants supplementary groups (`admin_user_groups`), and configures SSH access via `admin_authorized_keys`
- **Sudoers** — templates `/etc/sudoers.d/admin` to grant the admin user passwordless sudo
- **msmtp** — templates `/etc/msmtprc` with SMTP credentials from `group_vars/all.yml` for sending system emails (used by the update notifier below)
- **Package update notifications** — deploys the `update-notifier` script as a systemd service+timer to check for package updates and notify the configured recipient via email

## Required variables

See [`ansible/group_vars/all.yml`](../../group_vars/all.yml) for all variables. Key ones for this role:

| Variable                         | Description                                     |
| -------------------------------- | ----------------------------------------------- |
| `admin_username`                 | Name of the admin user to create                |
| `admin_password_hash`            | Password hash for the admin user                |
| `admin_user_groups`              | List of supplementary groups for the admin user |
| `smtp_host`                      | SMTP server hostname                            |
| `smtp_port`                      | SMTP server port                                |
| `smtp_user`                      | SMTP username                                   |
| `smtp_password`                  | SMTP password                                   |
| `server_notifications_from_addr` | From address for notification emails            |
| `update_notifications_recipient` | Recipient address for update notifications      |

## Usage

```bash
ansible-playbook ansible/playbook.yml --tags basics -i <inventory>
```

To run only the basics role against a specific inventory, use the command above.
