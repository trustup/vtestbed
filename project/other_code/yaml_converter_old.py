import sys
import yaml

with open(r'/home/ubuntu/PycharmProjects/config1_4.yaml') as f:
    data = yaml.safe_load(f)

path_dst_script = "/home/ubuntu/"  # path destination script ON virtual machine
path_img = "/home/ubuntu/cyris/images"
path_models = "/home/ubuntu/cyris/models"
path = data[6]['path']  # path image files
numb_cyber = data[6]['cyber_range_id']

# HOST SETTING
host = [{'id': 'host_1', 'mgmt_addr': '192.168.1.27', 'virbr_addr': '192.168.122.1', 'account': 'ubuntu'}]
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
           'basevm_config_file': '{}/xubuntu.xml'.format(path_img), 'basevm_type': 'kvm',
           'tasks': [{'copy_content': [
               {'src': '{}/{}/{}.tar.gz'.format(path_models, model[0], model[0]), 'dst': '{}'.format(path_dst_script)},
               {'src': '{}/{}/interfaces/opc_{}.py'.format(path_models, model[0], interface),
                'dst': '{}'.format(path_dst_script)},
               {'src': '{}/{}/script.sh'.format(path_models, model[0]), 'dst': '{}'.format(path_dst_script)}
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
        gst = {'id': mtu[x], 'basevm_host': 'host_1', 'basevm_config_file': '{}/xubuntu.xml'.format(path_img),
               'basevm_type': 'kvm',
               'tasks' : [{'copy_content': [
                   {'src': '/home/ubuntu/data.json', 'dst': '{}'.format(path_dst_script)},
                   {'src': '/home/ubuntu/PycharmProjects/script_selenium.py', 'dst': '{}'.format(path_dst_script)}
               ]}]
               }

    guest.append(gst)

# RTU
rtu = []
if data[2]['name'] != None:
    rtu = data[2]['name'].split(", ")
    for x in rtu:
        gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, os[x]),
               'basevm_type': 'kvm'}
        guest.append(gst)

# GENERIC
generic = []
if data[3]['name'] != None:
    generic = data[3]['name'].split(", ")
    os = data[3]['os'].split(", ")
    for x in range(len(generic)):
        gst = {'id': generic[x], 'basevm_host': 'host_1',
               'basevm_config_file': '{}/image_{}.xml'.format(path_img, os[x]), 'basevm_type': 'kvm'}
        guest.append(gst)

    # FIREWALL
firewall = data[4]['name'].split(", ")
for x in firewall:
    gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_centos.xml'.format(path_img),
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
name_network = data[5]['name']
cc = name_network.split("; ")
cc[-1] = cc[-1].replace(";", "")  # elimino ";" dall'ultimo elemento della lista
members = data[5]['members']
gateway = data[5]['gateway']

#calcolo elementi in ogni rete (solo per il campo members poichè di firewall ce n'è uno per ogni ; )
stringa = members.split("; ")
len_str = len(stringa)
elements = []
for x in range(len_str):
    add = stringa[x].split(", ")
    elements.append(len(add))


def add_eth(stringToConvert):
    new_str = stringToConvert.replace("; ", ", ")
    new_str = new_str.split(", ")
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
for j in cc:
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

#print(ip_list)

total_number_vm = total_number_vm + firewall
total_number_vm = [x + ".eth0" for x in total_number_vm]  # solo eth0 perchè anche se una macchina ha 2 interfacce, basta che mi collego via ssh solo alla eth0
with open(r'/home/ubuntu/PycharmProjects/script_after_clone_restart.sh', 'w') as f:
    f.write("#!/bin/bash\n")
    for y in total_number_vm:
        exit = 0
        for x in firewall:
            if y == x + '.eth0':
                f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
                f.write("root@{} ".format(ip_list[y][0]))
                f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
                f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
                f.write("\n")
                exit = 1
        if y == model[0] + '.eth0' and exit == 0:
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT; iptables -P OUTPUT ACCEPT;')
            f.write('chmod +x /home/ubuntu/script.sh;')
            f.write('/home/ubuntu/script.sh &>/dev/null &"')
            f.write("\n")
        elif y == mtu[0] + '.eth0' and exit == 0:
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT; iptables -P OUTPUT ACCEPT;')
            f.write('python3 /home/ubuntu/script_selenium.py &>/dev/null &"')
            f.write("\n")
        elif y != model[0] + '.eth0' and exit == 0 and y != mtu[0] + '.eth0':
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y][1]))
            f.write('iptables -F;iptables -P INPUT ACCEPT; iptables -P OUTPUT ACCEPT"')
            f.write("\n")
    f.write("exit 0")
f.close()

