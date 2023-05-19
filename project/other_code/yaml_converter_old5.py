import sys
import yaml
import json

with open(r'/home/ubuntu/PycharmProjects/config1_4.yaml') as f:
    data = yaml.safe_load(f)

path_dst_script = "/home/ubuntu/"  # path destination script ON virtual machine
path_img = "/home/ubuntu/cyris/images"
path_models = "/home/ubuntu/cyris/models"
path = data[6]['path']  # path cyris
numb_cyber = data[6]['cyber_range_id']

# HOST SETTING
host = [{'id': 'host_1', 'mgmt_addr': '192.168.1.65', 'virbr_addr': '192.168.122.1', 'account': 'ubuntu'}]
#print(host)

# ----------------------------------------------------------------------------
# GUEST SECTION
guest = []

# MODEL
modeler = data[0]['modeler']
model = data[0]['name'].split()
interface = data[0]['interface']
if modeler == 'openmodelica':
    gst = {'id': model[0], 'basevm_host': 'host_1',
           'basevm_config_file': '{}/image_ubuntu.xml'.format(path_img), 'basevm_type': 'kvm',
           'tasks': [{'copy_content': [
               {'src': '{}/{}/{}.tar.gz'.format(path_models, model[0], model[0]), 'dst': '{}'.format(path_dst_script)},
               {'src': '{}/PycharmProjects/temp/opc_{}.py'.format(path, interface),
                'dst': '{}'.format(path_dst_script)},
               {'src': '{}/PycharmProjects/temp/script.sh'.format(path), 'dst': '{}'.format(path_dst_script)},
               {'src': '{}/diagslave'.format(path_models), 'dst': '{}'.format(path_dst_script)}
           ]}]
           }
    guest.append(gst)

# MTU
mtu = data[1]['name'].split(", ")
hmi = data[1]['hmi'].split(", ")
for x in range(len(mtu)):
    if hmi[x] == 'scadabr':
        '''
        gst = {'id' : mtu[x], 'basevm_host': 'host_1', 'basevm_config_file' : '{}/xubuntu.xml'.format(path), 'basevm_type' : 'kvm',
           'tasks' : [{'copy_content' : [ {'src' : '/path/mango_configuration', 'dst' : 'bin/cyberrange'},
                                          {'src': '/path/other_conf', 'dst' : 'bin/cyberrange' } ]}]}
        '''
        gst = {'id': mtu[x], 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_ubuntu.xml'.format(path_img),
               'basevm_type': 'kvm',
               'tasks' : [{'copy_content': [
                   {'src': '/home/ubuntu/PycharmProjects/temp/data.json', 'dst': '{}'.format(path_dst_script)},
                   {'src': '/home/ubuntu/PycharmProjects/temp/script_selenium.py', 'dst': '{}'.format(path_dst_script)}
               ]}]
               }

    guest.append(gst)

# RTU
rtu = []
if data[2]['name'] != None:
    rtu = data[2]['name'].replace(", ",",").split(",")
    rtu_os = data[2]['os'].replace(", ",",").split(",")
    for idx, x in enumerate(rtu):
        gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, rtu_os[idx]),
               'basevm_type': 'kvm',
               'tasks': [{'copy_content': [
                   {'src': '{}/diagslave'.format(path_models), 'dst': '{}'.format(path_dst_script)}
               ]}]
               }
        guest.append(gst)

# GENERIC
generic = []
if data[3]['name'] != None:
    generic = data[3]['name'].replace(", ",",").split(",")
    os = data[3]['os'].replace(", ",",").split(",")
    for idx, x in enumerate(generic):
        gst = {'id': x, 'basevm_host': 'host_1',
               'basevm_config_file': '{}/image_{}.xml'.format(path_img, os[idx]), 'basevm_type': 'kvm'}
        guest.append(gst)

# FIREWALL
firewall = data[4]['name'].replace(", ",",").split(",")
fw_os = data[4]['os'].replace(", ",",").split(",")
for idx, x in enumerate(firewall):
    gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, fw_os[idx]),
           'basevm_type': 'kvm'}
    guest.append(gst)

# -----------------------------------------------------------------------------
# CLONE SETTINGS
clone_guest = []

# SECTION GUESTS
total_number_vm = model + mtu + rtu + generic
entry_point = data[6]['entry_point']

