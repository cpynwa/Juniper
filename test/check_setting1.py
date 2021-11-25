from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos import Device
import re
import os

# 장비 접속
dev = Device(host='211.45.116.132', user='eknow', password='Test1234')


# config 정보 수집
with StartShell(dev) as ss:
    configuration = ss.run("cli -c 'show configuration | display set | no-more'")[1]

with open("configuration.txt", "w") as file1:
    file1.write(configuration)

# os.system("cli -c 'show configuration | display set | no-more' > configuration.txt")

with open('configuration.txt', 'r') as file:
    data = file.read().replace('\n', '')

with open("configuration.txt", "r") as config:
    lines = config.readlines()

interface_config = [interface.strip("\n") for interface in lines if re.match(r'^set interfaces ', str(interface))]
ospf_config = [ospf.strip("\n") for ospf in lines if re.match(r'^set protocols ospf ', str(ospf))]
ospf3_config = [ospf3.strip("\n") for ospf3 in lines if re.match(r'^set protocols ospf3 ', str(ospf3))]
mpls_config = [mpls.strip("\n") for mpls in lines if re.match(r'^set protocols mpls ', str(mpls))]
ldp_config = [ldp.strip("\n") for ldp in lines if re.match(r'^set protocols ldp ', str(ldp))]

os.remove("configuration.txt")

def collect_interface_info(interface_config):
    interface_all_list = []
    interface_info_list = []
    interface_list = []

    for line in interface_config:
        interface_all_list.append(line.split()[2])

    for v in interface_all_list:

        if v not in interface_list:
            interface_list.append(v)

    for interface_idx in interface_list:
        physical = {
            "interface": "X",
            "ipv4": "X",
            "ipv6": "X",
            "description": "X",
            "hold_time_up": "X",
            "hold_time_down": "X",
            "mtu": "X",
            "ospf_area": "X",
            "ospf_type": "X",
            "ospf_bfd_minimum": "X",
            "ospf_bfd_multiplier": "X",
            "ospf_metric": "X",
            "ospf_ldp": "X",
            "mpls_set": "X",
            "ldp_set": "X",
            "ospf3_area": "X",
            "ospf3_type": "X",
            "ospf3_metric": "X",
        }

        logical = {
            "interface": "X",
            "ipv4": "X",
            "ipv6": "X",
            "description": "X",
            "hold_time_up": "X",
            "hold_time_down": "X",
            "mtu": "X",
            "ospf_area": "X",
            "ospf_type": "X",
            "ospf_bfd_minimum": "X",
            "ospf_bfd_multiplier": "X",
            "ospf_metric": "X",
            "ospf_ldp": "X",
            "mpls_set": "X",
            "ldp_set": "X",
            "ospf3_area": "X",
            "ospf3_type": "X",
            "ospf3_metric": "X",
        }
        for line in interface_config:

            if interface_idx == line.split()[2]:
                physical['interface'] = interface_idx

                if line.split()[3] == 'description':
                    physical['description'] = line.split()[4]

                elif line.split()[3] == 'mtu':
                    physical['mtu'] = line.split()[4]

                elif line.split()[3] == 'hold-time':

                    if line.split()[4] == 'up':
                        physical['hold_time_up'] = line.split()[5]

                    elif line.split()[4] == 'down':
                        physical['hold_time_down'] = line.split()[5]
                elif re.match(r'.*inet address.*', line):
                    logical["interface"] = line.split()[2] + '.' + line.split()[4]
                    logical["ipv4"] = line.split()[8]

                elif re.match(r'.*inet6 address.*', line):
                    logical["interface"] = line.split()[2] + '.' + line.split()[4]
                    logical["ipv6"] = line.split()[8]

                else:
                    continue

            else:
                continue
        interface_info_list.append(physical)
        interface_info_list.append(logical)
    return interface_info_list

