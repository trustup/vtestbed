import sys
import yaml
import restart_scenario_auto
# import os
# import time
# import socket
# from yaml_converter2 import total_number_vm2
# from yaml_converter2 import exp
# from yaml_converter2 import ip_list
# from yaml_converter2 import numb_cyber
#
# #list_vm = [x.replace(".eth0","") for x in total_number_vm2]
#
# list_vm = total_number_vm2
# if exp != None:
#     list_vm.append(exp)
#
# for x in list_vm:
#     os.system("virsh start {}_cr{}_1_1 >/dev/null".format(x, numb_cyber))
#
# for y in list_vm :
#     finished = False
#     while not finished:
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             s.connect(('{}'.format(ip_list[y + '.eth0'][0]), 22))
#             print(y + " is up!")
#             finished = True
#         except socket.error as e:
#             #print('"Error on connect: %s"' % e)
#             print(y + " is down ..retry")
#             time.sleep(5)
#         s.close()
#
# os.system("sudo chmod +x /home/ubuntu/PycharmProjects/temp/script_after_clone_restart.sh")
# os.system("sudo /home/ubuntu/PycharmProjects/temp/script_after_clone_restart.sh")
# print("Scenario Ready!")
#
# #print(finished)

path = '/home/ubuntu/virtualTestbed/temp/{}/values.yml'.format(sys.argv[1])

#CARICAMENTO FILE VALUES YAML
with open(r'{}'.format(path)) as f:
    data = yaml.safe_load(f)

restart_scenario_auto.restart(data)