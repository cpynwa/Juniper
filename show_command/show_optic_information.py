from jnpr.junos import Device
import re

"""
Junos Ver = over 16.1R3
filename = show_optic_information.py
location = /var/db/scripts/op/show_optic_information.py

- 적용 명령어
set system scripts language python3
set system scripts op file show_optic_information.py

- 실행 명령어
root@MX960> op show_optic_information.py
"""

# 장비 접속
dev1 = Device()

# RPC 정보 수집
with dev1:
    result1 = dev1.rpc.get_interface_information()
    result3 = dev1.rpc.get_chassis_inventory()
    result1_name = result1.findall('physical-interface/name')
    result3_module = result3.findall('chassis/chassis-module')

# 사용가능한 인터페이스 리스트 작성
name_list = []
for i in result1_name:
    if re.match(r"\b(fe|ge|xe|et)\-([0-9][0-9]?)\/([0-9][0-9]?)\/([0-9][0-9]?)\b", i.text.strip("\n")):
        name_list.append(i.text.strip("\n"))
    else:
        continue

# OPTIC 정보 수집
def collect_optic_information():
    chassis_int_list = []
    for chassis_module in result3_module:
        for module_name in chassis_module.findall('name'):
            if re.match(r"FPC\s\d", module_name.text):
                fpc = str(int(re.findall('\d+', module_name.text)[0]))
                for chassis_sub_module in chassis_module.findall('chassis-sub-module'):
                    for chassis_sub_module_name in chassis_sub_module.findall('name'):
                        if re.match(r"PIC\s\d", chassis_sub_module_name.text):
                            PIC = str(int(re.findall('\d+', chassis_sub_module_name.text)[0]))
                            for chassis_sub_sub_module in chassis_sub_module.findall('chassis-sub-sub-module'):
                                for chassis_sub_sub_module_name in chassis_sub_sub_module.findall('name'):
                                    if re.match(r"Xcvr\s\d", chassis_sub_sub_module_name.text):
                                        OPTIC = str(int(re.findall('\d+', chassis_sub_sub_module_name.text)[0]))
                                        if re.match(r".*((LR)|(SR))", chassis_sub_sub_module.find('description').text):
                                            optic_info = {"interface": "", "optic": "", "serial": ""}
                                            optic_info["interface"] = "xe-"+fpc+'/'+PIC+'/'+OPTIC
                                            optic_info["optic"] = chassis_sub_sub_module.find('description').text
                                            optic_info["serial"] = chassis_sub_sub_module.find('serial-number').text
                                            chassis_int_list.append(optic_info)
                        elif re.match(r"MIC\s\d", chassis_sub_module_name.text):
                            for chassis_sub_sub_module in chassis_sub_module.findall('chassis-sub-sub-module'):
                                for chassis_sub_sub_module_name in chassis_sub_sub_module.findall('name'):
                                    if re.match(r"PIC\s\d", chassis_sub_sub_module_name.text):
                                        PIC = str(int(re.findall('\d+', chassis_sub_sub_module_name.text)[0]))
                                        for chassis_sub_sub_sub_module in chassis_sub_sub_module.findall('chassis-sub-sub-sub-module'):
                                            for chassis_sub_sub_sub_module_name in chassis_sub_sub_sub_module.findall('name'):
                                                if re.match(r"Xcvr\s\d", chassis_sub_sub_sub_module_name.text):
                                                    OPTIC = str(int(re.findall('\d+', chassis_sub_sub_sub_module_name.text)[0]))
                                                    if re.match(r".*((LX)|(SX))", chassis_sub_sub_sub_module.find('description').text):
                                                        optic_info = {"interface": "", "optic": "", "serial": ""}
                                                        optic_info["interface"] = "ge-" + fpc + '/' + PIC + '/' + OPTIC
                                                        optic_info["optic"] = chassis_sub_sub_sub_module.find('description').text
                                                        optic_info["serial"] = chassis_sub_sub_sub_module.find('serial-number').text
                                                        chassis_int_list.append(optic_info)
                                                    elif re.match(r".*((LR)|(SR))", chassis_sub_sub_sub_module.find('description').text):
                                                        optic_info = {"interface": "", "optic": "", "serial": ""}
                                                        optic_info["interface"] = "xe-" + fpc + '/' + PIC + '/' + OPTIC
                                                        optic_info["optic"] = chassis_sub_sub_sub_module.find('description').text
                                                        optic_info["serial"] = chassis_sub_sub_sub_module.find('serial-number').text
                                                        chassis_int_list.append(optic_info)
    return chassis_int_list

#데이터 수집
def collect_interface_information():
    merge = []
    for physical_interface in result1.findall('physical-interface'):
        name = physical_interface.findtext('name').strip("\n")
        for i in name_list:
            if name == i:
                information = {
                    "interface": "",
                    "oper_status": "",
                    "description": "",
                }
                information["interface"] = i
                information["oper_status"] = physical_interface.findtext('oper-status').strip("\n")
                try:
                    information["description"] = physical_interface.findtext('description').strip("\n")
                except:
                    information["description"] = "X"
                merge.append(information)
    return merge

#OPTIC정보 병합
interface_info = collect_interface_information()
optic_info = collect_optic_information()

for i in range(len(interface_info)):
    for j in range(len(optic_info)):
        if interface_info[i]["interface"] == optic_info[j]["interface"]:
            interface_info[i].update(optic_info[j])
            break
        else:
            interface_info[i]["optic"] = "X"
            interface_info[i]["serial"] = "X"


#출력

print(
    'Interface'.ljust(14)+
    'Link'.ljust(5)+
    'description'.ljust(20)+
    'optics'.ljust(15)+
    'serial'
)
for i in range(len(interface_info)):
    print(
        interface_info[i]["interface"].ljust(14)+
        interface_info[i]["oper_status"].ljust(5)+
        interface_info[i]["description"].ljust(20)+
        interface_info[i]["optic"].ljust(15)+
        interface_info[i]["serial"]
        )

