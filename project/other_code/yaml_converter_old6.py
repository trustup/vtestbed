import sys
import yaml
import json

with open(r'/home/ubuntu/PycharmProjects/config1_5.yaml') as f:
    data = yaml.safe_load(f)

IP_LOCAL = '192.168.1.68'
numb_cyber = data['CONFIG']['cyber_range_id']
path = data['CONFIG']['path']  # path cyris
dst_script_ubuntu = "/home/ubuntu/"  # path destination script ON virtual machine
dst_script_windows = 'C:\CyberRange'
path_img = "{}/cyris/images".format(path)
path_models = "{}/cyris/models".format(path)

# HOST SETTING
host = [{'id': 'host_1', 'mgmt_addr': IP_LOCAL, 'virbr_addr': '192.168.122.1', 'account': 'ubuntu'}]
#print(host)

# ----------------------------------------------------------------------------
# GUEST SECTION
guest = []

# MODEL
modeler = data[0]['modeler']
model = data[0]['name'].split()
model_os = data[0]['os'].split()
interface = data[0]['interface']
if modeler == 'openmodelica':
    if model_os[0] == 'windows.7':
        archive = '{}/{}/{}.zip'.format(path_models, model[0], model[0])
        dst = dst_script_windows
        dgs = '{}/diagslave.exe'.format(path_models)
        script = '{}/PycharmProjects/temp/script.bat'.format(path)
    else:
        archive = '{}/{}/{}.tar.gz'.format(path_models, model[0], model[0])
        dst = dst_script_ubuntu
        dgs = '{}/diagslave'.format(path_models)
        script = '{}/PycharmProjects/temp/script.sh'.format(path)
    gst = {'id': model[0], 'basevm_host': 'host_1',
           'basevm_config_file': '{}/image_{}.xml'.format(path_img, model_os[0].replace(".","")), 'basevm_type': 'kvm',
           'tasks': [{'copy_content': [
               {'src': archive, 'dst': '{}'.format(dst)},
               {'src': '{}/PycharmProjects/temp/opc_{}.py'.format(path, interface),
                'dst': '{}'.format(dst)},
               {'src': script, 'dst': '{}'.format(dst)},
               {'src': dgs, 'dst': '{}'.format(dst)}
           ]}]
           }
    if model_os[0] == 'windows.7':
        gst["basevm_os_type"] = "windows.7"
        gst['tasks'][0]['copy_content'].append({'src':'{}/PycharmProjects/temp/script2.sh'.format(path), 'dst':dst_script_windows})
    guest.append(gst)


# MTU
mtu = data[1]['name'].replace(" ","").split(",")
hmi = data[1]['hmi'].replace(" ","").split(",")
hmi_os = data[1]['os'].replace(" ","").split(",")

for x in range(len(mtu)):
    if hmi[x] == 'scadabr':
        if hmi_os[x] == 'windows.7':
            #dest1, dest2 = 'C:/CyberRange', 'C:/CyberRange'  #destination script
            dst = dst_script_windows
        else:
            #dest1, dest2 = dst_script_ubuntu, '/var/lib/tomcat8/webapps/ScadaBR/uploads/'
            dst = dst_script_ubuntu
        gst = {'id': mtu[x], 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, hmi_os[x].replace(".","")),
               'basevm_type': 'kvm',
               'tasks' : [{'copy_content': [
                   {'src': '/home/ubuntu/PycharmProjects/temp/data.json', 'dst': '{}'.format(dst)},
                   {'src': '/home/ubuntu/PycharmProjects/temp/script_selenium.py', 'dst': '{}'.format(dst)},
                   {'src': '{}/{}/{}.png'.format(path_models, model[0], model[0]), 'dst': dst}
               ]}]
               }
    if hmi_os[x] == 'windows.7':
        gst["basevm_os_type"] = "windows.7"
    guest.append(gst)


