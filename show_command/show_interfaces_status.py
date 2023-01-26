from jnpr.junos import Device
import re

"""
test junos Ver = over 16.1R3
filename = show_interfaces_status.py
file location = /var/db/script/op/show_interfaces_status.py

- 적용 명령어
set system scripts language python
set system scripts op file show_interfaces_status.py

- 실행 명령어
root@MX960> op show_interfaces_status.py
"""

#장비 접속
dev1 = Device()

#RPC 정보 수집
with dev1:
    result1 = dev1.rpc.get_interface_information()
    result2 = dev1.rpc.get_configuration()

#데이터 수집
def collect_interface_information():
    merge = []
    physical_root = result1.findall('physical-interface')

    for physical_interface in physical_root:
        name = physical_interface.findtext('name').strip("\n")

        if re.match(r"\b(fe|ge|xe|et)\-([0-9][0-9]?)\/([0-9][0-9]?)\/([0-9][0-9]?)\b", name):
            information = {
                "interface": "",
                "admin_status": "",
                "oper_status": "",
                "mtu": "",
                "description": "",
                "speed": "",
                "duplex": "",
                "auto-nego": "",
                "ipaddress": "",
                "vlan" : ""
            }
            information["interface"] = name
            information["admin_status"] = physical_interface.findtext('admin-status').strip("\n")
            information["oper_status"] = physical_interface.findtext('oper-status').strip("\n")
            information["mtu"] = physical_interface.findtext('mtu').strip("\n")
            information["speed"] = physical_interface.findtext('speed').strip("\n")
            information["ipaddress"] = "-"
            if physical_interface.findtext('if-auto-negotiation') is None:
                information["auto-nego"] = "not found"
            else:
                information["auto-nego"] = physical_interface.findtext('if-auto-negotiation').strip("\n")
            if physical_interface.findtext('link-mode') is None:
                information["duplex"] = "not found"
            else:
                information["duplex"] = physical_interface.findtext('link-mode').strip("\n")
            if physical_interface.findtext('description') is None:
                information["description"] = "None"
            else:
                information["description"] = physical_interface.findtext('description').strip("\n")
            merge.append(information)
            for logical_interface in physical_interface.findall('logical-interface'):
                if re.match(r".*(16386|32767)", logical_interface.find('name').text.strip("\n")):
                    break
                else:
                    information_logical = {
                        "interface": "",
                        "admin_status": "",
                        "oper_status": "",
                        "mtu": "",
                        "description": "",
                        "speed": "",
                        "duplex": "",
                        "auto-nego": "",
                        "ipaddress": "",
                        "vlan": ""
                    }
                    information_logical["interface"] = logical_interface.findtext('name').strip("\n")
                    information_logical["admin_status"] = "-"
                    information_logical["oper_status"] = "-"
                    information_logical["mtu"] = "-"
                    information_logical["speed"] = "-"
                    information_logical["duplex"] = "-"
                    information_logical["auto-nego"] = "-"
                    vlans = result2.findall("interfaces/interface[name='{}']/unit/family/ethernet-switching/vlan/members".format(name))
                    vlan_list = []
                    for i in vlans:
                        vlan_list.append(i.text)
                    information_logical["vlan"] = str(vlan_list)
                    if logical_interface.findtext('address-family/interface-address/ifa-local') is None:
                        information_logical["ipaddress"] = "None"
                    else:
                        ip = logical_interface.findtext('address-family/interface-address/ifa-local').strip("\n")
                        subnet = logical_interface.findtext('address-family/interface-address/ifa-destination').strip("\n")
                        ipaddr = ip + "/" + subnet.split('/')[1]
                        information_logical["ipaddress"] = ipaddr

                    if logical_interface.findtext('description') is None:
                        information_logical["description"] = "None"
                    else:
                        information_logical["description"] = logical_interface.findtext('description').strip("\n")
                    merge.append(information_logical)
    return merge



#출력

print(
    'Interface'.ljust(15)+
    'Admin'.ljust(7)+
    'Link'.ljust(6)+
    'MTU'.ljust(6)+
    'Speed'.ljust(7)+
    'Duplex'.ljust(13)+
    'Auto-nego'.ljust(11)+
    'Description'.ljust(30)+
    'IP-Address'.ljust(20)+
    'Vlan'.ljust(0)
)

xml = collect_interface_information()

for i in range(len(collect_interface_information())):
    print(
        xml[i]["interface"].ljust(15)+
        xml[i]["admin_status"].ljust(7)+
        xml[i]["oper_status"].ljust(6)+
        xml[i]["mtu"].ljust(6)+
        xml[i]["speed"].ljust(7)+
        xml[i]["duplex"].ljust(13)+
        xml[i]["auto-nego"].ljust(11)+
        xml[i]["description"].ljust(30)+
        xml[i]["ipaddress"].ljust(20)+
        xml[i]["vlan"].ljust(0)
    )