def collect_ospf_info(ospf_config):
    ospf_all_list = []
    ospf_info_list = []
    ospf_list = []

    for line in ospf_config:
        ospf_all_list.append(line.split()[6])

    for v in ospf_all_list:

        if v not in ospf_list:
            ospf_list.append(v)


    for ospf_idx in ospf_list:
        logical = {
            "interface": "X",
            "ipv4": "X",
            "ipv6": "X",
            "description": "X",
            "hold_time_up": "X",
            "hold_time_down": "X",
            "mtu": "X",
            "ospf_area": "X",
            "ospf_type": "X",
            "ospf_bfd_minimum": "X",
            "ospf_bfd_multiplier": "X",
            "ospf_metric": "X",
            "ospf_ldp": "X",
            "mpls_set": "X",
            "ldp_set": "X",
            "ospf3_area": "X",
            "ospf3_type": "X",
            "ospf3_metric": "X",
        }

        for line in ospf_config:

            if ospf_idx == line.split()[6]:
                logical['interface'] = ospf_idx
                logical['ospf_area'] = line.split()[4]

                if line.split()[7] == 'interface-type':
                    logical['ospf_type'] = line.split()[8]

                elif line.split()[7] == 'passive':
                    logical['ospf_type'] = 'passive'

                elif line.split()[7] == 'ldp-synchronization':
                    logical['ospf_ldp'] = 'ldp_sync'

                elif line.split()[7] == 'metric':
                    logical['ospf_metric'] = line.split()[8]

                elif re.match(r'.*bfd-liveness-detection minimum-interval.*', line):
                    logical['ospf_bfd_minimum'] = line.split()[9]

                elif re.match(r'.*bfd-liveness-detection multiplier.*', line):
                    logical['ospf_bfd_multiplier'] = line.split()[9]

            else:
                continue

        ospf_info_list.append(logical)

    return ospf_info_list

def collect_ospf3_info(ospf3_config):
    ospf3_all_list = []
    ospf3_info_list = []
    ospf3_list = []

    for line in ospf3_config:
        ospf3_all_list.append(line.split()[6])

    for v in ospf3_all_list:

        if v not in ospf3_list:
            ospf3_list.append(v)

    for ospf3_idx in ospf3_list:
        logical = {
            "interface": "X",
            "ipv4": "X",
            "ipv6": "X",
            "description": "X",
            "hold_time_up": "X",
            "hold_time_down": "X",
            "mtu": "X",
            "ospf_area": "X",
            "ospf_type": "X",
            "ospf_bfd_minimum": "X",
            "ospf_bfd_multiplier": "X",
            "ospf_metric": "X",
            "ospf_ldp": "X",
            "mpls_set": "X",
            "ldp_set": "X",
            "ospf3_area": "X",
            "ospf3_type": "X",
            "ospf3_metric": "X",
            # "ospf3_bfd_minimum": "",
            # "ospf3_bfd_multiplier": "",
            # "ospf3_ldp": "",
        }

        for line in ospf3_config:

            if ospf3_idx == line.split()[6]:
                logical['interface'] = ospf3_idx
                logical['ospf3_area'] = line.split()[4]

                if line.split()[7] == 'interface-type':
                    logical['ospf3_type'] = line.split()[8]

                elif line.split()[7] == 'passive':
                    logical['ospf3_type'] = 'passive'

                elif line.split()[7] == 'metric':
                    logical['ospf3_metric'] = line.split()[8]

                # elif line.split()[7] == 'ldp-synchronization':
                #     logical['ospf3_ldp'] = 'ldp_sync'
                #
                # elif re.match(r'.*bfd-liveness-detection minimum-interval.*', line):
                #     logical['ospf3_bfd_minimum'] = line.split()[9]
                #
                # elif re.match(r'.*bfd-liveness-detection multiplier.*', line):
                #     logical['ospf3_bfd_multiplier'] = line.split()[9]

            else:
                continue

        ospf3_info_list.append(logical)

    return ospf3_info_list


def collect_ldp_info(ldp_config):
    ldp_all_list = []
    ldp_info_list = []
    ldp_list = []

    for line in ldp_config:
        ldp_all_list.append(line.split()[4])

    for v in ldp_all_list:

        if v not in ldp_list:
            ldp_list.append(v)


    for ldp_idx in ldp_list:
        logical = {
            "interface": "X",
            "ipv4": "X",
            "ipv6": "X",
            "description": "X",
            "hold_time_up": "X",
            "hold_time_down": "X",
            "mtu": "X",
            "ospf_area": "X",
            "ospf_type": "X",
            "ospf_bfd_minimum": "X",
            "ospf_bfd_multiplier": "X",
            "ospf_metric": "X",
            "ospf_ldp": "X",
            "mpls_set": "X",
            "ldp_set": "X",
            "ospf3_area": "X",
            "ospf3_type": "X",
            "ospf3_metric": "X",
        }

        for line in ldp_config:

            if ldp_idx == line.split()[4]:
                logical['interface'] = ldp_idx
                logical['ldp_set'] = "O"

            else:
                continue

        ldp_info_list.append(logical)

    return ldp_info_list


