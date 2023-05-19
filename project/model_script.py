def script_for_model(modeler, model, model_os, rtu, dst_script_ubuntu, interface, path_temp_script):

    #path python.exe on windows - User account: winuser
    path_python_win = r'C:\Users\winuser\AppData\Local\Programs\Python\Python37\python.exe'

    if modeler == 'openmodelica':
        if model_os[0] == 'windows.7':
            with open(r'{}/script.bat'.format(path_temp_script), 'w') as f:
                f.write("cd C:\CyberRange\modelica\n")
                f.write(
                    'START /B /REALTIME "" C:\CyberRange\modelica\{}.exe -embeddedServer=opc-ua -rt=1 >null\n'.format(
                        model[0]))
                if len(rtu) == 0:
                    f.write('START /B /REALTIME "" C:\CyberRange\modelica\diagslave.exe -m tcp >null2\n')
                f.write('START /B /REALTIME "" python opc_modbus.py >null\n')


        else:
            with open(r'{}/script.sh'.format(path_temp_script), 'w') as f:
                f.write("#!/bin/bash\n")
                #f.write("mkdir /home/ubuntu/{}\n".format(model[0]))
                #f.write("tar -C {}{} -xvf {}{}.tar.gz\n".format(dst_script_ubuntu, model[0], dst_script_ubuntu, model[0]))
                #f.write(("cp /home/ubuntu/diagslave /home/ubuntu/{}\n".format(model[0])))
                f.write("cd {}{}/\n".format(dst_script_ubuntu, model[0]))
                f.write("{}{}/{} -embeddedServer=opc-ua -rt=1 &>/dev/null &\n".format(dst_script_ubuntu, model[0], model[0]))
                f.write("python3 {}{}.py &>/dev/null &\n".format(dst_script_ubuntu, interface))
                #if len(rtu) == 0: f.write("{}{}/diagslave -m tcp &\n".format(dst_script_ubuntu, model[0]))
                f.write("su -c 'python3 {}opc_{}.py' - ubuntu &>/dev/null &\n".format(dst_script_ubuntu, interface))

                #f.write("python3 {}opc_{}.py - ubuntu\n".format(dst_script_ubuntu, interface))
                #f.write("exit 0")
            f.close()

    elif modeler == 'matlab':
        if model_os[0] == 'windows.7' and interface == 'modbus':
            with open(r'{}/script1.bat'.format(path_temp_script), 'w') as f: #script for root
                f.write('cd C:\CyberRange\n')
                f.write('START /B /REALTIME "" {} modbus.py > null\n'.format(path_python_win))
                f.write('START /B /REALTIME "" {} server_opcua.py > null2\n'.format(path_python_win))
            with open(r'{}/script2.bat'.format(path_temp_script), 'w') as f: #script for user
                f.write('cd C:\CyberRange\n')
                f.write('START /B /REALTIME "" {} opc_modbus.py > null3\n'.format(path_python_win))
                f.write('{}.exe\n'.format(model[0]))