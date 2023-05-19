import subprocess
from subprocess import Popen
import os
import json


def start_scenario(values):

    path_temp_script = values[4]
    path = values[5]

    os.system("sudo chmod +x {}/script_after_clone.sh".format(path_temp_script))
    #res = subprocess.Popen("sudo '{}/cyris/main/cyris.py' -v '{}/cyris/examples/cyberrange.yml' '{}/cyris/CONFIG' && {}/script_after_clone.sh".format(path, path, path, path_temp_script), stdout=subprocess.PIPE,
    #                       stderr=subprocess.PIPE,
    #                       encoding="utf-8", shell=True)
    res = subprocess.Popen(
        "sudo '{}/cyris/main/cyris.py' -v '{}/cyris/examples/cyberrange.yml' '{}/cyris/CONFIG' && {}/script_after_clone.sh".format(
            path, path, path, path_temp_script),
        stderr=subprocess.PIPE,
        encoding="utf-8", shell=True)

    if res.wait() != 0:
        output, error = res.communicate()
        subprocess.Popen("sudo rm -r {}/".format(path_temp_script),stderr=subprocess.PIPE,encoding="utf-8", shell=True)
        #return error
        return "error: check the configuration of scenario!"

    else: return "000" + str(json.dumps("Scenario Ready"))


