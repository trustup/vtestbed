import yaml
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
import server_opcua_conf
import os as command_os

def converter(data, code, *stfile):

    try:
        #IP_HOST = '192.168.1.65'
        IP_HOST = data['CONFIG']['ip_host']
        numb_cyber = data['CONFIG']['cyber_range_id']
        path = data['CONFIG']['path']  # path cyris
        path = operations.replace_path(path)
        dst_script_ubuntu = "/home/ubuntu/"  # path destination script ON virtual machine
        dst_script_windows = 'C:\CyberRange'
        path_img = "{}/cyris/images".format(path)
        path_models = "{}/models".format(path)

        if code == "900":
            command_os.system("mkdir {}/temp/{}".format(path,numb_cyber))
        path_temp_script = '{}/temp/{}'.format(path,numb_cyber)

        exp = data['EXPORT_DATA']['name']
        #exp = None
        read_topic = []
        ip_export = []
        source_log = []
        log_type = []
        if exp != None:
            ip_export = data['EXPORT_DATA']['ip_server']
            read_topic = data['EXPORT_DATA']['read_topic']
            topic = data['EXPORT_DATA']['public_to_kafka']['topic']
            source_log = data['EXPORT_DATA']['public_to_kafka']['source_data'].replace(" ", "").split(";")
            log_type = data['EXPORT_DATA']['public_to_kafka']['log_type'].replace(" ", "").split(";")

        # HOST SETTING
        host = [{'id': 'host_1', 'mgmt_addr': IP_HOST, 'virbr_addr': '192.168.122.1', 'account': 'ubuntu'}]
        # print(host)

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
                archive = '{}/{}/{}/{}.zip'.format(path_models,modeler, model[0], model[0])
                dst = dst_script_windows
                # dgs = '{}/{}/diagslave.exe'.format(path_models, modeler)
                script = '{}/script.bat'.format(path_temp_script)
            else:
                archive = '{}/{}/{}/{}.tar.gz'.format(path_models, modeler, model[0], model[0])
                dst = dst_script_ubuntu
                # dgs = '{}/{}/diagslave'.format(path_models, modeler)
                script = '{}/script.sh'.format(path_temp_script)
            gst = {'id': model[0], 'basevm_host': 'host_1',
                   'basevm_config_file': '{}/image_{}.xml'.format(path_img, model_os[0].replace(".", "")),
                   'basevm_type': 'kvm',
                   'tasks': [{'copy_content': [
                       {'src': archive, 'dst': '{}'.format(dst)},
                       {'src': '{}/opc_{}.py'.format(path_temp_script, interface),
                        'dst': '{}'.format(dst)},
                       {'src': '{}/{}.py'.format(path_temp_script, interface), 'dst': '{}'.format(dst)},
                       {'src': script, 'dst': '{}'.format(dst)}
                       # {'src': dgs, 'dst': '{}'.format(dst)}
                   ]}]
                   }
        if modeler == 'matlab':
            if model_os[0] == 'windows.7':
                archive = '{}/{}/{}/{}.exe'.format(path_models, modeler, model[0], model[0])
                dst = dst_script_windows
                script = '{}/script.bat'.format(path_temp_script)
            gst = {'id': model[0], 'basevm_host': 'host_1',
                   'basevm_config_file': '{}/image_{}_{}.xml'.format(path_img, model_os[0].replace(".", ""), modeler),
                   'basevm_type': 'kvm',
                   'tasks': [{'copy_content': [
                       {'src': archive, 'dst': '{}'.format(dst)},
                       {'src': '{}/server_opcua.py'.format(path_temp_script), 'dst': '{}'.format(dst)},
                       {'src': '{}/opc_{}.py'.format(path_temp_script, interface),
                        'dst': '{}'.format(dst)},
                       {'src': '{}/{}.py'.format(path_temp_script, interface), 'dst': '{}'.format(dst)},
                       {'src': '{}/script1.bat'.format(path_temp_script), 'dst': '{}'.format(dst)},
                       {'src': '{}/script2.bat'.format(path_temp_script), 'dst': '{}'.format(dst)}
                   ]}]
                   }
        if topic != None and operations.control_source_log(model[0], source_log) == True:
            gst['tasks'][0]['copy_content'].append(
                    {'src': '{}/filebeat_{}.yml'.format(path_temp_script, model[0]), 'dst': dst})
        if model_os[0] == 'windows.7':
            gst["basevm_os_type"] = "windows.7"
                # gst['tasks'][0]['copy_content'].append({'src':'{}/PycharmProjects/temp/script2.sh'.format(path), 'dst':dst_script_windows})
        guest.append(gst)


        # MTU
        mtu = data['MTU']['name'].replace(" ", "").split(",")
        hmi = data['MTU']['hmi'].replace(" ", "").split(",")
        hmi_os = data['MTU']['os'].replace(" ", "").split(",")
        image_try = command_os.path.isfile('{}/{}/{}/{}.png'.format(path_models, modeler, model[0], model[0]))
        if image_try == False:
            command_os.system('cp {}/generic.png {}/{}/{}/{}.png'.format(path_models,path_models, modeler, model[0], model[0]))
        for x in range(len(mtu)):
            if hmi[x] == 'scadabr':
                if hmi_os[x] == 'windows.7':
                    # dest1, dest2 = 'C:/CyberRange', 'C:/CyberRange'  #destination script
                    dst = dst_script_windows
                else:
                    # dest1, dest2 = dst_script_ubuntu, '/var/lib/tomcat8/webapps/ScadaBR/uploads/'
                    dst = dst_script_ubuntu
                gst = {'id': mtu[x], 'basevm_host': 'host_1',
                       'basevm_config_file': '{}/image_{}.xml'.format(path_img, hmi_os[x].replace(".", "")),
                       'basevm_type': 'kvm',
                       'tasks': [{'copy_content': [
                           {'src': '{}/data.json'.format(path_temp_script), 'dst': '{}'.format(dst)},
                           {'src': '{}/script_selenium.py'.format(path_temp_script), 'dst': '{}'.format(dst)},
                           {'src': '{}/{}/{}/{}.png'.format(path_models, modeler, model[0], model[0]), 'dst': dst}
                       ]}]
                       }
            if topic != None and operations.control_source_log(mtu[0], source_log) == True:
                gst['tasks'][0]['copy_content'].append(
                    {'src': '{}/filebeat_{}.yml'.format(path_temp_script, mtu[0]), 'dst': dst})
            if hmi_os[x] == 'windows.7':
                gst["basevm_os_type"] = "windows.7"
            guest.append(gst)

        # RTU
        rtu = []
        rtu_os = []
        if data['RTU']['name'] != None:
            rtu = data['RTU']['name'].replace(" ", "").split(";")
            rtu_os = data['RTU']['os'].replace(" ", "").split(";")
            for idx, x in enumerate(rtu):
                gst = {'id': x, 'basevm_host': 'host_1',
                       'basevm_config_file': '{}/image_{}.xml'.format(path_img, rtu_os[idx]),
                       'basevm_type': 'kvm',
                       'tasks': [{'copy_content': [
                           # {'src': '{}/diagslave'.format(path_models), 'dst': '{}'.format(dst_script_ubuntu)}
                           {'src': '{}/code_{}.py'.format(path_temp_script,x),
                            'dst': '{}'.format(dst_script_ubuntu)}
                       ]}]
                       }
                if topic != None and operations.control_source_log(x, source_log) == True:
                    gst['tasks'][0]['copy_content'].append(
                        {'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst})
                guest.append(gst)

        # PLC
        plc = []
        plc_os = []
        plc_code = []
        if data['PLC']['name'] != None:
            plc = data['PLC']['name'].replace(" ", "").split(";")
            plc_os = data['PLC']['os'].replace(" ", "").split(";")
            # slave_conf =
            plc_code = data['PLC']['plc_code'].replace(" ", "").split(";")
            for idx, x in enumerate(plc):
                gst = {'id': x, 'basevm_host': 'host_1',
                       'basevm_config_file': '{}/image_{}.xml'.format(path_img, plc_os[idx]),
                       'basevm_type': 'kvm',
                       'tasks': [{'copy_content': [
                           #{'src': '{}/cyris/PLC/{}/mbconfig.cfg'.format(path, idx + 1), 'dst': '/bin/cyberrange/OpenPLC_v3/webserver'},
                           #{'src': '{}/cyris/PLC/{}/{}'.format(path, idx + 1, plc_code[idx]), 'dst': dst_script_ubuntu},
                           {'src': '{}/PLC/{}/mbconfig.cfg'.format(path_temp_script, idx + 1),
                            'dst': '/bin/cyberrange/OpenPLC_v3/webserver'},
                           {'src': '{}/PLC/{}/{}'.format(path_temp_script, idx + 1, plc_code[idx]), 'dst': dst_script_ubuntu},
                           {'src': '{}/script_selenium_plc{}.py'.format(path_temp_script, idx + 1),
                            'dst': dst_script_ubuntu},
                           {'src': '{}/script_selenium_plc{}_restart.py'.format(path_temp_script, idx + 1),
                            'dst': dst_script_ubuntu},
                       ]}]
                       }
                if topic != None and operations.control_source_log(x, source_log) == True:
                    gst['tasks'][0]['copy_content'].append(
                        {'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst})
                guest.append(gst)

        # GENERIC
        generic = []
        generic_os = []
        if data['GENERIC']['name'] != None:
            generic = data['GENERIC']['name'].replace(" ", "").split(",")
            generic_os = data['GENERIC']['os'].replace(" ", "").split(",")
            for idx, x in enumerate(generic):
                gst = {'id': x, 'basevm_host': 'host_1',
                       'basevm_config_file': '{}/image_{}.xml'.format(path_img, generic_os[idx]), 'basevm_type': 'kvm',
                       #'tasks': [{'copy_content': [
                       #    {'src': '{}/{}/{}/storyboard'.format(path_models, modeler, model[0]), 'dst': '/root/Scrivania'}
                       #]}]
                       }
                if topic != None and operations.control_source_log(x, source_log) == True:
                    gst['tasks'][0]['copy_content'].append(
                        {'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst})
                guest.append(gst)

        # FIREWALL
        firewall = data['ROUTER_FIREWALL']['name'].replace(" ", "").split(",")
        fw_os = data['ROUTER_FIREWALL']['os'].replace(" ", "").split(",")
        for idx, x in enumerate(firewall):
            gst = {'id': x, 'basevm_host': 'host_1',
                   'basevm_config_file': '{}/image_{}.xml'.format(path_img, fw_os[idx]),
                   'basevm_type': 'kvm'}
            if topic != None and operations.control_source_log(x, source_log) == True:
                gst['tasks'] = [{'copy_content': [
                    {'src': '{}/filebeat_{}.yml'.format(path_temp_script, x), 'dst': dst_script_ubuntu}]}]
            guest.append(gst)

        # LOGSTASH
        if exp != None:
            #if topic != None:
                #tsk = {'src': '', 'dst': ''}
                #tsk['src'] = '{}/setting.conf'.format(path_temp_script)
                #tsk['dst'] = '/etc/logstash/conf.d/'
                #tsk = tsk + tsk.update({'src': '{}/setting.conf'.format(path_temp_script), 'dst': '/etc/logstash/conf.d/'})
            #if read_topic != None:
                #tsk = {'src': [], 'dst': []}
                #tsk['src'] = '{}/kafka_consumer.py'.format(path_temp_script)
                #tsk['dst'] = dst_script_ubuntu
                #tsk = tsk + tsk.update({'src': '{}/kafka_consumer.py'.format(path_temp_script), 'dst': dst_script_ubuntu})
            # gst = {'id': exp, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_ubuntu.xml'.format(path_img),
            #       'basevm_type': 'kvm',
            #       'tasks': [{'copy_content': [
            #           {'src': '{}/setting.conf'.format(path_temp_script), 'dst': '/etc/logstash/conf.d/'}
            #       ]}]
            #       }
            if topic == None and read_topic == None:
                gst = {'id': exp, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_ubuntu.xml'.format(path_img),
                       'basevm_type': 'kvm'
                       }
            else:
                gst = {'id': exp, 'basevm_host': 'host_1', 'basevm_config_file': '{}/image_ubuntu.xml'.format(path_img),
                    'basevm_type': 'kvm',
                    'tasks': [{'copy_content': []}]
                    }
                if topic != None:
                    gst['tasks'][0]['copy_content'].append(
                        {'src': '{}/setting.conf'.format(path_temp_script), 'dst': '/etc/logstash/conf.d/'})
                if read_topic != None:
                    gst['tasks'][0]['copy_content'].append(
                        {'src': '{}/kafka_consumer.py'.format(path_temp_script), 'dst': dst_script_ubuntu})
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
        name_network = data['NETWORKS']['name'].replace(" ", "").split(";")
        name_network[-1] = name_network[-1].replace(";", "")  # delete ";" from last element of list
        members_not_format = data['NETWORKS']['members'].replace(" ", "")
        gateway = data['NETWORKS']['gateway'].replace(" ", "")

        # setting vm machine with logstash
        if exp != None:
            name_network.append('export')
            members_not_format = members_not_format + ';' + exp
            gateway = gateway + ';' + firewall[0]  # case for only one router_firewall

        elements = operations.number_of_members(members_not_format)
        members_eth = operations.add_eth(members_not_format)
        gateway_eth = operations.add_eth(gateway)

        # insert into clone guest

        for y in total_number_vm:
            if y == entry_point:
                cl_g = {'guest_id': y, 'number': 1, 'entry_point': bool('yes')}
                clone_guest.append(cl_g)
            else:
                cl_g = {'guest_id': y, 'number': 1}
                clone_guest.append(cl_g)

        if exp != None:  # for logstash
            if exp == entry_point:
                cl_g = {'guest_id': exp, 'number': 1, 'entry_point': bool('yes')}
                clone_guest.append(cl_g)
            else:
                cl_g = {'guest_id': exp, 'number': 1}
                clone_guest.append(cl_g)

        for y in range(len(firewall)):
            rules = data['ROUTER_FIREWALL']['forwarding'][y]['rules']
            if exp != None: rules = operations.add_rule_to_export_data(rules, name_network)
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

        with open(r'{}/cyris/examples/cyberrange.yml'.format(path), 'w') as file:
            data_out = yaml.dump(output, file, sort_keys=False)

        # ---------------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # START SCRIPT GENERATIONS:

        # ip vms calculations
        ip_list = operations.ip_list(members_eth, gateway_eth, elements, numb_cyber)

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # OPC GENERATOR
        sensors = data['MODEL']['opc_parameters']['sensors'].replace(" ", "").split(",")
        actuators = []
        if data['MODEL']['opc_parameters']['actuators'] != None:
            actuators = data['MODEL']['opc_parameters']['actuators'].replace(" ", "").replace(", ", "").split(",")
            actuators = [x.split("=") for x in actuators]  # with value
        url = "opc.tcp://localhost:4841"  # nell'ipotesi che il server OPC sia sulla stessa macchina del client(script python)

        if interface == 'modbus':
            if len(rtu) != 0:
                address_modbus = ip_list[rtu[0] + '.eth0'][0]
            else:
                address_modbus = 'localhost'
            opc_generator.opc_modbus(interface, modeler, address_modbus, url, sensors, actuators, path_temp_script)
            opc_generator.modbus(path_temp_script)

        # ---------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # SCRIPT MODEL GENERATOR

        model_script.script_for_model(modeler, model, model_os, rtu, dst_script_ubuntu, interface, path_temp_script)

        # ----------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # SCRIPT RTU

        if len(rtu) != 0:
            input_rtu = data['RTU']['input'].replace(" ", "").split(";")
            act_wv = []  # actuators without values
            for idx, x in enumerate(actuators): act_wv.append(actuators[idx][0])
            for idx, x in enumerate(rtu):
                sensors_input = []
                actuators_input = []
                ss = input_rtu[idx].split(",")
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
                rtu_code_generator.rtu_code(sensors_input, actuators_input, ip_list['{}'.format(model[0] + '.eth0')][0],
                                            x, path_temp_script)

        # ----------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # SCRIPT PLC
        if len(plc) != 0:

            plc_input = data['PLC']['input'].replace(" ", "").split(";")
            plc_output = data['PLC']['output_slave'].replace(" ", "").split(";")

            if len(rtu) == 0:  # altrimenti questa operazione l'ho gia fatta prima
                act_wv = []
                for idx, x in enumerate(actuators): act_wv.append(actuators[idx][0])
            for idx, x in enumerate(plc):
                if idx == 0: command_os.system("mkdir {}/PLC".format(path_temp_script))
                command_os.system("mkdir {}/PLC/{}/".format(path_temp_script, idx+1))
                sensors_input = []  # address for reading sensors
                actuators_input = []  # address for reading actuators
                actuators_output = []  # address for writing actuators

                #stfile = stfile.replace("'", "", 1)
                #stfile = stfile[:-1]
                #print(stfile)
                #with open(r'{}/PLC/{}/{}'.format(path_temp_script, idx+1, plc_code[idx]), 'w') as f:
                #    f.write(stfile)

                #stfile = list(stfile.replace('\\r', '\r').replace('\\n','\n'))
                if stfile:
                    stfile = stfile[0]
                    if type(stfile) == str:
                        stfile = eval(stfile)
                    for idx_st, stcode in enumerate(stfile):
                        if stcode['plcName'] == x:
                            with open(r'{}/PLC/{}/{}'.format(path_temp_script, idx + 1, stcode['name']), 'w') as f:
                                f.write(stcode['value'])
                else:
                    command_os.system("cp {}/models/{}/{}/other_files/{} {}/PLC/{}/{}".format(path,modeler,model[0],plc_code[idx], path_temp_script,idx+1,plc_code[idx]))




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
                plc_configuration.plc_mbconfig(path_temp_script, idx + 1, sensors_input, actuators_input, actuators_output,
                                               plc_input[idx].split(","), ip_list['{}'.format(model[0] + '.eth0')][0])

        # ----------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # SCRIPT SELENIUM (HMI - SCADABR) (OPENPLC)

        selenium_script.selenium_script(hmi, hmi_os, plc, plc_code, dst_script_ubuntu, path_temp_script)

        # ---------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # DATA JSON GENERATOR

        if hmi[0] == 'scadabr':
            type_alert = []
            variable = []
            if data['MTU']['set_alert']['type'] != None:
                type_alert = data['MTU']['set_alert']['type']
                variable = data['MTU']['set_alert']['variable']

            if len(rtu) == 0:
                json_generator.json_generator(ip_list, sensors, actuators, model, rtu, type_alert, variable, path_temp_script)
            else:
                act_wv = []  # actuators without values
                for idx, x in enumerate(actuators): act_wv.append(actuators[idx][0])
                json_generator.json_generator_multiple(ip_list, sensors, act_wv, model, rtu, input_rtu, type_alert,
                                                       variable, path_temp_script)

        # ---------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # DATA EXPORT CONFIGURATION (LOGSTASH - FILEBEAT)

        if exp != None:
            port_kafka = 9092
            port_beats = 5044
            source_os = operations.get_os(source_log, total_number_vm2, total_os_vm)

            if topic != None:
                logstash_conf.logstash_config(ip_export, source_log, log_type, topic, port_kafka, port_beats, path_temp_script)
                for idx, x in enumerate(source_log):
                    filebeat_config.filebeat(x, source_os[idx], log_type[idx], ip_list['{}'.format(exp) + '.eth0'][0], port_kafka, port_beats, path_temp_script)

            if read_topic != None:
                if len(rtu) == 0 and len(plc) == 0:  # altrimenti questa operazione l'ho gia fatta prima
                    act_wv = []
                    for idx, x in enumerate(actuators): act_wv.append(actuators[idx][0])
                logstash_conf.kafka_consumer(numb_cyber, path_temp_script, dst_script_ubuntu, ip_export, port_kafka,read_topic, ip_list,model,interface,sensors,act_wv, plc, plc_os)

        # ---------------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # SCRIPT AFTER CLONE GENERATOR

        # manage script after clone AND security level
        sec_vuln = data['SECURITY']['vulnerability']
        sec_target = data['SECURITY']['target']

        after_clone.script_after_clone(sec_vuln, sec_target, ip_list, rtu, plc, model, model_os, mtu, hmi, hmi_os,
                                       firewall, generic, exp, read_topic, topic, source_log, total_number_vm, dst_script_ubuntu, dst_script_windows, numb_cyber, path_temp_script)



        # ---------------------------------------------------------------------------------------------------------------------------------
        ###################################################################################################################################
        # SERVER OPCUA GENERATOR (only for matlab)
        if modeler == 'matlab':
            server_opcua_conf.server_opcua(sensors,actuators,path_temp_script)



        values = [ip_list, total_number_vm2, exp, numb_cyber, path_temp_script, path]

        #save parameters for restart - close -destroy function
        with open(r'{}/values.yml'.format(path_temp_script), 'w') as file:
            data_out = yaml.dump(values, file, sort_keys=False)

        return values


    except Exception as error:
        return 'error: ' + str(error)


######################FOR TEST##########################
#data = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0, input2=0, PLC=0', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}
#sample = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0.6, input2=0.3, input3=0.5', 'sensors': 'mainTank.V, secondaryTank.V, velocityTank2, massOverflow'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': None}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'tankmodel; mtu-hmi', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 101, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}
#erro = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0.6, input2=0.3', 'sensors': 'mainTank.V, secondaryTank.V'}}, 'MTU': {'name': 'Node_5', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': 'Node_1, Node_2', 'os': 'ubuntu, ubuntu', 'input': 'mainTank.V; secondaryTank.V', 'output_slave': 'input1; input2', 'plc_code': 'double_control.st, double_control.st'}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'Node_6', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=net1 dst=net0'}]}]}, 'NETWORKS': {'name': 'net1; net0', 'members': 'tankmodel, Node_1; Node_5', 'gateway': 'Node_6; Node_6'}, 'CONFIG': {'entry_point': 'Node_5', 'cyber_range_id': 35, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': '', 'log_type': ''}}
#st = "FUNCTION function1 : BOOL\r\n  VAR_INPUT\r\n    LOWWORD : UINT;\r\n    HIGHWORD : UINT;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    WORDSTOREAL : REAL;\r\n  END_VAR\r\n\r\n  {{\r\n  union words_to_real {\r\n  uint16_t i[2];\r\n  float f;\r\n  }w2r;\r\n  w2r.i[0] = LOWWORD;\r\n  w2r.i[1] = HIGHWORD;\r\n  WORDSTOREAL = w2r.f;\r\n  }}\r\nEND_FUNCTION\r\n\r\nFUNCTION_BLOCK control\r\n  VAR_INPUT\r\n    VALORE : REAL;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    controll : REAL;\r\n  END_VAR\r\n\r\n  IF (VALORE<1.015) THEN\r\n    controll := 0.0;\r\n  ELSIF (controll = 0.0 and VALORE<2.4) THEN\r\n    controll := 0.0;\r\n  ELSIF (controll = 0.0 and VALORE>2.4) THEN\r\n    controll := 1.0;\r\n  ELSIF (controll =1.0 and VALORE<2.4) THEN\r\n    controll := 1.0;\r\n  END_IF; \r\nEND_FUNCTION_BLOCK\r\n\r\nFUNCTION prova : BOOL\r\n  VAR_INPUT\r\n    INPP : REAL;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    LOWW : UINT;\r\n    HIGG : UINT;\r\n  END_VAR\r\n\r\n  {{\r\n  union real_to_words {\r\n  uint16_t i[2];\r\n  float f;\r\n  }r2w;\r\n  r2w.f = INPP;\r\n  LOWW = r2w.i[0];\r\n  HIGG = r2w.i[1];\r\n  }}\r\nEND_FUNCTION\r\n\r\nPROGRAM pressure\r\n  VAR\r\n    WORD1 AT %IW100 : UINT;\r\n    WORD2 AT %IW101 : UINT;\r\n    WORD3 AT %MD0 : REAL;\r\n    prova1 AT %QW100 : UINT;\r\n    prova2 AT %QW101 : UINT;\r\n  END_VAR\r\n  VAR\r\n    control0 : control;\r\n    function18_OUT : BOOL;\r\n    function18_WORDSTOREAL : REAL;\r\n    prova9_OUT : BOOL;\r\n    prova9_LOWW : UINT;\r\n    prova9_HIGG : UINT;\r\n  END_VAR\r\n\r\n  function18_OUT := function1(LOWWORD := WORD2, HIGHWORD := WORD1, WORDSTOREAL => function18_WORDSTOREAL);\r\n  WORD3 := function18_WORDSTOREAL;\r\n  control0(VALORE := function18_WORDSTOREAL);\r\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\r\n  prova2 := prova9_LOWW;\r\n  prova1 := prova9_HIGG;\r\nEND_PROGRAM\r\n\r\n\r\nCONFIGURATION Config0\r\n\r\n  RESOURCE Res0 ON PLC\r\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\r\n    PROGRAM instance0 WITH task0 : pressure;\r\n  END_RESOURCE\r\nEND_CONFIGURATION\r\n"
# file contenente vari codici plc.st da salvare
#filke = [{"plcName":"plcone","name":"double_control (copy).st","value":"FUNCTION function1 : BOOL\r\n  VAR_INPUT\r\n    LOWWORD : UINT;\r\n    HIGHWORD : UINT;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    WORDSTOREAL : REAL;\r\n  END_VAR\r\n"},{"plcName":"Node_2","name":"double_control.st","value":"FUNCTION function1 : BOOL\r\n  VAR_INPUT\r\n    LOWWORD : UINT;\r\n    HIGHWORD : UINT;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    WORDSTOREAL : REAL;\r\n  END_VAR\r\n\r\n  {{\r\n  union words_to_real {\r\n  uint16_t i[2];\r\n  float f;\r\n  }w2r;\r\n  w2r.i[0] = LOWWORD;\r\n  w2r.i[1] = HIGHWORD;\r\n  WORDSTOREAL = w2r.f;\r\n  }}\r\nEND_FUNCTION\r\n\r\nFUNCTION_BLOCK control\r\n  VAR_INPUT\r\n    VALORE : REAL;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    controll : REAL;\r\n  END_VAR\r\n\r\n  IF (VALORE<1.015) THEN\r\n    controll := 0.0;\r\n  ELSIF (controll = 0.0 and VALORE<2.4) THEN\r\n    controll := 0.0;\r\n  ELSIF (controll = 0.0 and VALORE>2.4) THEN\r\n    controll := 1.0;\r\n  ELSIF (controll =1.0 and VALORE<2.4) THEN\r\n    controll := 1.0;\r\n  END_IF; \r\nEND_FUNCTION_BLOCK\r\n\r\nFUNCTION prova : BOOL\r\n  VAR_INPUT\r\n    INPP : REAL;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    LOWW : UINT;\r\n    HIGG : UINT;\r\n  END_VAR\r\n\r\n  {{\r\n  union real_to_words {\r\n  uint16_t i[2];\r\n  float f;\r\n  }r2w;\r\n  r2w.f = INPP;\r\n  LOWW = r2w.i[0];\r\n  HIGG = r2w.i[1];\r\n  }}\r\nEND_FUNCTION\r\n\r\nPROGRAM pressure\r\n  VAR\r\n    WORD1 AT %IW100 : UINT;\r\n    WORD2 AT %IW101 : UINT;\r\n    WORD3 AT %MD0 : REAL;\r\n    prova1 AT %QW100 : UINT;\r\n    prova2 AT %QW101 : UINT;\r\n  END_VAR\r\n  VAR\r\n    control0 : control;\r\n    function18_OUT : BOOL;\r\n    function18_WORDSTOREAL : REAL;\r\n    prova9_OUT : BOOL;\r\n    prova9_LOWW : UINT;\r\n    prova9_HIGG : UINT;\r\n  END_VAR\r\n\r\n  function18_OUT := function1(LOWWORD := WORD2, HIGHWORD := WORD1, WORDSTOREAL => function18_WORDSTOREAL);\r\n  WORD3 := function18_WORDSTOREAL;\r\n  control0(VALORE := function18_WORDSTOREAL);\r\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\r\n  prova2 := prova9_LOWW;\r\n  prova1 := prova9_HIGG;\r\nEND_PROGRAM\r\n\r\n\r\nCONFIGURATION Config0\r\n\r\n  RESOURCE Res0 ON PLC\r\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\r\n    PROGRAM instance0 WITH task0 : pressure;\r\n  END_RESOURCE\r\nEND_CONFIGURATION\r\n"}]


with open('/home/ubuntu/virtualTestbed/models/matlab/aiv_robot/other_files/robot_control.st') as f:
    stread = f.read()
st_construct = [{"plcName":"plc1", "name":"robot_control.st","value": '{}'.format(stread)}]
#st = [{"plcName":"plc1","name":"robot_control.st","value":"FUNCTION function1 : BOOL\n  VAR_INPUT\n    LOWWORD : UINT;\n    HIGHWORD : UINT;\n  END_VAR\n  VAR_OUTPUT\n    WORDSTOREAL : REAL;\n  END_VAR\n\n  {{\n  union words_to_real {\n  uint16_t i[2];\n  float f;\n  }w2r;\n  w2r.i[0] = LOWWORD;\n  w2r.i[1] = HIGHWORD;\n  WORDSTOREAL = w2r.f;\n  }}\nEND_FUNCTION\n\nFUNCTION_BLOCK control\n  VAR_INPUT\n    VALORE : REAL;\n    VALORE2 : REAL;\n  END_VAR\n  VAR_OUTPUT\n    controll : REAL;\n  END_VAR\n\n  IF (VALORE = 0.0 and VALORE2 = 0.0) THEN\n    controll := 1.0;\n  ELSIF (VALORE = 0.0 and VALORE2 = 1.0) THEN\n    controll := 0.0;\n  ELSIF (VALORE = 1.0 and VALORE2 = 1.0) THEN\n    controll := 1.0;\n  END_IF; \nEND_FUNCTION_BLOCK\n\nFUNCTION prova : BOOL\n  VAR_INPUT\n    INPP : REAL;\n  END_VAR\n  VAR_OUTPUT\n    LOWW : UINT;\n    HIGG : UINT;\n  END_VAR\n\n  {{\n  union real_to_words {\n  uint16_t i[2];\n  float f;\n  }r2w;\n  r2w.f = INPP;\n  LOWW = r2w.i[0];\n  HIGG = r2w.i[1];\n  }}\nEND_FUNCTION\n\nPROGRAM robot\n  VAR\n    STATE_STATION_w1 AT %IW100 : UINT;\n    STATION_w1 AT %IW102 : UINT;\n    STATION_w2 AT %IW103 : UINT;\n    STATE_STATION_w2 AT %IW101 : UINT;\n    WORD3 AT %MD0 : REAL;\n    WORD6 AT %MD1 : REAL;\n    ROBOT_STATE_w1 AT %QW100 : UINT;\n    ROBOT_STATE_w2 AT %QW101 : UINT;\n  END_VAR\n  VAR\n    control0 : control;\n    function18_OUT : BOOL;\n    function18_WORDSTOREAL : REAL;\n    function116_OUT : BOOL;\n    function116_WORDSTOREAL : REAL;\n    prova9_OUT : BOOL;\n    prova9_LOWW : UINT;\n    prova9_HIGG : UINT;\n  END_VAR\n\n  function18_OUT := function1(LOWWORD := STATE_STATION_w2, HIGHWORD := STATE_STATION_w1, WORDSTOREAL => function18_WORDSTOREAL);\n  WORD3 := function18_WORDSTOREAL;\n  function116_OUT := function1(LOWWORD := STATION_w2, HIGHWORD := STATION_w1, WORDSTOREAL => function116_WORDSTOREAL);\n  control0(VALORE := function18_WORDSTOREAL, VALORE2 := function116_WORDSTOREAL);\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\n  ROBOT_STATE_w2 := prova9_LOWW;\n  ROBOT_STATE_w1 := prova9_HIGG;\n  WORD6 := function116_WORDSTOREAL;\nEND_PROGRAM\n\n\nCONFIGURATION Config0\n\n  RESOURCE Res0 ON PLC\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\n    PROGRAM instance0 WITH task0 : robot;\n  END_RESOURCE\nEND_CONFIGURATION\n"}]
#st2 = [{'plcName': 'plc1', 'name': 'robot_control.st', 'value': 'FUNCTION function1 : BOOL\n  VAR_INPUT\n    LOWWORD : UINT;\n    HIGHWORD : UINT;\n  END_VAR\n  VAR_OUTPUT\n    WORDSTOREAL : REAL;\n  END_VAR\n\n  {{\n  union words_to_real {\n  uint16_t i[2];\n  float f;\n  }w2r;\n  w2r.i[0] = LOWWORD;\n  w2r.i[1] = HIGHWORD;\n  WORDSTOREAL = w2r.f;\n  }}\nEND_FUNCTION\n\nFUNCTION_BLOCK control\n  VAR_INPUT\n    VALORE : REAL;\n    VALORE2 : REAL;\n  END_VAR\n  VAR_OUTPUT\n    controll : REAL;\n  END_VAR\n\n  IF (VALORE = 0.0 and VALORE2 = 0.0) THEN\n    controll := 1.0;\n  ELSIF (VALORE = 0.0 and VALORE2 = 1.0) THEN\n    controll := 0.0;\n  ELSIF (VALORE = 1.0 and VALORE2 = 1.0) THEN\n    controll := 1.0;\n  END_IF; \nEND_FUNCTION_BLOCK\n\nFUNCTION prova : BOOL\n  VAR_INPUT\n    INPP : REAL;\n  END_VAR\n  VAR_OUTPUT\n    LOWW : UINT;\n    HIGG : UINT;\n  END_VAR\n\n  {{\n  union real_to_words {\n  uint16_t i[2];\n  float f;\n  }r2w;\n  r2w.f = INPP;\n  LOWW = r2w.i[0];\n  HIGG = r2w.i[1];\n  }}\nEND_FUNCTION\n\nPROGRAM robot\n  VAR\n    STATE_STATION_w1 AT %IW100 : UINT;\n    STATION_w1 AT %IW102 : UINT;\n    STATION_w2 AT %IW103 : UINT;\n    STATE_STATION_w2 AT %IW101 : UINT;\n    WORD3 AT %MD0 : REAL;\n    WORD6 AT %MD1 : REAL;\n    ROBOT_STATE_w1 AT %QW100 : UINT;\n    ROBOT_STATE_w2 AT %QW101 : UINT;\n  END_VAR\n  VAR\n    control0 : control;\n    function18_OUT : BOOL;\n    function18_WORDSTOREAL : REAL;\n    function116_OUT : BOOL;\n    function116_WORDSTOREAL : REAL;\n    prova9_OUT : BOOL;\n    prova9_LOWW : UINT;\n    prova9_HIGG : UINT;\n  END_VAR\n\n  function18_OUT := function1(LOWWORD := STATE_STATION_w2, HIGHWORD := STATE_STATION_w1, WORDSTOREAL => function18_WORDSTOREAL);\n  WORD3 := function18_WORDSTOREAL;\n  function116_OUT := function1(LOWWORD := STATION_w2, HIGHWORD := STATION_w1, WORDSTOREAL => function116_WORDSTOREAL);\n  control0(VALORE := function18_WORDSTOREAL, VALORE2 := function116_WORDSTOREAL);\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\n  ROBOT_STATE_w2 := prova9_LOWW;\n  ROBOT_STATE_w1 := prova9_HIGG;\n  WORD6 := function116_WORDSTOREAL;\nEND_PROGRAM\n\n\nCONFIGURATION Config0\n\n  RESOURCE Res0 ON PLC\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\n    PROGRAM instance0 WITH task0 : robot;\n  END_RESOURCE\nEND_CONFIGURATION\n'}]


#data={'MODEL': {'modeler': 'matlab', 'name': 'aiv_robot', 'os': 'windows.7', 'interface': 'modbus', 'opc_parameters': {'actuators': 'speed=0.3, start=1, nextWaypoints=0, plc_control=0', 'sensors': 'position_X, position_Y, station, state_station'}}, 'MTU': {'name': 'Node_11', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': 'Node_10', 'os': 'ubuntu', 'input': 'state_station, station', 'output_slave': 'plc_control', 'plc_code': 'robot_control.st'}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'Node_12', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=net1 dst=net0'}, {'rule': 'src=net0 dst=net1'}]}]}, 'NETWORKS': {'name': 'net1; net0', 'members': 'aiv_robot, Node_10; Node_11', 'gateway': 'Node_12; Node_12'}, 'CONFIG': {'entry_point': 'Node_11', 'cyber_range_id': 123, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': '', 'log_type': ''}}

#with open(r'/home/ubuntu/virtualTestbed/models/openmodelica/tankmodel_2/config1_5.yaml') as f:
#    data = yaml.safe_load(f)


#a=converter(data,"900")
#print(a)
