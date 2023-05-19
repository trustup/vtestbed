def logstash_config(ip, source, log_type, topic, port_kafka, port_beats, path_temp_script):
    #function that receives data from filebeat on vms and export data to kafka

    sipsId = "Pilot2"
    sourceId = "ST.APP.6.2"
    X = 51.83116
    Y = -8.27483
    with open(r'{}/setting.conf'.format(path_temp_script), 'w') as f:
        f.write("\ninput {\n\n")
        f.write("  beats {\n")
        f.write("    port => {}\n".format(port_beats))
        f.write("  }\n")
        f.write("\n}\n")

        f.write("\nfilter {\n")
        f.write("  mutate {\n")
        f.write('    add_field => {"id" => "93893893"}\n')
        f.write('    add_field => {"partner" => "CINI"}\n')
        f.write('    add_field => {"version" => "1.0"}\n')
        f.write('    add_field => {"sipsId" => "')
        f.write('{}'.format(sipsId))
        f.write('"}\n')
        f.write('    add_field => {"sourceId" => "')
        f.write('{}'.format(sourceId))
        f.write('"}\n')
        f.write('    add_field => {"[location][coordinatePairs]" => ')
        f.write('[{},{}]'.format(X,Y))
        f.write('}\n')
        f.write('    add_field => {"[location][impactRadius]" => 2}\n')
        f.write('    add_field => {"[location][geometryType]" => "Point"}\n')
        f.write('    rename => ["[host][name]", "[host]"]\n')
        f.write('    rename => ["@timestamp", "timestamp"]\n')
        f.write('    remove_field => ["agent","log","@version","input","ecs"]\n')
        f.write('  }\n')
        f.write('  uuid {\n')
        f.write('    target => "id"\n')
        f.write('    overwrite => true\n')
        f.write('  }\n')

        f.write('  ruby {\n')
        f.write("    code => '")
        f.write('event.set("sipsElements", [{"id" => "SCADA_element", "elementType" => "CP_Asset", "assetType" => "cyber/virtualTestbed"}])')
        f.write("'\n")
        f.write('  }\n')

        f.write('  mutate {\n')
        f.write('    convert => {\n')
        f.write('      "[location][impactRadius]" => "integer"\n')
        f.write('      "[location][coordinatePairs]" => "float"\n')
        f.write('    }\n')
        f.write('  }\n')
        f.write("}\n")

        ########
        ######## OUTPUT FOR SINGLE TOPIC ##############
        # f.write("\noutput {\n\n")
        # #insert_topic = '%{[tags][0]}'
        # insert_topic = topic
        # for idx, x in enumerate(source):
        #     tags = log_type[idx].split(',')
        #     if idx == 0:
        #         f.write('  if [host] == "{}"'.format(x))
        #         f.write(' {\n')
        #         #for y in tags:
        #         #    f.write('    if "{}" in [tags]:'.format(y))
        #             #f.write(' {\n')
        #         f.write('      kafka {\n')
        #         f.write('        bootstrap_servers => "{}:{}" \n'.format(ip,port_kafka))
        #         #f.write("        topic_id => '{}.{}' \n".format(x,insert_topic))
        #         f.write("        topic_id => '{}'\n".format(insert_topic))
        #         f.write('        codec => json\n')
        #         f.write('      }\n')
        #         f.write('  }')
        #     else :
        #         f.write(' else if [host] == "{}"'.format(x))
        #         f.write(' {\n')
        #         #for y in tags:
        #         #    f.write('    if "{}" in [tags]:'.format(y))
        #         #    f.write(' {\n')
        #         f.write('      kafka {\n')
        #         f.write('        bootstrap_servers => "{}:{}" \n'.format(ip, port_kafka))
        #         #f.write("        topic_id => '{}.{}' \n".format(x,insert_topic))
        #         f.write("        topic_id => '{}'\n".format(insert_topic))
        #         f.write("        codec => json\n")
        #         f.write('      }\n')
        #         f.write('  }\n')
        # f.write("\n}\n")

        ##########
        ########## OUTPUT FOR MULTIPLE TOPIC, SYNTAX es: plc1.login, mtu-hmi.topic, mtu-hmi.tomcat #################
        f.write("\noutput {\n\n")
        insert_topic = '%{[tags][0]}'
        for idx, x in enumerate(source):
            tags = log_type[idx].split(',')
            if idx == 0:
                f.write('  if [host] == "{}"'.format(x))
                f.write(' {\n')
                for y in tags:
                    f.write('    if "{}" in [tags]'.format(y))
                    f.write(' {\n')
                    f.write('      kafka {\n')
                    f.write('        bootstrap_servers => "{}:{}" \n'.format(ip, port_kafka))
                    f.write("        topic_id => '{}.{}' \n".format(x,insert_topic))
                    f.write('        codec => json\n')
                    f.write('      }\n')
                    f.write('    }\n')
                f.write('  }')
            else:
                f.write(' else if [host] == "{}"'.format(x))
                f.write(' {\n')
                for y in tags:
                    f.write('      if "{}" in [tags]'.format(y))
                    f.write(' {\n')
                    f.write('        kafka {\n')
                    f.write('          bootstrap_servers => "{}:{}" \n'.format(ip, port_kafka))
                    f.write("          topic_id => '{}.{}' \n".format(x,insert_topic))
                    f.write("          codec => json\n")
                    f.write('        }\n')
                    f.write('      }\n')
                f.write('    }\n')
        f.write("\n}\n")

    f.close()






