# Salt Server Parser

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GitHub release](https://img.shields.io/github/release/hatamiarash7/Salt-Server-Parser.svg)](https://GitHub.com/hatamiarash7/Salt-Server-Parser/releases/) [![Pylint](https://github.com/hatamiarash7/Salt-Server-Parser/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/hatamiarash7/Salt-Server-Parser/actions/workflows/pylint.yml) [![CodeQL](https://github.com/hatamiarash7/Salt-Server-Parser/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/hatamiarash7/Salt-Server-Parser/actions/workflows/codeql-analysis.yml)

Generate SSH config from Salt server lists

## Requirements

- Python 3.9+

## How to use

It's your `servers.sls` file:

```salt
servers:
    lab-1001:
        main_ip: 1.2.3.4
        ...
        ...
    lab-1002:
        main_ip: 4.5.6.7
        ...
        ...
    ...
    ...

```

> **Note**: Add/remove extra info from `main.py` file. For example `IdentityFile`, `IdentityAgent`, etc

Run:

```bash
python main.py <servers.sls> <output> <ssh port> <ssh user> <mode>
```

## Example

```bash
python main.py /Salt/pillar/dev/servers.sls out.txt 22 arash Staging
```

## Output

```text
#------- Staging Servers ------#

Host lab-1001
    HostName 1.2.3.4
    Port 22
    User user
    IdentitiesOnly yes
    IdentityAgent ~/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub

Host lab-1002
    HostName 4.5.6.7
    Port 22
    User user
    IdentitiesOnly yes
    IdentityAgent ~/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub
```

Also you will have two another files:

- A `ip-list.json` file containing all IPs will be generated for further use. For example whitelist them in WireGuard, etc. See This project: [WireGuard-Config-Generator](https://github.com/hatamiarash7/WireGuard-Config-Generator)
- A `server-list.json` file containing all servers with their IP baed on `role`, `zone`, `provider` and `code`. There is an `other` key for unknown servers. You can Change `__create_list()` function to fit your needs.
