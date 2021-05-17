from jnpr.junos import Device
"""
Junos Ver = over 16.1R3
filename = show_interfaces_status.py
location = /var/db/script/op/show_interfaces_status.py

- 적용 명령어
set system scripts language python3
set system scripts op file show_interfaces_status.py

- 실행 명령어
root@MX960> op show_interface_status1.py
"""

# device class 속성값정의
class Devices:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd


#장비 접속
device1 = Devices(host='X.X.X.X', user='XXXX', passwd='XXXX')
dev1 = Device(host=device1.host, user=device1.user, password=device1.passwd)

#RPC 정보 수집
with dev1:
    result = dev1.rpc.get_config()
    result_name = result.findall('interfaces/interface/name')

# 인터페이스 설정 수집
def collect_interface_setting():
    merge = []
    for physical_interface in result.findall('interfaces/interface'):
        information = {"interface": "","ipaddress": "",
                "description": "",
                "hold_time_up": "",
                "hold_time_down": "",
                "mtu": "",
                "ospf_area": "",
                "ospf_type": "",
                "ospf_bfd_minimum": "",
                "ospf_bfd_multiplier": "",
                "ospf_metric": "",
                "mpls_set": "",
                "ldp_set": "",
                "ospf3_area": "",
                "ospf3_type": "",
                "ospf3_metric": "",
            }

        information["interface"] = physical_interface.findtext('name')
        information["ipaddress"] = "X"
        information["description"] = physical_interface.findtext('description')
        information["hold_time_up"] = physical_interface.findtext('hold-time/up')
        information["hold_time_down"] = physical_interface.findtext('hold-time/down')
        information["mtu"] = physical_interface.findtext('mtu')

        merge.append(information)
        for logical_interface in physical_interface.findall('unit'):
            information_logical = {
                "interface": "",
                "ipaddress": "",
                "description": "",
                "hold_time_up": "",
                "hold_time_down": "",
                "mtu": "",
                "ospf_area": "",
                "ospf_type": "",
                "ospf_bfd_minimum": "",
                "ospf_bfd_multiplier": "",
                "ospf_metric": "",
                "mpls_set": "",
                "ldp_set": "",
                "ospf3_area": "",
                "ospf3_type": "",
                "ospf3_metric": "",
            }

            information_logical["interface"] = information["interface"] + "." + logical_interface.findtext('name')
            information_logical["ipaddress"] = logical_interface.findtext('family/inet/address/name')
            information_logical["description"] = logical_interface.findtext('description')
            information_logical["hold_time_up"] = "X"
            information_logical["hold_time_down"] = 'X'
            information_logical["mtu"] = "X"

            merge.append(information_logical)
    return merge

# ospf 설정 수집
def collect_ospf_setting():
    merge = []
    for area in result.findall('protocols/ospf/area'):
        for interface in area.findall('interface'):
            information = {
                "interface": "",
                "ospf_area": "",
                "ospf_type": "",
                "ospf_bfd_minimum": "",
                "ospf_bfd_multiplier": "",
                "ospf_metric": "",
            }
            information["interface"] = interface.findtext('name')
            information["ospf_area"] = area.findtext('name')
            information["ospf_type"] = interface.findtext('interface-type')
            information["ospf_bfd_minimum"] = interface.findtext('bfd-liveness-detection/minimum-interval')
            information["ospf_bfd_multiplier"] = interface.findtext('bfd-liveness-detection/multiplier')
            information["ospf_metric"] = interface.findtext('metric')
            merge.append(information)
    return merge

def collect_mpls_setting():
    merge = []
    for interface in result.findall('protocols/mpls/interface'):
        information = {
            "interface": "",
            "mpls_set": ""
        }
        information["interface"] = interface.findtext('name')
        information["mpls_set"] = "O"
        merge.append(information)
    return merge

def collect_ldp_setting():
    merge = []
    for interface in result.findall('protocols/ldp/interface'):
        information = {
            "interface": "",
            "ldp_set": ""
        }
        information["interface"] = interface.findtext('name')
        information["ldp_set"] = "O"
        merge.append(information)
    return merge

