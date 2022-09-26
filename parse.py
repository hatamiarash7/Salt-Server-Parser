import sys
import json
from ruamel.yaml import YAML
from pyfiglet import Figlet

f = Figlet(font='standard')

input = sys.argv[1]
output = sys.argv[2]
port = sys.argv[3]
user = sys.argv[4]
mode = sys.argv[5]

yaml = YAML(typ='safe')

print(f.renderText('SSH Config Generator'))
print("--> Start")

count = 0
ips = []

with (open(output, 'w') as writer, open('ip-list.json', 'w') as ip_list, open(input, 'r') as stream):
    writer.write("#---------------------------------- " + mode +
                 " Servers ----------------------------------#\n\n")
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
        count = count+1

    json.dump(ips, ip_list)

print("--> " + str(count) + " servers added")

'''
Sample:

HOST <NAME>
    HostName <IP>
    Port <PORT>
    User <USER>
    PubkeyAuthentication yes
    PreferredAuthentications publickey
    IdentitiesOnly yes
    IdentityAgent /Users/${USER}/.gnupg/S.gpg-agent.ssh
    IdentityFile ~/.ssh/id_rsa_yubikey.pub
'''
