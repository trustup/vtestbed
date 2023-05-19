import os
import time
import socket
import sys
import yaml
import close_scenario_auto
# from yaml_converter2 import total_number_vm2
# from yaml_converter2 import exp
# from yaml_converter2 import ip_list
# from yaml_converter2 import numb_cyber
#
# #list_vm = [x.replace(".eth0","") for x in total_number_vm2]
# list_vm = total_number_vm2
# if exp != None:
#     list_vm.append(exp)
#
# for x in list_vm:
#     os.system("virsh shutdown {}_cr{}_1_1".format(x, numb_cyber))
#
# for y in list_vm :
#     finished = False
#     while not finished:
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             s.connect(('{}'.format(ip_list[y + '.eth0'][0]), 22))
#             time.sleep(1)
#         except socket.error as e:
#             #print(y + 'close')
#             finished = True
#         s.close()
#
# print("scenario closed")

path = '/home/ubuntu/virtualTestbed/temp/{}/values.yml'.format(sys.argv[1])

#CARICAMENTO FILE VALUES YAML
with open(r'{}'.format(path)) as f:
    data = yaml.safe_load(f)

close_scenario_auto.close_scenario(data)