import yaml
import os as oscommand

import model_script
import selenium_script
import opc_generator
import plc_configuration
import json_generator
import rtu_code_generator
import after_clone
import operations
import logstash_conf
import filebeat_config

with open(r'/home/ubuntu/PycharmProjects/yaml_demo2.yml') as f:
    data = yaml.safe_load(f)

#format yaml via websocket
#data = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0.6, input2=0.3, PLC=0.5', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': '', 'variable': ''}}, 'RTU': {'name': '', 'os': '', 'input': ''}, 'PLC': {'name': '', 'os': '', 'input': '', 'output_slave': '', 'plc_code': ''}, 'GENERIC': {'name': '', 'os': ''}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': '', 'target': ''}, 'EXPORT_DATA': {'name': '', 'ip_server': '', 'source_data': '', 'log_type': ''}}
#data = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0, input2=0, PLC=0', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}

#print(data)
IP_HOST = '192.168.1.68'
numb_cyber = data['CONFIG']['cyber_range_id']
path = data['CONFIG']['path']  # path cyris
path = operations.replace_path(path)
dst_script_ubuntu = "/home/ubuntu/"  # path destination script ON virtual machine
dst_script_windows = 'C:\CyberRange'
path_img = "{}/cyris/images".format(path)
path_models = "{}/cyris/models".format(path)

oscommand.system("rm -r /home/ubuntu/PycharmProjects/temp/{}; mkdir /home/ubuntu/PycharmProjects/temp/{}".format(numb_cyber, numb_cyber))
path_temp_script = '/home/ubuntu/PycharmProjects/temp/{}'.format(numb_cyber)

exp = []
exp = data['EXPORT_DATA']['name']
ip_export = []
source = []
log_type = []
if exp != None:
#if len(exp) != 0 or exp != None:
    ip_export = data['EXPORT_DATA']['ip_server']
    source = data['EXPORT_DATA']['source_data'].replace(" ", "").split(",")
    log_type = data['EXPORT_DATA']['log_type'].replace(" ", "").split(";")

# HOST SETTING
host = [{'id': 'host_1', 'mgmt_addr': IP_HOST, 'virbr_addr': '192.168.122.1', 'account': 'ubuntu'}]
#print(host)

# ----------------------------------------------------------------------------
# GUEST SECTION
guest = []

# MODEL
modeler = data['MODEL']['modeler']
model = data['MODEL']['name'].split()
model_os = data['MODEL']['os'].split()
interface = data['MODEL']['interface']
if modeler == 'openmodelica':
    if model_os[0] == 'windows.7':
        archive = '{}/{}/{}.zip'.format(path_models, model[0], model[0])
        dst = dst_script_windows
        #dgs = '{}/diagslave.exe'.format(path_models)
        script = '{}/script.bat'.format(path_temp_script)
    else:
        archive = '{}/{}/{}.tar.gz'.format(path_models, model[0], model[0])
        dst = dst_script_ubuntu
        #dgs = '{}/diagslave'.format(path_models)
        script = '{}/script.sh'.format(path_temp_script)
    gst = {'id': model[0], 'basevm_host': 'host_1',
           'basevm_config_file': '{}/image_{}.xml'.format(path_img, model_os[0].replace(".","")), 'basevm_type': 'kvm',
           'tasks': [{'copy_content': [
               {'src': archive, 'dst': '{}'.format(dst)},
               {'src': '{}/opc_{}.py'.format(path_temp_script, interface),
                'dst': '{}'.format(dst)},
               {'src': '{}/{}.py'.format(path_temp_script, interface), 'dst': '{}'.format(dst)},
               {'src': script, 'dst': '{}'.format(dst)}
               #{'src': dgs, 'dst': '{}'.format(dst)}
           ]}]
           }
    if operations.control_source_log(model[0],source) == True:
        gst['tasks'][0]['copy_content'].append({'src': '{}/filebeat_{}.yml'.format(path_temp_script, model[0]), 'dst': dst})
    if model_os[0] == 'windows.7':
        gst["basevm_os_type"] = "windows.7"
        #gst['tasks'][0]['copy_content'].append({'src':'{}/PycharmProjects/temp/script2.sh'.format(path), 'dst':dst_script_windows})
    guest.append(gst)


