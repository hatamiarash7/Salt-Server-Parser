"""
This script will parse pillar file and generate a list of all servers for SSH
"""

import sys
import json
from ruamel.yaml import YAML
from pyfiglet import Figlet

f = Figlet(font='standard')

inputFile = sys.argv[1]
output = sys.argv[2]
port = sys.argv[3]
user = sys.argv[4]
mode = sys.argv[5]

yaml = YAML(typ='safe')

print(f.renderText('SSH Config Generator'))
print("--> Start")

COUNTER = 0
COUNTER_TINC = 0
ips = []

with (
    open(file=output, mode='w', encoding='UTF-8') as writer,
    open(file='ip-list.json', mode='w', encoding='UTF-8') as ip_list,
    open(file=inputFile, mode='r', encoding='UTF-8') as stream
):
    writer.write("############################################ " + mode +
                 " Servers ############################################\n\n")
    print("--> Load Salt file")
    out = yaml.load(stream)
    print("--> Writing data")

    for server in out['servers']:
        ip = out['servers'][server]['main_ip']

        ips.append(ip + "/32")

        writer.write("Host " + server + "\n")
        writer.write("\tHostName " + ip + "\n")
        writer.write("\tPort " + port + "\n")
        writer.write("\tUser " + user + "\n")
        writer.write("\tPubkeyAuthentication yes\n")
        writer.write("\tPreferredAuthentications publickey\n")
        writer.write("\tIdentitiesOnly yes\n")
        writer.write(
            "\tIdentityAgent /Users/${USER}/.gnupg/S.gpg-agent.ssh\n")
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
                writer.write(
                    "\tIdentityAgent /run/user/1000/gnupg/S.gpg-agent.ssh\n")
                writer.write("\tIdentityFile ~/.ssh/id_rsa_yubikey.pub\n")
                writer.write("\n")
                
                COUNTER_TINC = COUNTER_TINC+1

    json.dump(ips, ip_list)

print("--> " + str(COUNTER) + " servers added" + " ( " + str(COUNTER_TINC) + " with Tinc IP )")