########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
def kafka_consumer(numb_cyber, path_temp_script, dst_script_ubuntu, ip_export, port_kafka, name_topic, ip_list,model, interface,sensors,act_wv, plc, plc_os):
    # function that reads data from kafka and performs actions to vms

    with open(r'{}/kafka_consumer.py'.format(path_temp_script), 'w') as f:
        f.write("from kafka import KafkaConsumer\n")
        f.write("import json\n")
        f.write("import os\n")
        f.write("import modbus_tk.modbus_tcp as modbus_tcp\nimport modbus_tk.defines as cst\n\n")

        f.write("consumer = KafkaConsumer('{}', bootstrap_servers=['{}:{}'], auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000, group_id='my-group', value_deserializer=lambda x: json.loads(x.decode('utf-8')))\n\n".format(name_topic, ip_export, port_kafka))

        #ACTIONS
        f.write("for message in consumer:\n\n")

        # specific command for aiv_robot model
        if model[0] == 'aiv_robot' and interface == 'modbus':
            address = sensors + act_wv
            f.write('    master = modbus_tcp.TcpMaster(host="{}", port=502)\n'.format(ip_list['{}'.format(model[0]) + '.eth0'][0]))
            for idx, x in enumerate(address):
                if x == 'start':
                    f.write("    try:\n")
                    f.write("        if message[6]['{}']['asset_name'] == '{}':\n".format(numb_cyber, model[0]))
                    f.write("            if message[6]['{}']['actions'][0]['action_type'] == 'power_management':\n".format(numb_cyber))
                    f.write("                if message[6]['{}']['actions'][0]['commands'][0]['action_name'] == 'off':\n".format(numb_cyber))
                    f.write("                    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address={}, output_value=[0.0], data_format='>f')\n\n".format(idx * 2))

                    f.write("                if message[6]['{}']['actions'][0]['commands'][0]['action_name'] == 'on':\n".format(numb_cyber))
                    f.write("                    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address={}, output_value=[1.0], data_format='>f')\n\n".format(idx * 2))
                    f.write("    except:\n")
                    f.write("        continue\n\n")

        # commands for PLCs (for ubuntu)
        if len(plc) != 0 and plc_os[0] == 'ubuntu':
            for x in plc:
                f.write("    try:\n")
                f.write("        if message[6]['{}']['asset_name'] == '{}':\n".format(numb_cyber, x))
                f.write("            for z in range(4):\n")
                f.write("                try:\n")
                f.write("                    if message[6]['{}']['actions'][z]['action_type'] == 'power_management':\n".format(numb_cyber))
                f.write("                        if message[6]['{}']['actions'][z]['commands'][0]['action_name'] == 'stop':\n".format(numb_cyber))
                cmd1 = 'systemctl stop openplc.service'
                ssh_cmd = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x)+'.eth0'][0], cmd1)
                f.write("                            os.system('{}')\n".format(ssh_cmd))
                f.write("                        if message[6]['{}']['actions'][z]['commands'][0]['action_name'] == 'start':\n".format(numb_cyber))
                f.write('                            data = "')
                f.write("systemctl start openplc.service; su -c 'python3 {}/script_selenium_{}_restart.py' - ubuntu &>/dev/null &".format(dst_script_ubuntu, x))
                f.write('"\n')
                command = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x) + '.eth0'][0], '{}')
                f.write("                            os.system('{}'.format(data))\n".format(command))

                f.write("                    if message[6]['{}']['actions'][z]['action_type'] == 'update_firmware':\n".format(numb_cyber))
                f.write("                        if message[6]['{}']['actions'][z]['commands'][0]['action_name'] == 'disable':\n".format(numb_cyber))
                f.write("                            cmd = r'")
                f.write(r's/value=\"Upload Program\" name=\"submit\"/value=\"Upload Program\" name=\"submit\" disabled/g')
                f.write("'\n")
                f.write('                            data = "')
                f.write("systemctl stop openplc.service;sed -i '{}' /bin/cyberrange/OpenPLC_v3/webserver/webserver.py;systemctl start openplc.service;su -c 'python3 {}script_selenium_{}_restart.py' - ubuntu &>/dev/null &".format('{}', dst_script_ubuntu, x))
                f.write('".format(cmd)\n')
                command = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x) + '.eth0'][0], '{}')
                f.write("                            os.system('{}'.format(data))\n".format(command))
                f.write("                        if message[6]['{}']['actions'][z]['commands'][0]['action_name'] == 'enable':\n".format(numb_cyber))
                f.write("                            cmd = r'")
                f.write(r's/value=\"Upload Program\" name=\"submit\" disabled/value=\"Upload Program\" name=\"submit\"/g')
                f.write("'\n")
                f.write('                            data = "')
                f.write("systemctl stop openplc.service;sed -i '{}' /bin/cyberrange/OpenPLC_v3/webserver/webserver.py;systemctl start openplc.service;su -c 'python3 {}script_selenium_{}_restart.py' - ubuntu &>/dev/null &".format('{}', dst_script_ubuntu, x))
                f.write('".format(cmd)\n')
                command = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x) + '.eth0'][0], '{}')
                f.write("                            os.system('{}'.format(data))\n".format(command))

                f.write("                except:\n")
                f.write("                    continue\n")
                f.write("    except:\n")
                f.write("        continue\n")






        f.close()
    # with open(r'{}/kafka_consumer.py'.format(path_temp_script), 'w') as f:
    #     f.write("from kafka import KafkaConsumer\n")
    #     f.write("import json\n")
    #     f.write("import os\n")
    #     f.write("import modbus_tk.modbus_tcp as modbus_tcp\nimport modbus_tk.defines as cst\n\n")
    #
    #     f.write("consumer = KafkaConsumer('{}', bootstrap_servers=['{}:{}'], auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000, group_id='my-group', value_deserializer=lambda x: json.loads(x.decode('utf-8')))\n\n".format(name_topic, ip_export, port_kafka))
    #
    #     #ACTIONS
    #     f.write("for message in consumer:\n\n")
    #
    #     # specific command for aiv_robot model
    #     if model[0] == 'aiv_robot' and interface == 'modbus':
    #         address = sensors + act_wv
    #         f.write('    master = modbus_tcp.TcpMaster(host="{}", port=502)\n'.format(ip_list['{}'.format(model[0]) + '.eth0'][0]))
    #         for idx, x in enumerate(address):
    #             if x == 'start':
    #                 f.write("    if list(message[6])[0] == 'model':\n")
    #                 f.write("        if message[6]['model'] == 'stop_aiv_robot':\n")
    #                 f.write("            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address={}, output_value=[0.0], data_format='>f')\n\n".format(idx * 2))
    #
    #                 f.write("        if message[6]['model'] == 'start_aiv_robot':\n")
    #                 f.write("            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address={}, output_value=[1.0], data_format='>f')\n\n".format(idx * 2))
    #
    #     # commands for PLCs (for ubuntu)
    #     if len(plc) != 0 and plc_os[0] == 'ubuntu':
    #         for x in plc:
    #             f.write("    if list(message[6])[0] == 'plc':\n")
    #             f.write("        if message[6]['plc'] == 'stop':\n")
    #             cmd1 = 'systemctl stop openplc.service'
    #             ssh_cmd = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x)+'.eth0'][0], cmd1)
    #             f.write("            os.system('{}')\n".format(ssh_cmd))
    #
    #             f.write("        if message[6]['plc'] == 'start':\n")
    #             f.write('            data = "')
    #             f.write("systemctl start openplc.service; su -c 'python3 {}/script_selenium_{}_restart.py' - ubuntu &>/dev/null &".format(dst_script_ubuntu, x))
    #             f.write('"\n')
    #             command = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x)+'.eth0'][0],'{}')
    #             f.write("            os.system('{}'.format(data))\n".format(command))
    #
    #             f.write("        if message[6]['plc'] == 'disable_upload':\n")
    #             f.write("            cmd = r'")
    #             f.write(r's/value=\"Upload Program\" name=\"submit\"/value=\"Upload Program\" name=\"submit\" disabled/g')
    #             f.write("'\n")
    #             f.write('            data = "')
    #             f.write("systemctl stop openplc.service;sed -i '{}' /bin/cyberrange/OpenPLC_v3/webserver/webserver.py;systemctl start openplc.service;su -c 'python3 {}script_selenium_{}_restart.py' - ubuntu &>/dev/null &".format('{}',dst_script_ubuntu, x))
    #             f.write('".format(cmd)\n')
    #             command = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x) + '.eth0'][0], '{}')
    #             f.write("            os.system('{}'.format(data))\n".format(command))
    #
    #             f.write("        if message[6]['plc'] == 'enable_upload':\n")
    #             f.write("            cmd = r'")
    #             f.write(
    #                 r's/value=\"Upload Program\" name=\"submit\" disabled/value=\"Upload Program\" name=\"submit\"/g')
    #             f.write("'\n")
    #             f.write('            data = "')
    #             f.write("systemctl stop openplc.service;sed -i '{}' /bin/cyberrange/OpenPLC_v3/webserver/webserver.py;systemctl start openplc.service;su -c 'python3 {}script_selenium_{}_restart.py' - ubuntu &>/dev/null &".format('{}', dst_script_ubuntu, x))
    #             f.write('".format(cmd)\n')
    #             command = 'sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@{} "{}"'.format(ip_list['{}'.format(x) + '.eth0'][0], '{}')
    #             f.write("            os.system('{}'.format(data))".format(command))
    #
    #
    #
    #
    #     f.close()
