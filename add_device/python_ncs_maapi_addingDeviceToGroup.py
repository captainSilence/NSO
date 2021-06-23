import ncs
from inspect import getmembers, isfunction


# with ncs.maapi.single_read_trans('admin', 'python', groups=['ncsadmin']) as t:
#     root = ncs.maagic.get_root(t)
#     devicelist = root.devices.device
#     print(root.devices.device_group)
#     print(dir(root.devices.device_group))
#     junOS = []
#     for device in devicelist:
#        # print(device.config.ios__cached_show.version.model)
#         dev_ned = device.device_type.netconf.ned_id
#         if dev_ned == "juniper-junos-nc-4.6:juniper-junos-nc-4.6":
#             print("Adding device: " + device.name)
#             junOS.append(device.name)

#     print(junOS)

# with ncs.maapi.single_write_trans('admin', 'python', groups=['ncsadmin']) as t:
#     root = ncs.maagic.get_root(t)
#     for box in root.devices.device:
#         print(box.name,": ", box.device_type.cli.ned_id)


# # add devices to group
# with ncs.maapi.single_write_trans('admin', 'python', groups=['ncsadmin']) as t:
#     root = ncs.maagic.get_root(t)
#     new_group = root.devices.device_group.create('test2')
#     new_group.device_name = ['ASR-9010-A', 'ASR-9904-A']
#     t.apply()


with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'python'):
            with m.start_write_trans() as t:
               

                # Get a reference to the device list
                root = ncs.maagic.get_root(t)
                device_list = root.devices.device
                alu_omniswitch, alu_sr, arris_cmts, casa, ciena, cisco_ios, cisco_iosXR, junOS = ([] for i in range(8))
                

                for device in device_list:
                    # print(device.config.ios__cached_show.version.model)
                    # print(device.device_type.cli.ned_id)
                    if device.device_type.netconf.ned_id is None:
                        # print("false")
                        dev_ned = device.device_type.cli.ned_id
                    else:
                        dev_ned = device.device_type.netconf.ned_id
                    
                    # print("####" + dev_ned + "####")

                    if dev_ned == "juniper-junos-nc-4.6:juniper-junos-nc-4.6":
                        print("Adding juniper device to the array: " + device.name)
                        junOS.append(device.name)
                    elif dev_ned == "alu-omniswitch-6k-cli-2.3:alu-omniswitch-6k-cli-2.3":
                        print("Adding alu_omniswitch device to the array: " + device.name)
                        alu_omniswitch.append(device.name)
                    elif dev_ned == "alu-sr-cli-8.13:alu-sr-cli-8.13":
                        print("Adding alu_sr device to the array: " + device.name)
                        alu_sr.append(device.name)
                    elif dev_ned == "arris-cmts-cli-1.2:arris-cmts-cli-1.2":
                        print("Adding arris_cmts device to the array: " + device.name)
                        arris_cmts.append(device.name)
                    elif dev_ned == "casa-ccap-cli-1.2:casa-ccap-cli-1.2":
                        print("Adding casa device to the array: " + device.name)
                        casa.append(device.name)
                    elif dev_ned == "ciena-acos-cli-6.3:ciena-acos-cli-6.3":
                        print("Adding ciena device to the array: " + device.name)
                        ciena.append(device.name)
                    elif dev_ned == "cisco-ios-cli-6.69:cisco-ios-cli-6.69":
                        print("Adding cisco_ios device to the array: " + device.name)
                        cisco_ios.append(device.name)
                    elif dev_ned == "cisco-iosxr-cli-7.33:cisco-iosxr-cli-7.33":
                        print("Adding cisco_iosXR device: " + device.name)
                        cisco_iosXR.append(device.name)
                    else:
                        print("NED error for device: " + device.name)


                print('\n' * 2)
                print(junOS)
                print(alu_omniswitch)
                print(arris_cmts)
                print(casa)
                print(ciena)
                print(cisco_ios)
                print(cisco_iosXR)
                print('\n' * 2)


                junOS_group = root.devices.device_group.create('junOS')
                print("Creating junOS device group")
                junOS_group.device_name = junOS
                print("junOS devices added\n")

                alu_omniswitch_group = root.devices.device_group.create('alu_omniswitch')
                print("Creating alu_omniswitch device group")
                alu_omniswitch_group.device_name = alu_omniswitch
                print("alu_omniswitch devices added\n")

                arris_cmts_group = root.devices.device_group.create('arris_cmts')
                print("Creating arris_cmts device group")
                arris_cmts_group.device_name = arris_cmts
                print("arris_cmts devices added\n")

                casa_group = root.devices.device_group.create('casa')
                print("Creating casa device group")
                casa_group.device_name = casa
                print("casa devices added\n")

                ciena_group = root.devices.device_group.create('ciena')
                print("Creating ciena device group")
                ciena_group.device_name = ciena
                print("ciena devices added\n")

                cisco_ios_group = root.devices.device_group.create('cisco_ios')
                print("Creating cisco_ios device group")
                cisco_ios_group.device_name = cisco_ios
                print("cisco_ios devices added\n")

                cisco_iosXR_group = root.devices.device_group.create('cisco_iosXR')
                print("Creating cisco_iosXR device group")
                cisco_iosXR_group.device_name = cisco_iosXR
                print("cisco_iosXR devices added\n")

                t.apply()

                # device_group_list = root.devices.device_group['JunOS'].device_name
                # for group_device in device_group_list:
                #     print(group_device)

                