for y in total_number_vm:
    if y == entry_point:
        cl_g = {'guest_id': y, 'number': 1, 'entry_point': bool('yes')}
        clone_guest.append(cl_g)
    else:
        cl_g = {'guest_id': y, 'number': 1}
        clone_guest.append(cl_g)

for y in range(len(firewall)):
    if firewall[y] == entry_point:
        cl_g = {'guest_id': y, 'number': 1, 'forwarding_rules': data[4]['forwarding'][y]['rules'],
                'entry_point': bool('yes')}
        clone_guest.append(cl_g)
    else:
        cl_g = {'guest_id': firewall[y], 'number': 1, 'forwarding_rules': data[4]['forwarding'][y]['rules']}
        clone_guest.append(cl_g)

# SECTION NETWORKS
nt = []
ss = 0
name_network = data[5]['name'].replace("; ",";").split(";")
#cc = name_network.split("; ")
name_network[-1] = name_network[-1].replace(";", "")  # elimino ";" dall'ultimo elemento della lista
members = data[5]['members']
gateway = data[5]['gateway']

#calcolo elementi in ogni rete (solo per il campo members poichè di firewall ce n'è uno per ogni ; )
stringa = members.replace("; ",";").split(";")
len_str = len(stringa)
elements = []
for x in range(len_str):
    add = stringa[x].replace(", ",",").split(",")
    elements.append(len(add))


def add_eth(stringToConvert):
    new_str = stringToConvert.replace("; ", ", ").replace(";",",")
    new_str = new_str.replace(", ",",").split(",")
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

stringa2 = add_eth(members)
stringa_gateway = add_eth(gateway)

# insert into networks
str1 = ", "
tmp = 0
for j in name_network:
    ntt = {'name': j, 'members': str1.join(stringa2[tmp:elements[ss] + tmp]), 'gateway': stringa_gateway[ss]}
    nt.append(ntt)
    tmp = tmp + elements[ss]
    ss = ss + 1

range_id = data[6]['cyber_range_id']
clone = [{'range_id': range_id, 'hosts': [{'host_id': 'host_1', 'instance_number': 1, 'guests': clone_guest,
                                           'topology': [{'type': 'custom', 'networks': nt}]}]}]
# -----------------------------------------------------------------------------
# OUTPUT
output = [
    {'host_settings': host},
    {'guest_settings': guest},
    {'clone_settings': clone}
]

with open(r'/home/ubuntu/cyris/examples/cyberrange.yml', 'w') as file:
    data_out = yaml.dump(output, file, sort_keys=False)

# ---------------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT AFTER CLONE GENERATOR

temp2 = 0
zz = 0
ip_list = {}
for i in range(len(elements)):
    a = stringa2[temp2:elements[zz] + temp2]
    for h in range(len(a)):
        ip_list[a[h]] = ['{}.1.{}.{}'.format(numb_cyber, i + 1, h + 2), '{}.1.{}.{}'.format(numb_cyber, i + 1, len(a) + 2)]  # il gateway è l'ip del firewall che è sempre l'ultima macchina a cui vengono assegnati gli indirizzi, quindi macchine presenti nella sottorete + 2 (poichè parto da .2)
    temp2 = temp2 + elements[zz]
    zz = zz + 1
for i in range(len(elements)):
    ip_list[stringa_gateway[i]] = ['{}.1.{}.{}'.format(numb_cyber, i + 1, elements[i] + 2)]
print(ip_list)

#print(ip_list)

total_number_vm2 = total_number_vm + firewall
#total_number_vm2 = [x + ".eth0" for x in total_number_vm2]  # solo eth0 perchè anche se una macchina ha 2 interfacce, basta che mi collego via ssh solo alla eth0

with open(r'/home/ubuntu/PycharmProjects/temp/script_after_clone.sh','w') as f:
    f.write("#!/bin/bash\n")
    f.write("# {}\n".format(model[0]))
    f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
    f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
    f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
    f.write('chmod +x /home/ubuntu/script.sh;')
    f.write('/home/ubuntu/script.sh &>/dev/null &"')
    f.write("\n")

    f.write("# {}\n".format(mtu[0]))
    f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
    f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
    f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
    f.write("su -c 'python3 /home/ubuntu/script_selenium.py' - ubuntu")
    f.write(' &>/dev/null &"\n')

    if len(rtu) != 0:
        for y in rtu:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write("{}diagslave -m tcp".format(path_dst_script))
            f.write(' &>/dev/null &"\n')

    if len(generic) != 0:
        for y in generic:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
            f.write("\n")

    for y in firewall:
        f.write("# {}\n".format(y))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
        # f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
        f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
        f.write("\n")