# MTU
mtu = data['MTU']['name'].replace(" ","").split(",")
hmi = data['MTU']['hmi'].replace(" ","").split(",")
hmi_os = data['MTU']['os'].replace(" ","").split(",")
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
                   {'src': '{}/data.json'.format(path_temp_script), 'dst': '{}'.format(dst)},
                   {'src': '{}/script_selenium.py'.format(path_temp_script), 'dst': '{}'.format(dst)},
                   {'src': '{}/{}/{}.png'.format(path_models, model[0], model[0]), 'dst': dst}
               ]}]
               }
    if operations.control_source_log(mtu[0],source) == True:
        gst['tasks'][0]['copy_content'].append({'src': '{}/filebeat_{}.yml'.format(path_temp_script, mtu[0]), 'dst': dst})
    if hmi_os[x] == 'windows.7':
        gst["basevm_os_type"] = "windows.7"
    guest.append(gst)


# RTU
rtu = []
rtu_os = []
if data['RTU']['name'] != None:
#if len(data['RTU']['name']) != 0:
    rtu = data['RTU']['name'].replace(" ","").split(",")
    rtu_os = data['RTU']['os'].replace(" ","").split(",")
    for idx, x in enumerate(rtu):
        gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, rtu_os[idx]),
               'basevm_type': 'kvm',
               'tasks': [{'copy_content': [
                   #{'src': '{}/diagslave'.format(path_models), 'dst': '{}'.format(dst_script_ubuntu)}
                   {'src': '{}/code_{}.py'.format(path_temp_script,x), 'dst': '{}'.format(dst_script_ubuntu)}
               ]}]
               }
        if operations.control_source_log(x, source) == True:
            gst['tasks'][0]['copy_content'].append({'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst})
        guest.append(gst)

# PLC
plc = []
plc_os = []
plc_code = []
if data['PLC']['name'] != None:
#if len(data['PLC']['name']) != 0:
    plc = data['PLC']['name'].replace(" ", "").split(",")
    plc_os = data['PLC']['os'].replace(" ", "").split(",")
    #slave_conf =
    plc_code = data['PLC']['plc_code'].replace(" ", "").split(",")
    for idx, x in enumerate(plc):
        gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, plc_os[idx]),
               'basevm_type': 'kvm',
               'tasks': [{'copy_content': [
                   {'src': '{}/cyris/PLC/{}/mbconfig.cfg'.format(path, idx+1), 'dst': '/bin/cyberrange/OpenPLC_v3/webserver'},
                   {'src': '{}/cyris/PLC/{}/{}'.format(path, idx+1, plc_code[idx]), 'dst': dst_script_ubuntu},
                   {'src': '{}/script_selenium_plc{}.py'.format(path_temp_script,idx+1), 'dst': dst_script_ubuntu},
               ]}]
              }
        if operations.control_source_log(x, source) == True:
            gst['tasks'][0]['copy_content'].append({'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst})
        guest.append(gst)


# GENERIC
generic = []
generic_os = []
if data['GENERIC']['name'] != None:
#if len(data['GENERIC']['name']) != 0:
    generic = data['GENERIC']['name'].replace(" ","").split(",")
    generic_os = data['GENERIC']['os'].replace(" ","").split(",")
    for idx, x in enumerate(generic):
        gst = {'id': x, 'basevm_host': 'host_1',
               'basevm_config_file': '{}/image_{}.xml'.format(path_img, generic_os[idx]), 'basevm_type': 'kvm',
               'tasks': [{'copy_content': [
                   {'src': '{}/{}/storyboard'.format(path_models, model[0]), 'dst': '/root/Scrivania'}
               ]}]
               }
        if operations.control_source_log(x, source) == True:
            gst['tasks'][0]['copy_content'].append({'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst})
        guest.append(gst)

# FIREWALL
firewall = data['ROUTER_FIREWALL']['name'].replace(" ","").split(",")
fw_os = data['ROUTER_FIREWALL']['os'].replace(" ","").split(",")
for idx, x in enumerate(firewall):
    gst = {'id': x, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_{}.xml'.format(path_img, fw_os[idx]),
           'basevm_type': 'kvm'}
    if operations.control_source_log(x,source) == True:
        gst['tasks'] = [{'copy_content': [{'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst_script_ubuntu}]}]
    guest.append(gst)

#LOGSTASH
if exp != None:
#if len(exp) != 0:
    gst = {'id': exp, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_ubuntu.xml'.format(path_img),
           'basevm_type': 'kvm',
           'tasks': [{'copy_content': [
                   {'src': '{}/setting.conf'.format(path_temp_script), 'dst': '/etc/logstash/conf.d/'}
               ]}]
           }
    guest.append(gst)

# -----------------------------------------------------------------------------------------
# CLONE SETTINGS

# SECTION GUESTS - DATA
clone_guest = []
total_number_vm = model + mtu + rtu + plc + generic
total_number_vm2 = total_number_vm + firewall
total_os_vm = model_os + hmi_os + rtu_os + plc_os + generic_os + fw_os
entry_point = data['CONFIG']['entry_point']

# SECTION NETWORKS - DATA
nt = []
ss = 0
name_network = data['NETWORKS']['name'].replace(" ","").split(";")
name_network[-1] = name_network[-1].replace(";", "")  # delete ";" from last element of list
members_not_format = data['NETWORKS']['members'].replace(" ", "")
gateway = data['NETWORKS']['gateway'].replace(" ","")

#setting vm machine with logstash
if exp != None:
#if len(exp) != 0:
    name_network.append('export')
    members_not_format=members_not_format + ';' + exp
    gateway = gateway + ';' + firewall[0]  #case for only one router_firewall


elements = operations.number_of_members(members_not_format)
members_eth = operations.add_eth(members_not_format)
gateway_eth = operations.add_eth(gateway)


#insert into clone guest

for y in total_number_vm:
    if y == entry_point:
        cl_g = {'guest_id': y, 'number': 1, 'entry_point': bool('yes')}
        clone_guest.append(cl_g)
    else:
        cl_g = {'guest_id': y, 'number': 1}
        clone_guest.append(cl_g)

if exp != None: #for logstash
#if len(exp) != 0:
    if exp == entry_point:
        cl_g = {'guest_id': exp, 'number': 1, 'entry_point': bool('yes')}
        clone_guest.append(cl_g)
    else:
        cl_g = {'guest_id': exp, 'number': 1}
        clone_guest.append(cl_g)

for y in range(len(firewall)):
    rules = data['ROUTER_FIREWALL']['forwarding'][y]['rules']
    if exp != None : rules = operations.add_rule_to_export_data(rules, name_network)
    #if len(exp) != 0: rules = operations.add_rule_to_export_data(rules, name_network)
    if firewall[y] == entry_point:
        cl_g = {'guest_id': y, 'number': 1, 'forwarding_rules': rules,
                'entry_point': bool('yes')}
        clone_guest.append(cl_g)
    else:
        cl_g = {'guest_id': firewall[y], 'number': 1, 'forwarding_rules': rules}
        clone_guest.append(cl_g)


# insert into networks
str1 = ", "
tmp = 0
for j in name_network:
    ntt = {'name': j, 'members': str1.join(members_eth[tmp:elements[ss] + tmp]), 'gateway': gateway_eth[ss]}
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
# START SCRIPT GENERATIONS:

#ip vms calculations
ip_list= operations.ip_list(members_eth, gateway_eth, elements, numb_cyber)


# ------------------------------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# OPC GENERATOR
sensors = data['MODEL']['opc_parameters']['sensors'].replace(" ","").split(",")
actuators = []
if  data['MODEL']['opc_parameters']['actuators'] != None:
#if  len(data['MODEL']['opc_parameters']['actuators']) != 0:
    actuators = data['MODEL']['opc_parameters']['actuators'].replace(" ","").replace(", ","").split(",")
    actuators = [x.split("=") for x in actuators] #with value
url = "opc.tcp://localhost:4841" #nell'ipotesi che il server OPC sia sulla stessa macchina del client(script python)


if interface == 'modbus':
    if len(rtu) != 0:
        address_modbus = ip_list[rtu[0] + '.eth0'][0]
    else:
        address_modbus = 'localhost'
    opc_generator.opc_modbus(interface, address_modbus, url, sensors, actuators, path_temp_script)
    opc_generator.modbus(path_temp_script)


# ---------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT MODEL GENERATOR

model_script.script_for_model(modeler, model, model_os, rtu, dst_script_ubuntu, interface, path_temp_script)

#----------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT RTU

if len(rtu) != 0:
    input_rtu = data['RTU']['input'].replace(" ","").split(";")
    act_wv = [] #actuators without values
    for idx,x in enumerate(actuators): act_wv.append(actuators[idx][0])
    for idx, x in enumerate(rtu):
        sensors_input = []
        actuators_input = []
        ss = input_rtu[idx].split(",")
        for idx2, x2 in enumerate(ss):
            try:
                sensors_input.append((sensors.index(x2))*2)
            except:
                continue
        for idx2, x2 in enumerate(ss):
            try:
                actuators_input.append((act_wv.index(x2))*2+(len(sensors)*2))
            except:
                continue
        rtu_code_generator.rtu_code(sensors_input, actuators_input, ip_list['{}'.format(model[0] + '.eth0')][0], x, path_temp_script)

#----------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT PLC
if len(plc) != 0:
    plc_input = data['PLC']['input'].replace(" ","").split(";")
    plc_output = data['PLC']['output_slave'].replace(" ","").split(";")

    if len(rtu) == 0: #altrimenti questa operazione l'ho gia fatta prima
        act_wv = []
        for idx, x in enumerate(actuators): act_wv.append(actuators[idx][0])
    for idx, x in enumerate(plc):
        sensors_input = [] #address for reading sensors
        actuators_input = [] #address for reading actuators
        actuators_output = [] #address for writing actuators
        ss = plc_input[idx].split(",")
        os = plc_output[idx].split(",")
        for idx2, x2 in enumerate(ss):
            try:
                sensors_input.append((sensors.index(x2)) * 2)
            except:
                continue
        for idx2, x2 in enumerate(ss):
            try:
                actuators_input.append((act_wv.index(x2)) * 2 + (len(sensors) * 2))
            except:
                continue
        for idx2, x2 in enumerate(os):
            try:
                actuators_output.append((act_wv.index(x2)) * 2 + (len(sensors) * 2))
            except:
                continue
        plc_configuration.plc_mbconfig(path, idx + 1, sensors_input, actuators_input, actuators_output, plc_input[idx].split(","), ip_list['{}'.format(model[0] + '.eth0')][0])


#----------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT SELENIUM (HMI - SCADABR) (PLC)

selenium_script.selenium_script(hmi, hmi_os, plc, plc_code, dst_script_ubuntu, path_temp_script)

#---------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# DATA JSON GENERATOR


if hmi[0] == 'scadabr':
    type_alert = []
    variable = []
    if data['MTU']['set_alert']['type'] != None :
    #if len(data['MTU']['set_alert']['type']) != 0:
        type_alert = data['MTU']['set_alert']['type']
        variable = data['MTU']['set_alert']['variable']

    if len(rtu) == 0:
        json_generator.json_generator(ip_list, sensors, actuators, model, rtu, type_alert, variable, path_temp_script)
    else:
        act_wv = []  # actuators without values
        for idx, x in enumerate(actuators): act_wv.append(actuators[idx][0])
        json_generator.json_generator_multiple(ip_list, sensors, act_wv, model, rtu, input_rtu, type_alert, variable, path_temp_script)


#---------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# DATA EXPORT CONFIGURATION (LOGSTASH - FILEBEAT)

if exp != None:
#if len(exp) != 0:
    port_kafka = 9092
    port_beats = 5044
    source_os = operations.get_os(source,total_number_vm2, total_os_vm)

    logstash_conf.logstash_config(ip_export, source, log_type, port_kafka, port_beats, path_temp_script)
    for idx, x in enumerate(source):
        filebeat_config.filebeat(x, source_os[idx], log_type[idx], ip_list['{}'.format(exp)+'.eth0'][0], port_kafka, port_beats, path_temp_script)


# ---------------------------------------------------------------------------------------------------------------------------------
###################################################################################################################################
# SCRIPT AFTER CLONE GENERATOR

#manage script after clone AND security level
sec_vuln = data['SECURITY']['vulnerability']
sec_target = data['SECURITY']['target']

after_clone.script_after_clone(sec_vuln, sec_target, ip_list, rtu, plc, model, model_os, mtu, hmi, hmi_os, firewall, generic, exp, source, total_number_vm, dst_script_ubuntu, numb_cyber, path_temp_script)
