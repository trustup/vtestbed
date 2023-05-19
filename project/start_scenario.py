import os
import yaml
import yaml_converter_auto
import start_scenario_auto
import sys

#CARICAMENTO FILE YAML
#with open(r'/home/ubuntu/PycharmProjects/config1_5_9.yaml') as f:
#    data = yaml.safe_load(f)

# FILES ST
#with open('/home/ubuntu/cyris/models/matlab/aiv_robot/other_files/robot_control.st') as f:
#    stread = f.read()
#st_construct = [{"plcName":"plc1", "name":"robot_control.st","value": '{}'.format(stread)}]

with open(r'{}'.format(sys.argv[1])) as f:
    data = yaml.safe_load(f)
CODE_START = '900'

#GENERAZIONE FILES
value = yaml_converter_auto.converter(data, CODE_START) #passo lo yaml al convertitore
print(value)
start_scenario_auto.start_scenario(value)


# os.system("python /home/ubuntu/PycharmProjects/project/yaml_converter.py")
# os.system("sudo chmod +x /home/ubuntu/PycharmProjects/temp/{}/script_after_clone.sh".format(numb_cyber))
# os.system("sudo '{}/cyris/main/cyris.py' -v '{}/cyris/examples/cyberrange.yml' '{}/cyris/CONFIG' && /home/ubuntu/PycharmProjects/temp/{}/script_after_clone.sh".format(path, path, path,numb_cyber))
# print("You can connect via SSH using: ")
#os.system("grep -r 'Login' /home/ubuntu/cyris/cyber_range/{}/range_notification-cr{}.txt".format(numb_cyber, numb_cyber))
#os.system("grep -r 'Password' /home/ubuntu/cyris/cyber_range/{}/range_notification-cr{}.txt".format(numb_cyber, numb_cyber))