f.close()

with open(r'/home/ubuntu/PycharmProjects/temp/script_after_clone_restart.sh','w') as f:
    f.write("#!/bin/bash\n")
    f.write("# {}\n".format(model[0]))
    f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
    f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
    f.write('"route add default gw {} eth0;'.format(ip_list[model[0] + '.eth0'][1]))
    f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
    f.write('chmod +x /home/ubuntu/script.sh;')
    f.write('/home/ubuntu/script.sh &>/dev/null &"')
    f.write("\n")

    f.write("# {}\n".format(mtu[0]))
    f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
    f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
    f.write('"route add default gw {} eth0;'.format(ip_list[mtu[0] + '.eth0'][1]))
    f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
    f.write("\n")

    if len(rtu) != 0:
        for y in rtu:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y + '.eth0'][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write("{}diagslave -m tcp".format(path_dst_script))
            f.write(' &>/dev/null &"\n')

    if len(generic) != 0:
        for y in generic:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y + '.eth0'][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
            f.write("\n")

    for y in firewall:
        f.write("# {}\n".format(y))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
        f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
        f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
        f.write("\n")
f.close()

'''

with open(r'/home/ubuntu/PycharmProjects/temp/script_after_clone.sh','w') as f:
    mcn = model + mtu + firewall + generic
    mcn = [x + ".eth0" for x in mcn]
    idx = 0
    f.write("#!/bin/bash\n")
    for y in mcn:
        if y == model[0] + '.eth0':
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write('chmod +x /home/ubuntu/script.sh;')
            f.write('/home/ubuntu/script.sh &>/dev/null &"')
            f.write("\n")
        elif y == mtu[0] + '.eth0':
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write("su -c 'python3 /home/ubuntu/script_selenium.py' - ubuntu")
            f.write(' &>/dev/null &"\n')
        elif y == stringa_gateway[idx]:
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            # f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
            f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
            f.write("\n")
            idx = idx + 1
        elif y != model[0] + '.eth0' and y != mtu[0] + '.eth0' and y != stringa_gateway[idx]:
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
            f.write("\n")
    if len(rtu) != 0:
        mcn = rtu
        mcn = [x + '.eth0' for x in mcn]
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[mcn[0]][0]))
        f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
        f.write("{}diagslave -m tcp".format(path_dst_script))
        f.write(' &>/dev/null &"\n')
    f.write("exit 0")
f.close()

with open(r'/home/ubuntu/PycharmProjects/temp/script_after_clone_restart.sh','w') as f:
    mcn = model + mtu + firewall + generic
    mcn = [x + ".eth0" for x in mcn]
    idx = 0
    f.write("#!/bin/bash\n")
    for y in mcn:
        if y == model[0] + '.eth0':
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write('chmod +x /home/ubuntu/script.sh;')
            f.write('/home/ubuntu/script.sh &>/dev/null &"')
            f.write("\n")
        elif y == stringa_gateway[idx] + '.eth0':
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
            f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
            f.write("\n")
            idx = idx + 1
        elif y != model[0] + '.eth0' and y != stringa_gateway[idx]:
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
            f.write("\n")
    if len(rtu) != 0:
        mcn = rtu
        mcn = [x + '.eth0' for x in mcn]
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[mcn[0]][0]))
        f.write('"route add default gw {} eth0;'.format(ip_list[mcn[0]][1]))
        f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
        f.write("{}diagslave -m tcp".format(path_dst_script))
        f.write(' &>/dev/null &"\n')
    f.write("exit 0")
f.close()
'''




# ------------------------------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# OPC GENERATOR

url = data[0]['opc_parameters']['server']
# url = "opc.tcp://DESKTOP-ADCS5PF:4841"
if data[2]['name'] != None:
    address_modbus = ip_list[rtu[0] + '.eth0'][0]
else:
    address_modbus = 'localhost'
# interface = data[1]['interface']

with open(r'/home/ubuntu/PycharmProjects/temp/opc_{}.py'.format(interface), 'w') as f:
    f.write(
        "import threading\nimport time\nimport timeit\nimport opcua\nfrom opcua import Client\nfrom opcua import ua\n")
    f.write("import modbus_tk\nimport modbus_tk.defines as cst\nimport modbus_tk.modbus_tcp as modbus_tcp\n\n")
    f.write('url = "{}"\n'.format(url))
    f.write("client = Client(url)\nclient.connect()\n")
    f.write('master = modbus_tcp.TcpMaster(host="{}", port=502)\n'.format(address_modbus))

value_run = data[0]['opc_parameters']['run']
sens = data[0]['opc_parameters']['sensors']

if data[0]['opc_parameters']['actuators'] != None:
    act = data[0]['opc_parameters']['actuators']
    #name, address actuators
    actuators_name = [x for x in act]
    actuators_address = []
    for i in act:
        actuators_address.append(act[i])

# name, address sensors
sensors_name = [x.replace(".","") for x in sens]
sensors_address = []
for i in sens:
    sensors_address.append(sens[i])


with open(r'/home/ubuntu/PycharmProjects/temp/opc_{}.py'.format(interface), 'a') as f:
    f.write('\n\n')
    f.write('run = client.get_node({})\nrun.set_value(True)\n'.format(value_run))
    f.write('nodes = []\n')
    if data[0]['opc_parameters']['actuators'] != None:
        for x in range(len(actuators_address)):
            tmp = actuators_address[x].split("; ")
            tmp2 = tmp[0].replace(" ", ";")
            f.write('{} = client.get_node("{}")\n'.format(actuators_name[x], tmp2))
            f.write('{}.set_value({})\n'.format(actuators_name[x], tmp[1]))

    f.write('\n\n')
    for x in range(len(sensors_address)):
        tmp = sensors_address[x].replace(" ", ";")
        f.write('{} = client.get_node("{}")\n'.format(sensors_name[x], tmp))
        f.write('nodes.append({})\n'.format(sensors_name[x]))

    f.write('\n\n')
    f.write('class SubHandler(object):\n')
    f.write('    def datachange_notification(self, node, val, data):\n')
    f.write('        val = round(val, 3)\n')
    f.write('        for idx, x in enumerate(nodes):\n')
    f.write('            if node == nodes[idx]:\n')
    f.write('                ad=idx*2\n')
    f.write("                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')")

    f.write('\n\n')
    f.write('handler = SubHandler()\n')
    f.write('sub = client.create_subscription(0, handler)\n')
    f.write('handle=sub.subscribe_data_change(nodes)\n')

f.close()

# ---------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT MODEL GENERATOR
if modeler == 'openmodelica':
    with open(r'/home/ubuntu/PycharmProjects/temp/script.sh'.format(model[0]), 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("mkdir /home/ubuntu/{}\n".format(model[0]))
        f.write("tar -C {}{} -xvf {}{}.tar.gz\n".format(path_dst_script, model[0], path_dst_script, model[0]))
        f.write(("cp /home/ubuntu/diagslave /home/ubuntu/{}\n".format(model[0])))
        f.write("cd {}{}/\n".format(path_dst_script, model[0]))
        f.write("{}{}/{} -embeddedServer=opc-ua -rt=1 &\n".format(path_dst_script, model[0], model[0]))
        if len(rtu) == 0:
            f.write("{}{}/diagslave -m tcp &\n".format(path_dst_script, model[0]))
        f.write("su -c 'python3 {}opc_{}.py' - ubuntu\n".format(path_dst_script, interface))
        f.write("exit 0")
    f.close()

#----------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT SELENIUM
if hmi[0] == 'scadabr':
    with open(r'/home/ubuntu/PycharmProjects/temp/script_selenium.py', 'w') as f:
        f.write("import selenium\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\nimport json\n")
        f.write("from selenium.webdriver.firefox.options import Options\n")
        f.write("options = Options()\noptions.headless = True\n")
        f.write("driver = webdriver.Firefox(options=options)\ndriver.implicitly_wait(30)\n")
        f.write('driver.get("http://localhost:8080/ScadaBR/login.htm")\n')
        f.write('element = driver.find_element_by_id("username")\nelement.send_keys("admin")\n')
        f.write('element = driver.find_element_by_id("password")\nelement.send_keys("admin")\n')
        f.write('element.send_keys(Keys.RETURN)\n')
        a = "'emport.shtm'"
        #b = "'watch_list.shtm'"
        b = "'views.shtm'"
        f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))
        f.write('data = driver.find_element_by_id("emportData")\n')
        f.write('with open("/home/ubuntu/data.json") as json_file:\n')
        f.write('    data_to_write = json.loads(json_file.read())\n')
        f.write('data.send_keys("{}".format(json.dumps(data_to_write)))\n')
        f.write('driver.find_element_by_id("importJsonBtn").click()\n')
        f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()'.format(b))
    f.close()


