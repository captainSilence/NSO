# This module will add new device to the Cisco NSO
# Version: 1.0
# Author: Bizhou Duan
# Copyright 2021, Sparklight ®. All rights reserved
import argparse
import ncs


# Create parse function to define what arguments is required from user imput
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='device name', required=True)
    parser.add_argument('--address', help='device ip address', required=True)
    parser.add_argument('--ned_id', help='device NED ID', required=True)
    parser.add_argument('--ned_type', help='device NED type, cli/netconf', default='cli')
    parser.add_argument('--port', help='device port to connect', type=int, default=22)
    parser.add_argument('--desc', help='device description', default='default')
    parser.add_argument('--auth', help='device authgroup', default='default')
    parser.add_argument('--state', help='device admin state', default='unlocked')

    return parser.parse_args()


# main function
def main(args):
    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'python'):
            with m.start_write_trans() as t:
                print(f'Setting the device "{args.name}" configuration...')

                # Get a reference to the device list
                root = ncs.maagic.get_root(t)
                device_list = root.devices.device

                if args.name not in device_list:
                    device = device_list.create(args.name)
                    device.address = args.address
                    device.port = args.port
                    device.description = args.desc
                    device.authgroup = args.auth
                    dev_type = device.device_type.args.ned_type
                    dev_type.ned_id = args.ned_id
                    device.state.admin_state = args.state
                    print('Committing the device configuration...')
                    t.apply()
                    print('Device committed!')
                else:
                    print(f'Device "{args.name}" configuration already exists...')

            root = ncs.maagic.get_root(m)
            device = root.devices.device[args.name]
            print('Fetching SSH keys...')
            output = device.ssh.fetch_host_keys()
            print(f'Result: {output.result}')
            print('Syncing configuration...')
            output = device.sync_from()
            print(f'Result: {output.result}')
            if not output.result:

                print(f'Error: {output.info}')



if __name__ == '__main__':
    main(parse_args())