with open(r'/home/ubuntu/PycharmProjects/script_after_clone.sh','w') as g:
    y = model[0] + '.eth0'
    g.write("#!/bin/bash\n")
    g.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
    g.write("root@{} ".format(ip_list[y][0]))
    g.write('"chmod +x /home/ubuntu/script.sh;')
    g.write('/home/ubuntu/script.sh &>/dev/null &"')
    g.write("\n")
    y = mtu[0] + '.eth0'
    g.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
    g.write("root@{} ".format(ip_list[y][0]))
    g.write('"python3 /home/ubuntu/script_selenium.py &>/dev/null &"')
    g.write("\n")
    g.write("exit 0")
g.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------
# OPC GENERATOR

url = data[0]['opc_parameters']['server']
# url = "opc.tcp://DESKTOP-ADCS5PF:4841"
address_modbus = ip_list[model[0] + '.eth0'][0]
# interface = data[1]['interface']

with open(r'/home/ubuntu/cyris/models/{}/interfaces/opc_{}.py'.format(model[0],interface), 'w') as f:
    f.write(
        "import threading\nimport time\nimport timeit\nimport opcua\nfrom opcua import Client\nfrom opcua import ua\n")
    f.write("import modbus_tk\nimport modbus_tk.defines as cst\nimport modbus_tk.modbus_tcp as modbus_tcp\n\n")
    f.write('url = "{}"\n'.format(url))
    f.write("client = Client(url)\nclient.connect()\n")
    f.write('master = modbus_tcp.TcpMaster(host="localhost", port=502)\n')

value_run = data[0]['opc_parameters']['run']

act = data[0]['opc_parameters']['actuators']
sens = data[0]['opc_parameters']['sensors']

# name actuators and sensors
actuators_name = [x for x in act]
sensors_name = [x for x in sens]
# address actuators and sensors
actuators_address = []
sensors_address = []
for i in act:
    actuators_address.append(act[i])
for i in sens:
    sensors_address.append(sens[i])

with open(r'/home/ubuntu/cyris/models/{}/interfaces/opc_{}.py'.format(model[0],interface), 'a') as f:
    f.write('\n\n')
    f.write('run = client.get_node({})\nrun.set_value(True)\n'.format(value_run))
    for x in range(len(actuators_address)):
        tmp = actuators_address[x].split("; ")
        tmp2 = tmp[0].replace(" ", ";")
        f.write('{} = client.get_node("{}")\n'.format(actuators_name[x], tmp2))
        f.write('{}.set_value({})\n'.format(actuators_name[x], tmp[1]))

    f.write('\n\n')
    for x in range(len(sensors_address)):
        tmp = sensors_address[x].replace(" ", ";")
        f.write('{} = client.get_node("{}")\n'.format(sensors_name[x], tmp))

    f.write('\n\n')
    for x in range(len(sensors_address)):
        f.write('class SubHandler{}(object):\n'.format(x + 1))
        f.write('    def datachange_notification(self, node, val, data):\n')
        f.write(
            "        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address={}, output_value=[val], data_format='>f')\n".format(
                x * 2))

    f.write('\n\n')
    for x in range(len(sensors_address)):
        f.write('handler{} = SubHandler{}()\n'.format(x + 1, x + 1))
        f.write('sub{} = client.create_subscription(0, handler{})\n'.format(x + 1, x + 1))
        f.write('handle{}=sub{}.subscribe_data_change({})\n\n'.format(x + 1, x + 1, sensors_name[x]))

f.close()

# ---------------------------------------------------------------------------------------------------------------------------
# SCRIPT MODEL GENERATOR
if modeler == 'openmodelica':
    with open(r'/home/ubuntu/cyris/models/{}/script.sh'.format(model[0]), 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("tar -C {} -xvf {}{}.tar.gz\n".format(path_dst_script, path_dst_script, model[0]))
        f.write("cd {}{}/\n".format(path_dst_script, model[0]))
        f.write("{}{}/{} -embeddedServer=opc-ua -rt=1 &\n".format(path_dst_script, model[0], model[0]))
        f.write("{}{}/diagslave -m tcp &\n".format(path_dst_script, model[0]))
        f.write("python3 {}opc_{}.py\n".format(path_dst_script, interface))
        f.write("exit 0")
    f.close()

#----------------------------------------------------------------------------------------------------------------------------
# SCRIPT SELENIUM
if hmi[0] == 'scadabr':
    with open(r'/home/ubuntu/PycharmProjects/script_selenium.py', 'w') as f:
        f.write("import selenium\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\nimport json\n")
        f.write("driver = webdriver.Firefox()\ndriver.implicitly_wait(30)\n")
        f.write('driver.get("http://localhost:8080/ScadaBR/login.htm")\n')
        f.write('element = driver.find_element_by_id("username")\nelement.send_keys("admin")\n')
        f.write('element = driver.find_element_by_id("password")\nelement.send_keys("admin")\n')
        f.write('element.send_keys(Keys.RETURN)\n')
        a = "'emport.shtm'"
        b = "'watch_list.shtm'"
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