def collect_mpls_info(mpls_config):
    mpls_all_list = []
    mpls_info_list = []
    mpls_list = []

    for line in mpls_config:
        mpls_all_list.append(line.split()[4])

    for v in mpls_all_list:

        if v not in mpls_list:
            mpls_list.append(v)


    for mpls_idx in mpls_list:
        logical = {
            "interface": "X",
            "ipv4": "X",
            "ipv6": "X",
            "description": "X",
            "hold_time_up": "X",
            "hold_time_down": "X",
            "mtu": "X",
            "ospf_area": "X",
            "ospf_type": "X",
            "ospf_bfd_minimum": "X",
            "ospf_bfd_multiplier": "X",
            "ospf_metric": "X",
            "ospf_ldp": "X",
            "mpls_set": "X",
            "ldp_set": "X",
            "ospf3_area": "X",
            "ospf3_type": "X",
            "ospf3_metric": "X",
        }

        for line in mpls_config:

            if mpls_idx == line.split()[4]:
                logical['interface'] = mpls_idx
                logical['mpls_set'] = "O"

            else:
                continue

        mpls_info_list.append(logical)

    return mpls_info_list


def main(interface_config, ospf_config, mpls_config, ldp_config, ospf3_config):
    interface = collect_interface_info(interface_config)
    ospf = collect_ospf_info(ospf_config)
    mpls = collect_mpls_info(mpls_config)
    ldp = collect_ldp_info(ldp_config)
    ospf3 = collect_ospf3_info(ospf3_config)


    for i in range(len(interface)):

        for j in range(len(ospf)):

            if interface[i]["interface"] == ospf[j]["interface"]:
                interface[i].update(ospf[j])
                ospf.remove(ospf[j])
                break

            else:
                continue

        for j in range(len(mpls)):
            if interface[i]["interface"] == mpls[j]["interface"]:
                interface[i].update(mpls[j])
                mpls.remove(mpls[j])
                break
            else:
                interface[i]["mpls_set"] = "X"

        for j in range(len(ldp)):
            if interface[i]["interface"] == ldp[j]["interface"]:
                interface[i].update(ldp[j])
                ldp.remove(ldp[j])
                break
            else:
                interface[i]["ldp_set"] = "X"
        for j in range(len(ospf3)):
            if interface[i]["interface"] == ospf3[j]["interface"]:
                interface[i].update(ospf3[j])
                ospf3.remove(ospf3[j])
                break
            else:
                interface[i]["ospf3_area"] = "X"
                interface[i]["ospf3_type"] = "X"
                interface[i]["ospf3_metric"] = "X"

    for i in range(len(ospf)):
        interface.append(ospf[i])
    for i in range(len(mpls)):
        interface.append(mpls[i])
    for i in range(len(ldp)):
        interface.append(ldp[i])
    for i in range(len(ospf3)):
        interface.append(ospf3[i])

    # 출력
    print(
        "interface".ljust(14) +
        "ipv4".ljust(18) +
        "ipv6".ljust(18) +
        "description".ljust(18) +
        "h_up".ljust(5) +
        "h_dn".ljust(5) +
        "mtu".ljust(5) +
        "area".ljust(9) +
        "type".ljust(9) +
        "bfd_min".ljust(8) +
        "bfd_mul".ljust(8) +
        "cost".ljust(6) +
        "ldp_syn".ljust(10) +
        "mpls".ljust(5) +
        "ldp".ljust(4) +
        "o3_area".ljust(9) +
        "o3_type".ljust(8) +
        "o3_cost"
        )

    for i in range(len(interface)):
        print(
            str(interface[i]["interface"]).ljust(14) +
            str(interface[i]["ipv4"]).ljust(18) +
            str(interface[i]["ipv6"]).ljust(18) +
            str(interface[i]["description"]).ljust(18) +
            str(interface[i]["hold_time_up"]).ljust(5) +
            str(interface[i]["hold_time_down"]).ljust(5) +
            str(interface[i]["mtu"]).ljust(5) +
            str(interface[i]["ospf_area"]).ljust(9)+
            str(interface[i]["ospf_type"]).ljust(9)+
            str(interface[i]["ospf_bfd_minimum"]).ljust(8)+
            str(interface[i]["ospf_bfd_multiplier"]).ljust(8)+
            str(interface[i]["ospf_metric"]).ljust(6) +
            str(interface[i]["ospf_ldp"]).ljust(10) +
            str(interface[i]["mpls_set"]).ljust(5) +
            str(interface[i]["ldp_set"]).ljust(4) +
            str(interface[i]["ospf3_area"]).ljust(9) +
            str(interface[i]["ospf3_type"]).ljust(8) +
            str(interface[i]["ospf3_metric"])
    )

if __name__ == '__main__':
    main(interface_config, ospf_config, mpls_config, ldp_config, ospf3_config)
