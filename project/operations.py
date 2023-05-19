def replace_path(p):
    return p[:-1] if p[-1] == "/" else p

def add_eth(stringToConvert):
    new_str = stringToConvert.replace("; ", ", ").replace(";",",")
    new_str = new_str.replace(" ","").split(",")
    new_str[-1] = new_str[-1].replace(";", "")
    new_str = [x + ".eth0" for x in new_str]
    bb = 1
    for item in range(0, len(new_str)):
        number_interface = 1
        for ii in range(bb, len(new_str)):
            if new_str[item] == new_str[ii]:
                new_str[ii] = new_str[ii].replace(".eth0", ".eth{}".format(number_interface))
                number_interface = number_interface + 1
        bb = bb + 1
    return new_str

def ip_list(vms_eth, gw_eth, numbers_vms, numb_cyber):
    temp2 = 0
    zz = 0
    ip_list = {}
    for i in range(len(numbers_vms)):
        a = vms_eth[temp2:numbers_vms[zz] + temp2]
        for h in range(len(a)):
            ip_list[a[h]] = ['{}.1.{}.{}'.format(numb_cyber, i + 1, h + 2), '{}.1.{}.{}'.format(numb_cyber, i + 1, len(
                a) + 2)]  # il gateway è l'ip del firewall che è sempre l'ultima macchina a cui vengono assegnati gli indirizzi, quindi macchine presenti nella sottorete + 2 (poichè parto da .2)
        temp2 = temp2 + numbers_vms[zz]
        zz = zz + 1
    for i in range(len(numbers_vms)):
        ip_list[gw_eth[i]] = ['{}.1.{}.{}'.format(numb_cyber, i + 1, numbers_vms[i] + 2)]
    #print(ip_list)
    return ip_list


def number_of_members(members_not_format):
    # elements for each network (only for members, because there is only one firewall for each ; )
    members = members_not_format.replace(" ", "").split(";")
    len_str = len(members)
    elements = []
    for x in range(len_str):
        add = members[x].replace(" ", "").split(",")
        elements.append(len(add))
    return elements


#add firewall rules for vm export machine(logstash), all vms can communicate with vm export machine
def add_rule_to_export_data(rules, name_network):
    for x in range((len(name_network)-1)) :
        rl = {'rule': 'src={} dst={}'.format(name_network[x], name_network[-1])}
        rules.append(rl)
        rl = {'rule': 'src={} dst={}'.format(name_network[-1], name_network[x])}
        rules.append(rl)
    return rules

#getting OS for vm list input
def get_os(vm_list, total_vm, total_os):
    os_output = []
    for idx, x in enumerate(vm_list):
        for idy, y in enumerate(total_vm):
            if x == y:
                os_output.append(total_os[idy])
    return os_output


#return true/false if vm must be monitored by filebeat
def control_source_log(vm, source):
    out = False
    for x in source:
        if vm == x:
            out = True
    return out


