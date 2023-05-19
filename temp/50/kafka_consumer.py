from kafka import KafkaConsumer
import json
import os
import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.defines as cst

consumer = KafkaConsumer('testbed', bootstrap_servers=['192.168.1.179:9092'], auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000, group_id='my-group', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:

    try:
        if message[6]['50']['asset_name'] == 'plc1':
            for z in range(4):
                try:
                    if message[6]['50']['actions'][z]['action_type'] == 'power_management':
                        if message[6]['50']['actions'][z]['commands'][0]['action_name'] == 'stop':
                            os.system('sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.3 "systemctl stop openplc.service"')
                        if message[6]['50']['actions'][z]['commands'][0]['action_name'] == 'start':
                            data = "systemctl start openplc.service; su -c 'python3 /home/ubuntu//script_selenium_plc1_restart.py' - ubuntu &>/dev/null &"
                            os.system('sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.3 "{}"'.format(data))
                    if message[6]['50']['actions'][z]['action_type'] == 'update_firmware':
                        if message[6]['50']['actions'][z]['commands'][0]['action_name'] == 'disable':
                            cmd = r's/value=\"Upload Program\" name=\"submit\"/value=\"Upload Program\" name=\"submit\" disabled/g'
                            data = "systemctl stop openplc.service;sed -i '{}' /bin/cyberrange/OpenPLC_v3/webserver/webserver.py;systemctl start openplc.service;su -c 'python3 /home/ubuntu/script_selenium_plc1_restart.py' - ubuntu &>/dev/null &".format(cmd)
                            os.system('sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.3 "{}"'.format(data))
                        if message[6]['50']['actions'][z]['commands'][0]['action_name'] == 'enable':
                            cmd = r's/value=\"Upload Program\" name=\"submit\" disabled/value=\"Upload Program\" name=\"submit\"/g'
                            data = "systemctl stop openplc.service;sed -i '{}' /bin/cyberrange/OpenPLC_v3/webserver/webserver.py;systemctl start openplc.service;su -c 'python3 /home/ubuntu/script_selenium_plc1_restart.py' - ubuntu &>/dev/null &".format(cmd)
                            os.system('sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.3 "{}"'.format(data))
                except:
                    continue
    except:
        continue
