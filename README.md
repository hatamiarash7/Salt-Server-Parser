# Salt Server Parser

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Generate SSH config from Salt server lists

## How to use

Add/remove extra info from `parse.py` file. For example `IdentityFile`, `IdentityAgent`, etc and run:

```bash
python parse.py <servers.sls> <output> <ssh port> <ssh user> <mode>
```

## Example

```bash
python parse.py /Salt/pillar/dev/servers.sls out.txt 2219 hatamiarash7 Staging
```

## Output

```text
#------- Staging Servers ------#

Host lab-fra-hzr-1001
    HostName 1.2.3.4
    Port 2219
    User hatamiarash7
    IdentitiesOnly yes
    IdentityAgent ~/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub

Host lab-thr-at-1002
    HostName 4.5.6.7
    Port 2219
    User hatamiarash7
    IdentitiesOnly yes
    IdentityAgent ~/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub
```

Also, a `ip-list.json` file will be generated for further use containing all IPs in JSON format. For example whitelist them in WireGuard, etc. See This project: [WireGuard-Config-Generator](https://github.com/hatamiarash7/WireGuard-Config-Generator)
