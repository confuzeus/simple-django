# django

Ansible role for setting up a Django application server with SQLite and Litestream replication.

## Requirements

- Ansible 2.10+
- `ansible.builtin` collection

## Role Variables

Variables are expected to be defined in `group_vars/all.yml`:

| Variable | Description | Example |
|---|---|---|
| `admin_username` | System admin user for config directory ownership | `me` |
| `backblaze_key_id` | Backblaze B2 access key ID for Litestream | `abcd` |
| `backblaze_app_key` | Backblaze B2 application key for Litestream | `efgh` |

The Litestream template (`templates/litestream.j2.yml`) also references `backblaze_key_id` and `backblaze_app_key` and should be customized with your S3-compatible endpoint and bucket path.

## Dependencies

None.

## Tasks

1. **Config directory** — Creates `/etc/simple_django` owned by the admin user.
2. **App user and group** — Creates a system group and user (`simple_django`, uid/gid 700) with no home directory.
3. **Data directory** — Creates `/var/simple_django` owned by the app user with restricted permissions (`u=rwx,g=rwx,o=`).
4. **Litestream config** — Templates `litestream.j2.yml` to `/etc/clarohq/litestream.yml`.
5. **DB restore script** — Copies `files/restore-db.sh` to `/root/restore-db.sh` as an executable root-only script.

## Usage

```sh
ansible-playbook playbook.yml --tags django
```

Or include in a playbook:

```yaml
- hosts: all
  roles:
    - role: django
      tags: django
```

## Files

- `files/restore-db.sh` — Standalone script to restore the SQLite database from Litestream replicas using Docker.
