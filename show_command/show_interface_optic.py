from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos import Device
import re
import os

# 장비 접속
# dev = Device(host='x.x.x.x', user='eknow', password='Test1234')

# 정보 수집
# with StartShell(dev) as ss:
#     extensive = ss.run("cli -c 'show interfaces extensive | no-more'")[1]
#     hardware = ss.run("cli -c 'show chassis hardware detail | no-more'")[1]
#
# with open("hardware.txt", "w") as file1:
#     file1.write(hardware)
#
# with open("extensive.txt", "w") as file2:
#     file2.write(extensive)


with open("../hardware.txt", "r") as hfile:
    hlines = hfile.readlines()

with open("../extensive.txt", "r") as efile:
    elines = efile.readlines()

# os.remove("extensive.txt")
# os.remove("hardware.txt")

def collect_optic_info(lines):
    interface_list = []

    for line in lines:
        interface = {"interface": "", "optic": "", "serial": ""}

        if re.match(r'^FPC',line):
            fpc = re.findall('\d+', line)[0]

        elif re.match(r'^    PIC',line):
            pic = re.findall('\d+', line)[0]

        elif re.match(r'^  PIC',line):
            pic = re.findall('\d+', line)[0]

        elif re.match(r'^      Xcvr',line):
            xcvr = re.findall('\d+', line)[0]
            spl = line.split()
            idx = [i for i, item in enumerate(spl) if re.match("SFP.*|XFP.*|QSFP.*", item)]
            optic = spl[idx[0]]
            interface["optic"] = optic
            interface["serial"] = spl[idx[0] - 1]

            if re.match(r'.*SX.*|,*LX.*', optic):
                interface["interface"] = "ge-" + str(fpc) + "/" + str(pic) + "/" + str(xcvr)

            elif re.match(r'.*LR.*|.*SR.*', optic):
                interface["interface"] = "xe-" + str(fpc) + "/" + str(pic) + "/" + str(xcvr)

            interface_list.append(interface)

        elif re.match(r'^    Xcvr', line):
            xcvr = re.findall('\d+', line)[0]
            spl = line.split()
            idx = [i for i, item in enumerate(spl) if re.match("SFP.*|XFP.*|QSFP.*", item)]
            optic = spl[idx[0]]
            interface["optic"] = optic
            interface["serial"] = spl[idx[0] - 1]

            if re.match(r'.*LR.*|.*SR.*', optic):
                interface["interface"] = "xe-" + str(fpc) + "/" + str(pic) + "/" + str(xcvr)

            interface_list.append(interface)

        elif not line:
            break

    return interface_list

def collect_interface_info(lines):
    idx = [i for i, item in enumerate(lines) if re.match("^Physical interface: ge|^Physical interface: xe|^Physical interface: et",item)]
    interface_list = []

    for i in idx:
        interface = {"interface": "", "status": "", "description": ""}
        interface["interface"] = lines[i].split()[2].strip(",")

        try:
            interface["status"] = lines[i].split()[8]
        except:
            interface["status"] = lines[i].split()[7]

        if re.match("^  Description:", lines[i + 4]):
            interface["description"] = lines[i + 4].split()[1]
            interface_list.append(interface)

        else:
            interface["description"] = ""
            interface_list.append(interface)

    return interface_list


#OPTIC정보 병합
interface_info = collect_interface_info(elines)
optic_info = collect_optic_info(hlines)

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
    'Status'.ljust(7)+
    'Description'.ljust(25)+
    'Optics'.ljust(15)+
    'Serial'
)

for i in range(len(interface_info)):
    print(
        interface_info[i]["interface"].ljust(14)+
        interface_info[i]["status"].ljust(6)+
        interface_info[i]["description"].ljust(25)+
        interface_info[i]["optic"].ljust(15)+
        interface_info[i]["serial"]
    )