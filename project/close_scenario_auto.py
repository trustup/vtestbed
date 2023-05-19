import os
import time
import socket
import subprocess
from subprocess import Popen

def close_scenario(values):
    ip_list = values[0]
    total_number_vm2 = values[1]
    #total_number_vm2 = ['tankmodel', 'router-gw']
    exp = values[2]
    #numb_cyber = 150
    numb_cyber = values[3]

    try:
        list_vm = total_number_vm2
        if exp != None:
            list_vm.append(exp)

        # try:
        #     for x in list_vm:
        #         os.system("virsh shutdown {}_cr{}_1_1".format(x, numb_cyber))
        # except:
        #     return Exception
        for x in list_vm:
            res = subprocess.Popen("virsh shutdown {}_cr{}_1_1".format(x, numb_cyber),
                                   stderr=subprocess.PIPE,
                                   encoding="utf-8", shell=True)
            if res.wait() != 0:
                output, error = res.communicate()
                return error

        for y in list_vm:
            finished = False
            while not finished:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('{}'.format(ip_list[y + '.eth0'][0]), 22))
                    time.sleep(1)
                except socket.error as e:
                    # print(y + 'close')
                    finished = True
                s.close()

        return 'Close Scenario completed'

    except Exception as error:
        return str(error)