# RTU
rtu = []
if data[2]['name'] != None:
    rtu = data[2]['name'].replace(" ","").split(",")
    rtu_os = data[2]['os'].replace(" ","").split(",")
    for idx, x in enumerate(rtu):
        gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, rtu_os[idx]),
               'basevm_type': 'kvm',
               'tasks': [{'copy_content': [
                   {'src': '{}/diagslave'.format(path_models), 'dst': '{}'.format(dst_script_ubuntu)}
               ]}]
               }
        guest.append(gst)

# GENERIC
generic = []
if data[3]['name'] != None:
    generic = data[3]['name'].replace(" ","").split(",")
    os = data[3]['os'].replace(" ","").split(",")
    for idx, x in enumerate(generic):
        gst = {'id': x, 'basevm_host': 'host_1',
               'basevm_config_file': '{}/image_{}.xml'.format(path_img, os[idx]), 'basevm_type': 'kvm',
               'tasks': [{'copy_content': [
                   {'src': '{}/{}/storyboard'.format(path_models, model[0]), 'dst': '/root/Scrivania'}
               ]}]
               }
        guest.append(gst)

# FIREWALL
firewall = data[4]['name'].replace(" ","").split(",")
fw_os = data[4]['os'].replace(" ","").split(",")
for idx, x in enumerate(firewall):
    gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, fw_os[idx]),
           'basevm_type': 'kvm'}
    guest.append(gst)

# -----------------------------------------------------------------------------
# CLONE SETTINGS
clone_guest = []

# SECTION GUESTS
total_number_vm = model + mtu + rtu + generic
entry_point = data['CONFIG']['entry_point']

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
name_network = data[5]['name'].replace(" ","").split(";")
#cc = name_network.split("; ")
name_network[-1] = name_network[-1].replace(";", "")  # elimino ";" dall'ultimo elemento della lista
members = data[5]['members'].replace(" ","")
gateway = data[5]['gateway'].replace(" ","")

#calcolo elementi in ogni rete (solo per il campo members poichè di firewall ce n'è uno per ogni ; )
stringa = members.replace(" ","").split(";")
len_str = len(stringa)
elements = []
for x in range(len_str):
    add = stringa[x].replace(" ","").split(",")
    elements.append(len(add))


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

range_id = data['CONFIG']['cyber_range_id']
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

#manage security level
vuln = []
target = []
fix = []
if data[7]['vulnerability'] != None:
    vuln = data[7]['vulnerability'].replace(" ","").split(";")
    target = data[7]['target'].replace(" ","").split(";")
    for idx, x in enumerate(vuln):
        if x == 'ssh_root_deny' :
            fix.append("sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config;echo 'Match Host {}.1.1.1' >> /etc/ssh/sshd_config;echo '    PermitRootLogin yes' >> /etc/ssh/sshd_config;/etc/init.d/ssh restart".format(numb_cyber))
        elif x == 'altra' :
            fix.append('comando fix 2')

def check_target(insert_target) :
    if len(vuln) != 0:
        command = ''
        for idx, x in enumerate(vuln):
            tmp = target[idx].split(",")
            for x in tmp:
                if insert_target == x :
                    tt = fix[idx] + ";"
                else: continue
                command = command + tt
        return command


total_number_vm2 = total_number_vm + firewall
#total_number_vm2 = [x + ".eth0" for x in total_number_vm2]  # solo eth0 perchè anche se una macchina ha 2 interfacce, basta che mi collego via ssh solo alla eth0

