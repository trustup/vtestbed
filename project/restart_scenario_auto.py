import os
import time
import socket
import subprocess
from subprocess import Popen
#from yaml_converter2 import total_number_vm2
#from yaml_converter2 import exp
#from yaml_converter2 import ip_list
#from yaml_converter2 import numb_cyber

def restart(values):
    print(values)
    ip_list = values[0]
    total_number_vm2 = values[1]
    #total_number_vm2 = ['tankmodel','router-gw']
    exp = values[2]
    #numb_cyber = 150
    numb_cyber = values[3]
    path_temp_script = values[4]
    try:
        list_vm = total_number_vm2
        if exp != None:
            list_vm.append(exp)

        #try:
        #    for x in list_vm:
        #        cmd = os.system("virsh start {}_cr{}_1_1 >/dev/null".format(x, numb_cyber))
        #        print(cmd)
        #        if cmd != 0:
        #            raise Exception
        #except ValueError:
        #    print(ValueError)
        #    if cmd == 256:
        #        error = 'ERROR: The domain is already running'
        #    return error
        for x in list_vm:
            res = subprocess.Popen("virsh start {}_cr{}_1_1".format(x, numb_cyber), stdout=subprocess.PIPE,
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
                    print(y + " is up!")
                    finished = True
                except socket.error as e:
                    # print('"Error on connect: %s"' % e)
                    print(y + " is down ..retry")
                    time.sleep(5)
                s.close()

        os.system("sudo chmod +x {}/script_after_clone_restart.sh".format(path_temp_script))
        os.system("sudo {}/script_after_clone_restart.sh".format(path_temp_script))

        #print("Scenario Ready!")
        return "Restart Complete!"

    except Exception as error:
        return 'error: ' + str(error)