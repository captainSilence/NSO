#!/usr/bin/env python

import socket
import sys
import tty
import termios
import paramiko
from paramiko.py3compat import u
import ncs
from _ncs import decrypt

debug = False

def get_credentials(root, device):
    authgrp = root.ncs__devices.authgroups.group[device.authgroup].default_map

    return (device.address, authgrp.remote_name, decrypt(authgrp.remote_password))


class IgnoreMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


def main():
    with ncs.maapi.Maapi() as m:
        m.install_crypto_keys()
        with ncs.maapi.Session(m, 'admin', 'ssh-context'):
            with m.start_read_trans() as t:
                root = ncs.maagic.get_root(t)

                while True:
                    print("q: exit")
                    print("d: enable paramiko debug")
                    devs = []
                    for device in root.ncs__devices.device:
                        devs.append(device)

                    for (idx, dev) in enumerate(devs):
                        print("{}: {}".format(idx, dev.name))

                    inp = input('# ')
                    if inp == 'q':
                        break
                    if inp == 'd':
                        print("enabling debug")
                        paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
                    try:
                        idx = int(inp)
                        if (idx >= 0) and (idx < len(devs)):
                            ssh_to(root, devs[idx])
                    except ValueError:
                        pass


def ssh_to(root, device):
    (host, user, pwd) = get_credentials(root, device)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(IgnoreMissingHostKeyPolicy())
    ssh.connect(host, username=user, password=pwd, allow_agent=False, look_for_keys=False)

    chan = ssh.invoke_shell()

    interactive_shell(chan)

    ssh.close()


def interactive_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        while True:
            read, _, _ = select.select([chan, sys.stdin], [], [])
            if chan in read:
                try:
                    data = u(chan.recv(1024))
                    if not data:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(data)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in read:
                data = sys.stdin.read(1)
                if not data:
                    break
                chan.send(data)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


if __name__ == "__main__":
    main()