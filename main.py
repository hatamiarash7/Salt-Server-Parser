"""
This script will parse pillar file and generate a list of all servers for SSH
"""

import sys
import json
from ruamel.yaml import YAML
from pyfiglet import Figlet
import toml
import subprocess
f = Figlet(font='standard')

inputFile = sys.argv[1]
output = sys.argv[2]
port = sys.argv[3]
user = sys.argv[4]
mode = sys.argv[5]

yaml = YAML(typ='safe')

print(f.renderText('SSH Config Generator'))

ips = []
servers_json = {}
servers_toml = {}


def _create_json(server, ip):
    """Create a json list of servers and IPs

    The default format is: role-zone-provider-code

    Args:
        server (string): The server name
        ip (string): The server IP
    """

    ips.append(ip + "/32")

    name = server.split('-')
    role = name[0]

    servers_json.update({'other': {}}) if 'other' not in servers_json else None

    if role in ['edge', 'monitoring', 'specto', 'prx']:
        servers_json.update({role: {}}) if role not in servers_json else None
        zone = name[1]
        provider = name[2]
        code = name[3]

        servers_json[role].update(
            {zone: {}}) if zone not in servers_json[role] else None
        servers_json[role][zone].update(
            {provider: {}}) if provider not in servers_json[role][zone] else None

        servers_json[role][zone][provider].update({code: ip})
    else:
        servers_json['other'].update({server: ip})


def _create_toml(server, ip):
    """Create a toml list of servers and IPs

    The default format is: role-zone-provider-code

    Args:
        server (string): The server name
        ip (string): The server IP
    """

    name = server.split('-')
    role = name[0]
    zone = name[1] if len(name) > 1 else 'a'
    provider = name[2] if len(name) > 2 else 'a'
    code = name[3] if len(name) > 3 else 'a'
    key = zone + '-' + provider + '-' + code

    servers_toml.update({role: {}}) if role not in servers_toml else None
    servers_toml[role].update(
        {key: {}}) if key not in servers_toml[role] else None
    servers_toml[role][key] = ip


def generate():
    print("--> Start")

    COUNTER = 0
    COUNTER_TINC = 0

    with (
        open(file=output, mode='w', encoding='UTF-8') as writer,
        open(file='ip-list.json', mode='w', encoding='UTF-8') as ip_list,
        open(file='server-list.json', mode='w', encoding='UTF-8') as server_json,
        open(file='server-list.toml', mode='w', encoding='UTF-8') as server_toml,
        open(file=inputFile, mode='r', encoding='UTF-8') as stream
    ):
        writer.write("############################################ " + mode +
                     " Servers ############################################\n\n")
        print("--> Load Salt file")
        out = yaml.load(stream)
        print("--> Writing data")
        identityAgentPath = subprocess.run(["gpgconf" ,"--list-dirs", "agent-ssh-socket"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(identityAgentPath)
        for server in out['servers']:
            ip = out['servers'][server]['main_ip']

            _create_json(server, ip)
            _create_toml(server, ip)

            writer.write("Host " + server + "\n")
            writer.write("\tHostName " + ip + "\n")
            writer.write("\tPort " + port + "\n")
            writer.write("\tUser " + user + "\n")
            writer.write("\tPubkeyAuthentication yes\n")
            writer.write("\tPreferredAuthentications publickey\n")
            writer.write("\tIdentitiesOnly yes\n")
            writer.write("\t" + identityAgentPath)
            writer.write("\tIdentityFile ~/.ssh/id_rsa_yubikey.pub\n")
            writer.write("\n")

            COUNTER = COUNTER+1

            if 'tinc_ip' in out['servers'][server]:
                tinc_ip = out['servers'][server]['tinc_ip']
                if len(tinc_ip) > 0:
                    writer.write("Host " + server + "-t\n")
                    writer.write("\tHostName " + tinc_ip + "\n")
                    writer.write("\tPort " + port + "\n")
                    writer.write("\tUser " + user + "\n")
                    writer.write("\tPubkeyAuthentication yes\n")
                    writer.write("\tPreferredAuthentications publickey\n")
                    writer.write("\tIdentitiesOnly yes\n")
                    writer.write("\t" + identityAgentPath)
                    writer.write("\tIdentityFile ~/.ssh/id_rsa_yubikey.pub\n")
                    writer.write("\n")

                    COUNTER_TINC = COUNTER_TINC+1

        json.dump(ips, ip_list)
        json.dump(servers_json, server_json)
        toml.dump(servers_toml, server_toml)

    print("--> " + str(COUNTER) + " servers added" +
          " ( " + str(COUNTER_TINC) + " with Tinc IP )")


if __name__ == "__main__":
    generate()
