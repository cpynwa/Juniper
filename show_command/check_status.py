import re
"""
show ospf neighbor
show ospf3 neighbor
show ldp neighbor
show bfd session
show mpls interface
"""

all_interface = "xe-0/0/0 xe-0/0/1 xe-0/0/2"
interfaces = all_interface.split(" ")

ospf = []
ospf3 = []
ldp = []
mpls = []
bfd = []

with open("config.txt", "r") as file:
    for line in file:
        if re.search("Address          I", line):
            for line in file:
                ospf.append(line)
                if re.search(f"show", line):
                    break
        elif re.search("ID               I", line):
            for line in file:
                ospf3.append(line)
                if re.search(f"show", line):
                    break
        elif re.search("Address                             I", line):
            for line in file:
                ldp.append(line)
                if re.search(f"show", line):
                    break
        elif re.search("Address                  S", line):
            for line in file:
                bfd.append(line)
                if re.search(f"show", line):
                    break
        elif re.search("Interface        S", line):
            for line in file:
                mpls.append(line)
                if re.search(f"show", line):
                    break



all_status = []
for interface in interfaces:

    status = {
        "interface": "",
        "ospf": "",
        "ospf3": "",
        "ldp": "",
        "bfd": "",
        "mpls": ""
    }
    status["interface"] = interface
    for ospf_i in ospf:
        if re.match(f".*{interface}.*", ospf_i):
            if re.match(".*Full.*", ospf_i):
                status["ospf"] = "Full"
    for ospf3_i in ospf3:
        if re.match(f".*{interface}.*", ospf3_i):
            if re.match(".*Full.*", ospf3_i):
                status["ospf3"] = "Full"
    for ldp_i in ldp:
        if re.match(f".*{interface}.*", ldp_i):
            status["ldp"]= "OK"
    for bfd_i in bfd:
        if re.match(f".*{interface}.*", bfd_i) and re.match(".*Up.*", bfd_i):
            status["bfd"] = "Up"
    for mpls_i in mpls:
        if re.match(f".*{interface}.*", mpls_i) and re.match(".*Up.*", mpls_i):
            status["mpls"] = "Up"
    all_status.append(status)

print(
    "Interface".ljust(12) +
    "OSPF".ljust(6) +
    "OSPF3".ljust(7) +
    "LDP".ljust(6) +
    "BFD".ljust(6) +
    "MPLS".ljust(6)
)

for i in range(len(all_status)):
    print(
        all_status[i]["interface"].ljust(12) +
        all_status[i]["ospf"].ljust(6) +
        all_status[i]["ospf3"].ljust(7) +
        all_status[i]["ldp"].ljust(6) +
        all_status[i]["bfd"].ljust(6) +
        all_status[i]["mpls"].ljust(6)
    )