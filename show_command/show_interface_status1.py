from jnpr.junos import Device
import re

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
    result1 = dev1.rpc.get_interface_information()
    result2 = dev1.rpc.get_interface_information(terse=True, normalize=True)
    result1_name = result1.findall('physical-interface/name')

#사용가능한 인터페이스 리스트 작성
name_list = []
for i in result1_name:
    if re.match(r"\b(fe|ge|xe|et)\-([0-9][0-9]?)\/([0-9][0-9]?)\/([0-9][0-9]?)\b", i.text.strip("\n")):
        name_list.append(i.text.strip("\n"))
    else:
        continue

#데이터 수집
def collect_interface_information():
    merge = []
    for physical_interface in result1.findall('physical-interface'):
        name = physical_interface.findtext('name').strip("\n")
        for i in name_list:
            if name == i:
                information = {
                    "interface": "",
                    "admin_status": "",
                    "oper_status": "",
                    "mtu": "",
                    "description": "",
                    "speed": "",
                    "ipaddress": ""
                }
                information["interface"] = i
                information["admin_status"] = physical_interface.findtext('admin-status').strip("\n")
                information["oper_status"] = physical_interface.findtext('oper-status').strip("\n")
                information["mtu"] = physical_interface.findtext('mtu').strip("\n")
                information["speed"] = physical_interface.findtext('speed').strip("\n")
                information["ipaddress"] = "X"
                try:
                    information["description"] = physical_interface.findtext('description').strip("\n")
                except:
                    information["description"] = "X"
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
                            "ipaddress": ""
                        }

                        information_logical["interface"] = logical_interface.findtext('name').strip("\n")

                        information_logical["admin_status"] = "X"
                        information_logical["oper_status"] = "X"
                        information_logical["mtu"] = "X"
                        information_logical["speed"] = "X"
                        try:
                            ip = logical_interface.findtext('address-family/interface-address/ifa-local').strip("\n")
                            subnet = logical_interface.findtext(
                                'address-family/interface-address/ifa-destination').strip("\n")
                            ipadd = ip + "/" + subnet.split('/')[1]
                            information_logical["description"] = logical_interface.findtext('description').strip("\n")
                            information_logical["ipaddress"] = ipadd
                        except:
                            information_logical["description"] = "X"
                            information_logical["ipaddress"] = "X"
                        merge.append(information_logical)
    return merge

#출력

print(
    'Interface'.ljust(14)+
    'Admin'.ljust(6)+
    'Link'.ljust(5)+
    'mtu'.ljust(5)+
    'speed'.ljust(10)+
    'description'.ljust(20)+
    'ipaddress'.ljust(18)
)
for i in range(len(collect_interface_information())):
    print(
        collect_interface_information()[i]["interface"].ljust(14)+
        collect_interface_information()[i]["admin_status"].ljust(6)+
        collect_interface_information()[i]["oper_status"].ljust(5)+
        collect_interface_information()[i]["mtu"].ljust(5)+
        collect_interface_information()[i]["speed"].ljust(10)+
        collect_interface_information()[i]["description"].ljust(20)+
        collect_interface_information()[i]["ipaddress"].ljust(18)
    )