def collect_ospf3_setting():
    merge = []
    for area in result.findall('protocols/ospf3/area'):
        for interface in area.findall('interface'):
            information = {
                "interface": "",
                "ospf3_area": "",
                "ospf3_type": "",
                "ospf3_metric": "",
            }
            information["interface"] = interface.findtext('name')
            information["ospf3_area"] = area.findtext('name')
            information["ospf3_type"] = interface.findtext('interface-type')
            information["ospf3_metric"] = interface.findtext('metric')
            merge.append(information)
    return merge
collect_ospf3_setting()

#OPTIC정보 병합
interface = collect_interface_setting()
ospf = collect_ospf_setting()
mpls = collect_mpls_setting()
ldp = collect_ldp_setting()
ospf3 = collect_ospf3_setting()


for i in range(len(interface)):
    for j in range(len(ospf)):
        if interface[i]["interface"] == ospf[j]["interface"]:
            interface[i].update(ospf[j])
            break
        else:
            interface[i]["ospf_area"] = "X"
            interface[i]["ospf_type"] = "X"
            interface[i]["ospf_bfd_minimum"] = "X"
            interface[i]["ospf_bfd_multiplier"] = "X"
            interface[i]["ospf_metric"] = "X"
    for j in range(len(mpls)):
        if interface[i]["interface"] == mpls[j]["interface"]:
            interface[i].update(mpls[j])
            break
        else:
            interface[i]["mpls_set"] = "X"
    for j in range(len(ldp)):
        if interface[i]["interface"] == ldp[j]["interface"]:
            interface[i].update(ldp[j])
            break
        else:
            interface[i]["ldp_set"] = "X"
    for j in range(len(ospf3)):
        if interface[i]["interface"] == ospf3[j]["interface"]:
            interface[i].update(ospf3[j])
            break
        else:
            interface[i]["ospf3_area"] = "X"
            interface[i]["ospf3_type"] = "X"
            interface[i]["ospf3_metric"] = "X"

# 출력
print("interface".ljust(14) +
          "ipaddress".ljust(18) +
          "description".ljust(18) +
          "h_up".ljust(5) +
          "h_dn".ljust(5) +
          "mtu".ljust(5) +
          "area".ljust(9) +
          "type".ljust(5) +
          "bfd_min".ljust(8) +
          "bfd_mul".ljust(8) +
          "cost".ljust(6) +
          "mpls".ljust(5) +
          "ldp".ljust(4) +
          "o3_area".ljust(9) +
          "o3_type".ljust(8) +
          "o3_cost"
          )

for i in range(len(interface)):
    print(
        str(interface[i]["interface"]).ljust(14) +
        str(interface[i]["ipaddress"]).replace("None", "X").ljust(18) +
        str(interface[i]["description"]).replace("None", "X").ljust(18) +
        str(interface[i]["hold_time_up"]).replace("None", "X").ljust(5) +
        str(interface[i]["hold_time_down"]).replace("None", "X").ljust(5) +
        str(interface[i]["mtu"]).replace("None", "X").ljust(5) +
        str(interface[i]["ospf_area"]).replace("None", "X").ljust(9)+
        str(interface[i]["ospf_type"]).replace("None", "X").ljust(5)+
        str(interface[i]["ospf_bfd_minimum"]).replace("None", "X").ljust(8)+
        str(interface[i]["ospf_bfd_multiplier"]).replace("None", "X").ljust(8)+
        str(interface[i]["ospf_metric"]).replace("None", "X").ljust(6) +
        str(interface[i]["mpls_set"]).replace("None", "X").ljust(5) +
        str(interface[i]["ldp_set"]).replace("None", "X").ljust(4) +
        str(interface[i]["ospf3_area"]).replace("None", "X").ljust(9) +
        str(interface[i]["ospf3_type"]).replace("None", "X").ljust(8) +
        str(interface[i]["ospf3_metric"]).replace("None", "X")
)
