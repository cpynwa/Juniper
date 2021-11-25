from jnpr.junos import Device
import re

"""
test junos Ver = over 16.1R3
filename = show_interfaces_status.py
file location = /var/db/scripts/op/show_interfaces_status.py

- 적용 명령어
set system scripts language python
set system scripts op file show_interfaces_status.py

- 실행 명령어
root@MX960> op show_interfaces_status.py
"""

#장비 접속
#dev1 = Device()
#dev1 = Device(host='10.1.112.80', user='eknow', password='rkskek123')
dev1 = Device(host='10.1.113.120', user='root', password='jun000')
#dev1 = Device(host='10.1.113.41', user='juniper', password='jun2per')
#dev1 = Device(host='211.45.116.134', user='eknow', password='Test1234')

#RPC 정보 수집
with dev1:
    result1 = dev1.rpc.get_interface_information()
    result2 = dev1.rpc.get_l2ckt_connection_information()

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
                "circuit-id": "",
                "vlan" : "",
                "neighbor": "",
                "conn_status": ""
            }
            information["interface"] = name
            information["admin_status"] = physical_interface.findtext('admin-status').strip("\n")
            information["oper_status"] = physical_interface.findtext('oper-status').strip("\n")
            information["mtu"] = physical_interface.findtext('mtu').strip("\n")
            information["speed"] = physical_interface.findtext('speed').strip("\n")
            information["circuit-id"] = "-"
            information["vlan"] = "-"
            information["neighbor"] = "-"
            information["conn_status"] = "-"
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
                    continue
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
                        "circuit-id": "",
                        "vlan": "",
                        "neighbor": "",
                        "conn_status": ""
                    }
                    logical_name = logical_interface.findtext('name').strip("\n")
                    information_logical["interface"] = logical_name
                    information_logical["admin_status"] = "-"
                    information_logical["oper_status"] = "-"
                    information_logical["mtu"] = "-"
                    information_logical["speed"] = "-"
                    information_logical["duplex"] = "-"
                    information_logical["auto-nego"] = "-"

                    all_con_id = result2.findall("l2circuit-neighbor/connection/connection-id")

                    for i in all_con_id:
                        if re.match('^{}'.format(logical_name), i.text):
                            information_logical['conn_status'] = i.findtext("../connection-status")
                            circuit_id = i.text.split('vc')[1]
                            information_logical['circuit-id'] = re.sub(r'[^0-9]', '', circuit_id)
                            if i.findtext("../remote-pe") is None:
                                information_logical['neighbor'] = "-"
                            else:
                                information_logical['neighbor'] = i.findtext("../remote-pe")

                    if logical_interface.findtext('link-address') is None:
                        information_logical["vlan"] = "-"
                    else:
                        ethtype = logical_interface.findtext('link-address').strip("\n")
                        vlan = ethtype.split(".")[1]
                        information_logical["vlan"] = re.sub(r'[^0-9]', '', vlan)

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
                    continue
        else:
            continue
    return merge

#출력
print(
    'Interface'.ljust(15) +
    'Admin'.ljust(7) +
    'Link'.ljust(6) +
    'MTU'.ljust(6) +
    'Speed'.ljust(7) +
    'Duplex'.ljust(13) +
    'Auto-nego'.ljust(11) +
    'Description'.ljust(30) +
    'IP-Address'.ljust(20) +
    'Circuit-id'.ljust(12) +
    'Neighbor'.ljust(10) +
    'Conn_status'.ljust(13) +
    'Vlan'.ljust(0)
)

xml = collect_interface_information()

for i in range(len(xml)):
    print(
        xml[i]["interface"].ljust(15) +
        xml[i]["admin_status"].ljust(7) +
        xml[i]["oper_status"].ljust(6) +
        xml[i]["mtu"].ljust(6) +
        xml[i]["speed"].ljust(7) +
        xml[i]["duplex"].ljust(13) +
        xml[i]["auto-nego"].ljust(11) +
        xml[i]["description"].ljust(30) +
        xml[i]["ipaddress"].ljust(20) +
        xml[i]["circuit-id"].ljust(12) +
        xml[i]["neighbor"].ljust(10) +
        xml[i]["conn_status"].ljust(13) +
        xml[i]["vlan"].ljust(0)
    )