import sys
import yaml
import destroy_scenario_auto
# import os
# import  sys
# from yaml_converter2 import path
# from yaml_converter2 import numb_cyber
# from yaml_converter2 import interface
# sys.path.append('home/ubuntu/PycharmProjects/project/TestBed')
#
# os.system("sudo '{}/cyris/main/range_cleanup.py' {} '{}/cyris/CONFIG'".format(path, numb_cyber, path))
# os.system("rm * home/ubuntu/PycharmProjects/temp/")
# #os.system("rm {}/cyris/examples/cyberrange.yml".format(path))
# #os.system("rm {}/PycharmProjects/temp/opc_{}.py".format(path,interface))
# #os.system("rm {}/PycharmProjects/temp/script.sh".format(path))
# #os.system("rm /home/ubuntu/PycharmProjects/temp/script_after_clone_restart.sh")
# #os.system("rm /home/ubuntu/PycharmProjects/temp/script_after_clone.sh")
# #os.system("rm /home/ubuntu/PycharmProjects/temp/script_selenium.py")
# #os.system("rm /home/ubuntu/PycharmProjects/temp/data.json")
#
# print("COMPLETED")

path = '/home/ubuntu/virtualTestbed/temp/{}/values.yml'.format(sys.argv[1])

#CARICAMENTO FILE VALUES YAML
with open(r'{}'.format(path)) as f:
    data = yaml.safe_load(f)

destroy_scenario_auto.destroy_scenario(data)