with open(r'/home/ubuntu/PycharmProjects/temp/script_after_clone.sh','w') as f:
    f.write("#!/bin/bash\n")

    if len(rtu) != 0:
        for y in rtu:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            #f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write('"')
            ck = check_target(y)
            if ck != None: f.write(ck)
            f.write("{}diagslave -m tcp".format(dst_script_ubuntu))
            f.write(" &>/dev/null &")
            f.write('"\n')

    #MODEL, CASE WINDOWS - UBUNTU
    if model_os[0] == 'windows.7':
        f.write("# {}\n".format(model[0]))
        f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("seven@{} ".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"')
        f.write(r"C:\CyberRange\psexec \\\\{} -d -i C:\CyberRange\script.bat".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"\n')
    else:
        f.write("# {}\n".format(model[0]))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
        # f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
        f.write('"')
        ck = check_target(model[0])
        if ck != None: f.write(ck)
        f.write('chmod +x /home/ubuntu/script.sh;')
        f.write('/home/ubuntu/script.sh &>/dev/null &')
        f.write('"\n')

    #MTU, CASE WINDOWS - UBUNTU
    if hmi_os[0] == 'windows.7':
        f.write("# {}\n".format(mtu[0]))
        f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("seven@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
        f.write("'")
        f.write('move C:\CyberRange\{}.png "C:\Program Files\ScadaBR\webapps\ScadaBR\\uploads"'.format(model[0]))
        f.write(' && cd C:\CyberRange && python script_selenium.py')
        f.write("'\n")
    else:
        f.write("# {}\n".format(mtu[0]))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
        # f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
        f.write('"')
        ck = check_target(mtu[0])
        if ck != None: f.write(ck)
        if hmi[0] == 'scadabr' : f.write('mv {}{}.png /var/lib/tomcat8/webapps/ScadaBR/uploads/;'.format(dst_script_ubuntu, model[0]))
        f.write('systemctl enable tomcat8 &>/dev/null;systemctl start tomcat8 &>/dev/null;sleep 10;')
        # f.write('"su -c')
        f.write("su -c 'python3 /home/ubuntu/script_selenium.py' - ubuntu")
        f.write(' &>/dev/null')
        f.write('"\n')


    for y in firewall:
        f.write("# {}\n".format(y))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
        # f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
        #f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
        f.write('"')
        ck = check_target(y)
        if ck != None: f.write(ck)
        f.write("iptables-save > /bin/cyberrange/initif/iptables.conf;")
        # if sec_lev != 'low':
        #     f.write("sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config;")
        #     f.write("echo 'Match Host 100.1.1.1' >> /etc/ssh/sshd_config;")
        #     f.write("echo '    PermitRootLogin yes' >> /etc/ssh/sshd_config;/etc/init.d/ssh restart")
        f.write('"')
        f.write("\n")
f.close()



with open(r'/home/ubuntu/PycharmProjects/temp/script_after_clone_restart.sh','w') as f:
    f.write("#!/bin/bash\n")

    if len(rtu) != 0:
        for y in rtu:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[y + '.eth0'][1]))
            #f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write("{}diagslave -m tcp".format(dst_script_ubuntu))
            f.write(' &>/dev/null &"\n')

    #MODEL RESTART - WINDOWS,UBUNTU
    if model_os[0] == 'windows.7':
        f.write("# {}\n".format(model[0]))
        f.write('sleep 20\n')
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"route delete 0.0.0.0 mask 0.0.0.0"\n')
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"route add 0.0.0.0 mask 0.0.0.0 {}"\n'.format(ip_list[model[0] + '.eth0'][1]))
        f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("seven@{} ".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"')
        f.write(r"C:\CyberRange\psexec \\\\{} -d -i C:\CyberRange\script.bat".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"\n')
        f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("seven@{} ".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"')
        f.write(r"C:\CyberRange\psexec \\\\{} -d -i C:\CyberRange\script2.bat".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"\n')
    else:
        f.write("# {}\n".format(model[0]))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
        f.write('"route add default gw {} eth0;'.format(ip_list[model[0] + '.eth0'][1]))
        # f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
        f.write('chmod +x /home/ubuntu/script.sh;')
        f.write('/home/ubuntu/script.sh &>/dev/null &"')
        f.write("\n")

    #MTU RESTART - WINDOWS,UBUNTU
    f.write("# {}\n".format(mtu[0]))
    if hmi_os[0] == 'windows.7' :
        f.write('sleep 20\n')
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
        #f.write('"route -p change 0.0.0.0 mask 0.0.0.0 {}'.format(ip_list[mtu[0] + '.eth0'][1]))
        f.write('"route delete 0.0.0.0 mask 0.0.0.0"\n')
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
        f.write('"route add 0.0.0.0 mask 0.0.0.0 {}"\n'.format(ip_list[mtu[0] + '.eth0'][1]))
    else:
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
        f.write('"route add default gw {} eth0'.format(ip_list[mtu[0] + '.eth0'][1]))
        f.write('"\n')

    if len(generic) != 0:
        for y in generic:
            f.write("# {}\n".format(y))
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
            f.write('"route add default gw {} eth0'.format(ip_list[y + '.eth0'][1]))
            #f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
            f.write('"\n')

    for y in firewall:
        f.write("# {}\n".format(y))
        f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
        f.write("root@{} ".format(ip_list[y + '.eth0'][0]))
        f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward"')
        #f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
        f.write("\n")
f.close()


# ------------------------------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# OPC GENERATOR
sensors = data[0]['opc_parameters']['sensors'].replace(" ","").split(",")
actuators = []
if  data[0]['opc_parameters']['actuators'] != None:
    actuators = data[0]['opc_parameters']['actuators'].replace(" ","").replace(", ","").split(",")
    actuators = [x.split("=") for x in actuators]
url = "opc.tcp://localhost:4841" #nell'ipotesi che il server OPC sia sulla stessa macchina del client(script python)

if data[2]['name'] != None:
    address_modbus = ip_list[rtu[0] + '.eth0'][0]
else:
    address_modbus = 'localhost'
# interface = data[1]['interface']

with open(r'/home/ubuntu/PycharmProjects/temp/opc_{}.py'.format(interface), 'w') as f:
    f.write("import time\nimport timeit\nimport opcua\nfrom opcua import Client\nfrom opcua import ua\n")
    f.write("import modbus_tk\nimport modbus_tk.defines as cst\nimport modbus_tk.modbus_tcp as modbus_tcp\n\n")
    f.write('class SubHandler(object):\n')
    f.write('    def datachange_notification(self, node, val, data):\n')
    f.write('        for idx, x in enumerate(nodes):\n')
    f.write('            if node == nodes[idx]:\n')
    f.write('                ad=idx*2\n')
    f.write("                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')\n\n")

    f.write('if __name__ == "__main__":\n\n')
    f.write('    master = modbus_tcp.TcpMaster(host="{}", port=502)\n'.format(address_modbus))
    f.write('    url = "{}"\n'.format(url))
    f.write("    client = Client(url, timeout=100)\n    client.connect()\n\n")
    f.write('    nodes = []\n')
    f.write('    root = client.get_objects_node()\n')
    f.write('    obj = client.get_node(root)\n')
    f.write("    run = obj.get_child('1:OpenModelica.run')\n")
    f.write('\n   #sensors:\n')

    for idx, x in enumerate(sensors):
        f.write("    node{} = obj.get_child('1:{}')\n".format(idx+1, x))
        f.write("    nodes.append(node{})\n".format(idx+1))
    f.write("    len_sensors = {}\n".format(len(sensors)))
    f.write('    run.set_value(True)\n')
    if len(actuators) != 0:
        f.write("    act=[]\n")
        f.write("    ad = (len_sensors * 2) - 2\n")
        for idx, x in enumerate(actuators):
            f.write("   #actuator {}\n".format(idx + 1))
            f.write("    node{} = obj.get_child('1:{}')\n".format(idx + 1 + len(sensors), x[0]))
            f.write("    node{}.set_value({})\n".format(idx + 1 + len(sensors), x[1]))
            f.write('    act.append({})\n'.format(x[1]))
            f.write("    ad = ad + 2\n")
            f.write("    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[{}], data_format='>f')\n".format(x[1]))

    f.write("\n    try:\n")
    f.write('        handler = SubHandler()\n')
    f.write('        sub = client.create_subscription(0, handler)\n')
    f.write('        handle=sub.subscribe_data_change(nodes)\n')
    f.write('        time.sleep(0.1)\n')

    if len(actuators) != 0:
        f.write("\n        while True:\n")
        f.write("            for idx, x in enumerate(act):\n")
        f.write("                r_a = (len_sensors * 2) + (idx * 2)\n")
        f.write("                a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')\n")
        f.write("                if a[0] != act[idx]:\n")
        f.write("                    nodd = globals()['node{}'.format(len_sensors + 1 + idx)]\n")
        f.write("                    nodd.set_value(a[0])\n")
        f.write("                    act[idx] = a[0]\n")
        f.write("                time.sleep(1)\n")

    f.write("\n    finally:\n")
    f.write("        print('..retry')\n")

    f.close()

# sensors = data[0]['opc_parameters']['sensors'].replace(", ",",").split(",")
# actuators = []
# if  data[0]['opc_parameters']['actuators'] != None:
#     actuators = data[0]['opc_parameters']['actuators'].replace(" ","").replace(", ","").split(",")
#     actuators = [x.split("=") for x in actuators]
#
# with open(r'/home/ubuntu/PycharmProjects/temp/opc_{}.py'.format(interface), 'a') as f:
#     f.write('\n\n')
#     #f.write('run = client.get_node({})\nrun.set_value(True)\n'.format(value_run))
#     f.write('nodes = []\n')
#     f.write('root = client.get_objects_node()\n')
#     f.write('obj = client.get_node(root)\n')
#     f.write("run = obj.get_child('1:OpenModelica.run')")
#
#     f.write('\n\n#sensors:\n')
#     for idx, x in enumerate(sensors):
#         f.write("node{} = obj.get_child('1:{}')\n".format(idx+1, x))
#         f.write("nodes.append(node{})\n".format(idx+1))
#     f.write("len_sensors = {}\n".format(len(sensors)))
#
#     f.write('\n#actuators:\n')
#     f.write('act=[]\n')
#     f.write('run.set_value(True)\n')
#     if len(actuators) != 0:
#         for idx, x in enumerate(actuators):
#             f.write(" #actuator {}\n".format(idx + 1))
#             f.write("node{} = obj.get_child('1:{}')\n".format(idx + 1 + len(sensors), x[0]))
#             f.write("node{}.set_value({})\n".format(idx + 1 + len(sensors), x[1]))
#             f.write("nodes.append(node{})\n".format(idx + 1 + len(sensors)))
#             f.write('act.append({})\n'.format(x[1]))
#
#     f.write('\n')
#     f.write('class SubHandler(object):\n')
#     f.write('    def datachange_notification(self, node, val, data):\n')
#     f.write('        val = round(val, 3)\n')
#     f.write('        for idx, x in enumerate(nodes):\n')
#     f.write('            if node == nodes[idx]:\n')
#     f.write('                ad=idx*2\n')
#     f.write("                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')")
#
#     f.write("\n\ndef read():\n")
#     f.write("    threading.Timer(1, read).start()\n")
#     f.write("    for idx, x in enumerate(act):\n")
#     f.write("        r_a = (len_sensors * 2) + (idx * 2)\n")
#     f.write("        a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')\n")
#     f.write("        if a[0] != act[idx]:\n")
#     f.write("            node[len_sensors + 1 + idx].set_value(a[0])\n")
#     f.write("            act[idx] = a[0]\n")
#
#
#     f.write('\n\n')
#     f.write('handler = SubHandler()\n')
#     f.write('sub = client.create_subscription(0, handler)\n')
#     f.write('handle=sub.subscribe_data_change(nodes)\n')
#     f.write('\nif len(act) != 0:\n')
#     f.write("    read()")

f.close()

# ---------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT MODEL GENERATOR
if modeler == 'openmodelica':
    if model_os[0] == 'windows.7':
        with open(r'/home/ubuntu/PycharmProjects/temp/script.bat'.format(model[0]), 'w') as f:
            f.write("cd C:\CyberRange && unzip -n tankmodel.zip -d C:\CyberRange\modelica && copy /y diagslave.exe C:\CyberRange\modelica && cd C:\CyberRange\modelica\n")
            f.write(r"START /B C:\CyberRange\modelica\tankmodel -embeddedServer=opc-ua -rt=1 >null")
            if len(rtu) == 0:
                f.write("\nSTART /B C:\CyberRange\modelica\diagslave -m tcp >null2")
            #f.write("\ncd C:\CyberRange && START /B python opc_{}.py".format(interface))
        with open(r'/home/ubuntu/PycharmProjects/temp/script2.bat'.format(model[0]), 'w') as f:
            f.write("cd C:\CyberRange\n")
            f.write("python opc_modbus.py >null3")
    else:
        with open(r'/home/ubuntu/PycharmProjects/temp/script.sh'.format(model[0]), 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("mkdir /home/ubuntu/{}\n".format(model[0]))
            f.write("tar -C {}{} -xvf {}{}.tar.gz\n".format(dst_script_ubuntu, model[0], dst_script_ubuntu, model[0]))
            f.write(("cp /home/ubuntu/diagslave /home/ubuntu/{}\n".format(model[0])))
            f.write("cd {}{}/\n".format(dst_script_ubuntu, model[0]))
            f.write("{}{}/{} -embeddedServer=opc-ua -rt=1 &\n".format(dst_script_ubuntu, model[0], model[0]))
            if len(rtu) == 0:
                f.write("{}{}/diagslave -m tcp &\n".format(dst_script_ubuntu, model[0]))
            f.write("su -c 'python3 {}opc_{}.py' - ubuntu\n".format(dst_script_ubuntu, interface))
            f.write("exit 0")
        f.close()


#----------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT SELENIUM
login_user='admin'
login_pass='$admin$'
if hmi[0] == 'scadabr':
    with open(r'/home/ubuntu/PycharmProjects/temp/script_selenium.py', 'w') as f:
        f.write("import selenium\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\nimport json\n")
        f.write("from selenium.webdriver.firefox.options import Options\n")
        f.write("options = Options()\noptions.headless = True\n")
        if hmi_os[0] != 'windows.7' :
            f.write("driver = webdriver.Firefox(options=options)\ndriver.implicitly_wait(30)\n")
        else :
            f.write("driver = webdriver.Firefox(options=options, executable_path=r'C:\CyberRange\geckodriver.exe')\ndriver.implicitly_wait(30)\n")
        f.write('driver.get("http://localhost:8080/ScadaBR/login.htm")\n')
        f.write('element = driver.find_element_by_id("username")\nelement.send_keys("{}")\n'.format(login_user))
        f.write('element = driver.find_element_by_id("password")\nelement.send_keys("{}")\n'.format(login_pass))
        f.write('element.send_keys(Keys.RETURN)\n')
        a = "'emport.shtm'"
        #b = "'watch_list.shtm'"
        b = "'data_sources.shtm'"
        f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))
        f.write('data = driver.find_element_by_id("emportData")\n')
        if hmi_os[0] != 'windows.7':
            f.write('with open("/home/ubuntu/data.json") as json_file:\n')
        else:
            f.write("with open(r'C:\CyberRange\data.json') as json_file:\n")
        f.write('    data_to_write = json.loads(json_file.read())\n')
        f.write('data.send_keys("{}".format(json.dumps(data_to_write)))\n')
        f.write('driver.find_element_by_id("importJsonBtn").click()\n')
    f.close()



#---------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# DATA JSON GENERATOR
register_modbus = [0, 2, 4, 6, 8, 10, 12]
dataSource_id = 'DS_074735'
if data[2]['name'] != None:
    host = ip_list[rtu[0] + '.eth0'][0]
else:
    host = ip_list[model[0] + '.eth0'][0]

#manage alert:
eventDetector = []
variable_alert = []
type_alert = []
#values_alert = []
if data[1]['set_alert']['type'] != None:
    tp = data[1]['set_alert']['type'].upper()
    type_alert.append(tp)
    for idx, y in enumerate(type_alert):
        if y == 'HIGH_LIMIT':
            vr = data[1]['set_alert']['variable'].replace(" ", "").split(">")
            variable_alert.append(vr[0])
            eventDetector.append({'xid':'PED_{}'.format(980000+idx),
                                  'type':y,
                                  'alarmLevel': 'URGENT',
                                  'limit':float(vr[1]),
                                  "durationType": "SECONDS",
                                  "duration": 2,
                                  "alias":y})
        if y == 'LOW_LIMIT':
            vr = data[1]['set_alert']['variable'].replace(" ", "").split("<")
            variable_alert.append(vr[0])
            eventDetector.append({'xid':'PED_{}'.format(980000+idx),
                                  'type':y,
                                  'alarmLevel': 'URGENT',
                                  'limit':float(vr[1]),
                                  "durationType": "SECONDS",
                                  "duration": 2,
                                  "alias":y})
        if y == 'CHANGE':
            vr = data[1]['set_alert']['variable'].replace(" ", "")
            variable_alert.append(vr)
            eventDetector.append({'xid':'PED_{}'.format(980000+idx),
                                  'type':"POINT_CHANGE",
                                  'alarmLevel': 'URGENT',
                                  "alias":"change"})
        if y == 'NO_CHANGE':
            vr = data[1]['set_alert']['variable'].replace(" ", "")
            variable_alert.append(vr)
            eventDetector.append({'xid':'PED_{}'.format(980000+idx),
                                  'type':"POINT_CHANGE",
                                  'alarmLevel': 'URGENT',
                                  "durationType": "SECONDS",
                                  "duration": 2,
                                  "alias":"change"})

#------------------------------------data sources----------------------------------
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
#-----------------------------data points-------------------------------------


data['dataPoints'] = []
for idx, x in enumerate(sensors) :
    event = []
    for idxx, xx in enumerate(variable_alert):
        if x == xx :
            event.append(eventDetector[idxx])
        else : event.clear()
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
        'eventDetectors': event,
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
if len(actuators) != 0:
    for idx, x in enumerate(actuators):
        data['dataPoints'].append({
            'xid': 'DP_{}'.format(967000 + idx + len(sensors)),
            'loggingType': 'ON_CHANGE',
            'intervalLoggingPeriodType': 'MINUTES',
            'intervalLoggingType': 'INSTANT',
            'purgeType': 'YEARS',
            'pointLocator': {
                'range': 'HOLDING_REGISTER',
                'modbusDataType': 'FOUR_BYTE_FLOAT',
                'additive': 0.0,
                'bit': 0,
                'charset': 'ASCII',
                'multiplier': 1.0,
                'offset': register_modbus[idx + len(sensors)],
                'registerCount': 0,
                'settableOverride': True,
                'slaveId': 1,
                'slaveMonitor': False
            },
            'eventDetectors':[],
            'engineeringUnits': '',
            'chartColour': None,
            'chartRenderer': None,
            'dataSourceXid': dataSource_id,
            'defaultCacheSize': 1,
            'deviceName': model[0],
            'discardExtremeValues': False,
            'discardHighLimit': 1.7976931348623157E308,
            'discardLowLimit': -1.7976931348623157E308,
            'enabled': True,
            'intervalLoggingPeriod': 15,
            'name': x[0],
            'purgePeriod': 1,
            'textRenderer': {'type': 'PLAIN', 'suffix': ''},
            'tolerance': 0.0
        })

#----------------------------------graphical views-----------------------------------
graphical_pages = sensors ###NOTA: viene aggiornato anche sensors non solo graphical_pages
if len(actuators) != 0:
    for idx, x in enumerate(actuators):
        graphical_pages.append(x[0])

viewComponents = [] #for main page
for idx, y in enumerate(graphical_pages):
    viewComponents.append({
        "type": "HTML",
        "content": "<a href=\"http://localhost:8080/ScadaBR/views.shtm?viewId={}\"><IMG SRC=\"uploads\/btn.png\" BORDER=\"0\"></a></img></A>".format(2+idx),
        "x": 30+(100*idx),
        "y": 15
    })
    viewComponents.append({
        "type": "LINK",
        "content": "<a href='http://localhost:8080/ScadaBR/views.shtm?viewId={}'>{}</a>".format(2+idx, y),
        "link": "http://localhost:8080/ScadaBR/views.shtm?viewId={}".format(2+idx),
        "text": "{}".format(y),
        "x": 30+(100*idx),
        "y": 55
    })

data['graphicalViews'] = []
data['graphicalViews'].append({ #MAIN PAGE
        'user': 'admin',
        'anonymousAccess': 'NONE',
        'viewComponents': viewComponents,
        'sharingUsers': [{"user":"user","accessType":"READ"}],
        'backgroundFilename': "uploads\\/{}.png".format(model[0]),
        'name': "{}".format(model[0]),
        'xid': "GV_360000"
    })
for idx, y in enumerate(graphical_pages) :
    data['graphicalViews'].append({ #SENSORS AND ACTUATORS PAGE
        'user': 'admin',
        'anonymousAccess': 'NONE',
        'viewComponents': [{
            "type": "IMAGE_CHART",
            "children": { "point1":"DP_96700{}".format(idx)},
            "durationType": "HOURS",
            "durationPeriods": 1,
            "height": 300,
            "name": "{}".format(y),
            "width": 500,
            "x": 100,
            "y": 40
        },{
            "type": "SIMPLE",
            "dataPointXid": "DP_96700{}".format(idx),
            "bkgdColorOverride": "",
            "displayControls": False,
            "displayPointName": True,
            "nameOverride": "",
            "settableOverride": False,
            "styleAttribute": "",
            "x": 290,
            "y": 350
        },{
            "type": "HTML",
            "content": "<a href=\"http://localhost:8080/ScadaBR/views.shtm?viewId=1\"><IMG SRC=\"uploads\\/btn.png\" BORDER=\"0\"></a></img></A>",
            "x": 350,
            "y": 386
        },{
            "type": "LINK",
            "content": "<a href='http://localhost:8080/ScadaBR/views.shtm?viewId=1'>Go To Model</a>",
            "link": "http://localhost:8080/ScadaBR/views.shtm?viewId=1",
            "text": "Go To Model",
            "x": 341,
            "y": 428
        }
        ],
        'sharingUsers': [{"user":"user","accessType":"READ"}],
        'backgroundFilename': None,
        'name': y,
        'xid': "GV_36000{}".format(idx+1)
    })


#--------------------------watch lists---------------------------------------------
data['watchLists'] = []
data['watchLists'].append({
    'xid':'WL_558981',
    'user':'admin',
    'name':'(unnamed)'
})

#------------------------------users-----------------------------------------------
#bisognerebbe fare un for per sensors e uno per actuators, ma nelle righe precedenti l'ho gia fatto per graphical_pages, uso quello
#nota: sensors anche è cambiato assieme a graphical pages
dataPointPermissions = []
for idx, x in enumerate(graphical_pages) :
    dataPointPermissions.append({
        "dataPointXid": "DP_{}".format(967000+idx),
        "permission": "READ"
    })

data['users'] = []
data['users'].append({
         "admin":True,
         "disabled":False,
         "email":"admin@yourMangoDomain.com",
         "homeUrl":"",
         "password":"wUt32hShc6WTwurKth9wRWKq9Gs=",
         "phone":"",
         "receiveOwnAuditEvents":False,
         "username":"admin"
})
data['users'].append({
    "dataSourcePermissions":[],
    "dataPointPermissions": dataPointPermissions,
    "admin": False,
    "disabled": False,
    "email": "u@u.com",
    "homeUrl": "",
    "password": "8ibT1VOTbHjV4OlGfg622j2yJBg=",
    "phone": "0000000",
    "receiveOwnAuditEvents": False,
    "username": "user"
})




with open('/home/ubuntu/PycharmProjects/temp/data.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=3)