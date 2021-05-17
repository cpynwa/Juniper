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
device1 = Devices(host='211.45.116.132', user='eknow', passwd='Test1234')
dev1 = Device(host=device1.host, user=device1.user, password=device1.passwd)

#RPC 정보 수집
with dev1:
    result = dev1.rpc.get_interface_information(statistics=True, normalize=True)
    result_name = result.findall('physical-interface/name')

#사용가능한 인터페이스 리스트 작성
name_list = []
for i in result_name:
    if re.match(r"\b(fe|ge|xe|et)\-([0-9][0-9]?)\/([0-9][0-9]?)\/([0-9][0-9]?)\b", i.text.strip("\n")):
        name_list.append(i.text.strip("\n"))
    else:
        continue

def collect_interface_error():
    merge = []
    for physical_interface in result.findall('physical-interface'):
        name = physical_interface.findtext('name').strip("\n")
        for i in name_list:
            if name == i:
                information = {
                    "interface": "",
                    "description": "",
                    "oper-status": "",
                    "input-error-count": "",
                    "output-error-count": "",
                }
                information["interface"] = i
                information["oper-status"] = physical_interface.findtext('oper-status').strip("\n")
                information["input-error-count"] = physical_interface.findtext('input-error-count').strip("\n")
                information["output-error-count"] = physical_interface.findtext('output-error-count').strip("\n")
                try:
                    information["description"] = physical_interface.findtext('description').strip("\n")
                except:
                    information["description"] = "X"
                merge.append(information)
    return merge

#출력


print(
    'Interface'.ljust(14)+
    'description'.ljust(20)+
    'status'.ljust(7)+
    'in-error'.ljust(9)+
    'out-error'.ljust(10)
)
for i in range(len(collect_interface_error())):
    print(
        collect_interface_error()[i]["interface"].ljust(14)+
        collect_interface_error()[i]["description"].ljust(20)+
        collect_interface_error()[i]["oper-status"].ljust(7)+
        collect_interface_error()[i]["input-error-count"].ljust(9)+
        collect_interface_error()[i]["output-error-count"].ljust(10)
    )
