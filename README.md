# Salt Server Parser

Generate SSH config from Salt server lists

## Usage

Add/remove extra info from `parse.py` file. For example `IdentityFile`, `IdentityAgent`, etc and run:

```bash
py parse.py <servers.sls> <output> <ssh port> <ssh user> <mode>
```

## Example

```bash
python parse.py /Salt/pillar/dev/servers.sls out.txt 2219 hatamiarash7 Staging
```

## Output

```text
#------- Staging Servers ------#

Host lab-edge-fra-hzr-1001
    HostName 1.2.3.4
    Port 2219
    User hatamiarash7
    IdentitiesOnly yes
    IdentityAgent ~/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub

Host lab-edge-thr-at-1002
    HostName 4.5.6.7
    Port 2219
    User hatamiarash7
    IdentitiesOnly yes
    IdentityAgent ~/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub
```
