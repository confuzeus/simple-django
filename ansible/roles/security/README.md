# security

Part of the [`ansible/playbook.yml`](../../playbook.yml). Tag: `security`

This role hardens a server's security posture by configuring SSH, the firewall, and fail2ban.

## What it does

- **SSH host keys** — generates (or regenerates on change) ED25519 and RSA 4096-bit host keys using `community.crypto.openssh_keypair` with `regenerate: full_idempotence`
- **Hardened sshd** — templates [`templates/sshd_config`](templates/sshd_config) to `/etc/ssh/sshd_config.d/custom.conf` with restrictive key exchange, cipher, and MAC algorithms, disabled root login, disabled password authentication, disabled agent forwarding, X11 forwarding, and compression, and restricts access to the admin user (`AllowUsers {{ admin_username }}`)
- **UFW firewall** — defaults to deny incoming / allow outgoing, then opens ports from the `firewall_open_ports` list (default: 22, 80, 443)
- **Fail2ban** — deploys [`files/sshd_jail.conf`](files/sshd_jail.conf) to `/etc/fail2ban/jail.d/sshd.conf` enabling the sshd jail on port 22

## Handlers

- **Reload sshd** — runs `systemctl reload ssh` after sshd config changes
- **Reload and enable firewall** — enables UFW after port rule changes

## Required variables

See [`ansible/group_vars/all.yml`](../../group_vars/all.yml) for all variables. Key ones for this role:

| Variable               | Description                              |
| ---------------------- | ---------------------------------------- |
| `admin_username`       | SSH user allowed by `AllowUsers`         |
| `firewall_open_ports`  | List of ports to open in the firewall    |

## Usage

```bash
ansible-playbook ansible/playbook.yml --tags security -i <inventory>
```