#driver.find_element_by_xpath("//a[contains(@href,"emport.shtm")]").click()
#data = driver.find_element_by_id("emportData")

#with open("/home/ubuntu/data.json") as json_file:
#    data_to_write = json.loads(json_file.read())

#data.send_keys("{}".format(json.dumps(data_to_write)))
#driver.find_element_by_id("importJsonBtn").click()

#driver.find_element_by_xpath("//a[contains(@href,"watch_list.shtm")]").click()


#---------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# DATA JSON GENERATOR
register_modbus = [0, 2, 4, 6, 8, 10]
dataSource_id = 'DS_074735'
if data[2]['name'] != None:
    host = ip_list[rtu[0] + '.eth0'][0]
else:
    host = ip_list[model[0] + '.eth0'][0]
data = {}
data['dataSources'] = []
data['dataSources'].append({
    'xid':dataSource_id,
    'type':'MODBUS_IP',
    'alarmLevels': {'POINT_WRITE_EXCEPTION':'NONE', 'DATA_SOURCE_EXCEPTION':'NONE', 'POINT_READ_EXCEPTION':'NONE'},
    'updatePeriodType':'SECONDS',
    'transportType':'TCP',
    'contiguousBatches': False,
    'createSlaveMonitorPoints':False,
    'enabled':True,
    'encapsulated':False,
    'host': host,
    'maxReadBitCount':2000,
    'maxReadRegisterCount':125,
    'maxWriteRegisterCount':120,
    'name':model[0],
    'port':502,
    'quantize':False,
    'retries':2,
    'timeout':500,
    'updatePeriods':1
})
data['dataPoints'] = []
for idx, x in enumerate(sensors_name) :
    data['dataPoints'].append({
        'xid':'DP_{}'.format(967000+idx),
        'loggingType':'ON_CHANGE',
        'intervalLoggingPeriodType':'MINUTES',
        'intervalLoggingType':'INSTANT',
        'purgeType':'YEARS',
        'pointLocator': {
            'range':'HOLDING_REGISTER',
            'modbusDataType':'FOUR_BYTE_FLOAT',
            'additive':0.0,
            'bit':0,
            'charset':'ASCII',
            'multiplier':1.0,
            'offset':register_modbus[idx],
            'registerCount':0,
            'settableOverride':False,
            'slaveId':1,
            'slaveMonitor':False
        },
        #'eventDetectors':[],
        'engineeringUnits':'',
        'chartColour':None,
        'chartRenderer':None,
        'dataSourceXid':dataSource_id,
        'defaultCacheSize':1,
        'deviceName':model[0],
        'discardExtremeValues':False,
        'discardHighLimit':1.7976931348623157E308,
        'discardLowLimit':-1.7976931348623157E308,
        'enabled':True,
        'intervalLoggingPeriod':15,
        'name':x,
        'purgePeriod':1,
        'textRenderer':{'type':'PLAIN','suffix':''},
        'tolerance':0.0
    })
children = {}
for idx, x in enumerate(sensors_name) :
    children.update({'point{}'.format(idx+1):'DP_{}'.format(967000+idx)})
data['graphicalViews'] = []
data['graphicalViews'].append({
    'user' :'admin',
    'anonymousAccess' :'NONE',
    'viewComponents' : [{
        'type':'IMAGE_CHART',
        'children': children,
        'durationType':'HOURS',
        'durationPeriods':1,
        'height':300,
        'name':'{}'.format(model[0]),
        'width':500,
        'x':120,
        'y':90
    }],
    'sharingUsers': [],
    'backgroundFilename': None,
    'name': '{}'.format(model[0]),
    'xid': 'GV_860000'
})
data['watchLists'] = []
data['watchLists'].append({
    'xid':'WL_558981',
    'user':'admin',
    'name':'(unnamed)'
})



with open('/home/ubuntu/PycharmProjects/temp/data.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=3)