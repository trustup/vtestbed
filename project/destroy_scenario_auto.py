import subprocess

def destroy_scenario(values):

    path = values[5]
    path_temp_script = values[4]
    cyber_number = values[3]


    res = subprocess.Popen(
        "sudo '{}/cyris/main/range_cleanup.py' {} '{}/cyris/CONFIG';sudo '{}/cyris/main/range_cleanup.py' {} '{}/cyris/CONFIG'".format(
            path, cyber_number, path,path, cyber_number, path),
        stderr=subprocess.PIPE,
        encoding="utf-8", shell=True)

    if res.wait() != 0:
        output, error = res.communicate()
        return error

    else:
        subprocess.Popen("sudo rm -r {}/".format(path_temp_script), stderr=subprocess.PIPE, encoding="utf-8",
                         shell=True)
        return 'Scenario Destroyed'

