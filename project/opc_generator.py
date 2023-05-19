# def opc_modbus(interface, address_modbus, url, sensors, actuators):
#
#     length_holding_reg = 100
#     with open(r'/home/ubuntu/PycharmProjects/temp/opc_{}.py'.format(interface), 'w') as f:
#         f.write("import time\nimport timeit\nimport opcua\nfrom opcua import Client\nfrom opcua import ua\n")
#         f.write("import modbus_tk\nimport modbus_tk.defines as cst\nimport modbus_tk.modbus_tcp as modbus_tcp\nimport struct\n\n")
#
#         f.write('def unpack_float(fl):\n')
#         f.write("    a = struct.unpack('>HH', struct.pack('>f',fl))\n")
#         f.write("    return(a)\n\n")
#
#         f.write('class SubHandler(object):\n')
#         f.write('    def datachange_notification(self, node, val, data):\n')
#         f.write('        for idx, x in enumerate(nodes):\n')
#         f.write('            if node == nodes[idx]:\n')
#         f.write('                ad=idx*2\n')
#         f.write('                value = unpack_float(val)\n')
#         f.write('                slave.set_values("a", ad, value)\n\n')
#         #f.write("                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')\n\n")
#
#         f.write('if __name__ == "__main__":\n\n')
#         f.write('    server = modbus_tcp.TcpServer()\n')
#         f.write('    server.start()\n')
#         f.write('    master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)\n')
#         f.write('    slave1 = server.add_slave(1)\n')
#         f.write('    slave1.add_block("a", cst.HOLDING_REGISTERS, 0, {})\n'.format(length_holding_reg))
#         f.write('    slave = server.get_slave(1)\n\n')
#         f.write('    url = "{}"\n'.format(url))
#         f.write("    client = Client(url, timeout=100)\n    client.connect()\n\n")
#         f.write('    nodes = []\n')
#         f.write('    root = client.get_objects_node()\n')
#         f.write('    obj = client.get_node(root)\n')
#         f.write("    run = obj.get_child('1:OpenModelica.run')\n")
#         f.write('\n   #sensors:\n')
#
#         for idx, x in enumerate(sensors):
#             f.write("    node{} = obj.get_child('1:{}')\n".format(idx + 1, x))
#             f.write("    nodes.append(node{})\n".format(idx + 1))
#         f.write("    len_sensors = {}\n".format(len(sensors)))
#         f.write('    run.set_value(True)\n')
#         if len(actuators) != 0:
#             f.write("    act=[]\n")
#             f.write("    ad = (len_sensors * 2) - 2\n")
#             for idx, x in enumerate(actuators):
#                 f.write("   #actuator {}\n".format(idx + 1))
#                 f.write("    node{} = obj.get_child('1:{}')\n".format(idx + 1 + len(sensors), x[0]))
#                 f.write("    node{}.set_value({})\n".format(idx + 1 + len(sensors), x[1]))
#                 f.write('    act.append({})\n'.format(x[1]))
#                 f.write("    ad = ad + 2\n")
#                 f.write("    wr = unpack_float({})\n".format(x[1]))
#                 f.write('    slave.set_values("a", ad, wr)\n')
#                 #f.write("    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[{}], data_format='>f')\n".format(x[1]))
#
#         f.write("\n    try:\n")
#         f.write('        handler = SubHandler()\n')
#         f.write('        sub = client.create_subscription(0, handler)\n')
#         f.write('        handle=sub.subscribe_data_change(nodes)\n')
#         f.write('        time.sleep(0.1)\n')
#
#         if len(actuators) != 0:
#             f.write("\n        while True:\n")
#             f.write("            for idx, x in enumerate(act):\n")
#             f.write("                r_a = (len_sensors * 2) + (idx * 2)\n")
#             f.write("                a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')\n")
#             f.write("                if a[0] != act[idx]:\n")
#             f.write("                    nodd = globals()['node{}'.format(len_sensors + 1 + idx)]\n")
#             f.write("                    nodd.set_value(a[0])\n")
#             f.write("                    act[idx] = a[0]\n")
#             f.write("                time.sleep(1)\n")
#
#         f.write("\n    finally:\n")
#         f.write("        print('..retry')\n")
#
#         f.close()
#
#     f.close()

def opc_modbus(interface, modeler, address_modbus, url, sensors, actuators, path_temp_script):

    if modeler == 'matlab':
        opc_index = 2
    else: opc_index = 1

    with open(r'{}/opc_{}.py'.format(path_temp_script,interface), 'w') as f:
        f.write("import time\nimport timeit\nimport opcua\nfrom opcua import Client\nfrom opcua import ua\n")
        f.write("import modbus_tk\nimport modbus_tk.defines as cst\nimport modbus_tk.modbus_tcp as modbus_tcp\n\n")
        f.write('class SubHandler(object):\n')
        f.write('    def datachange_notification(self, node, val, data):\n')
        f.write('        for idx, x in enumerate(nodes):\n')
        f.write('            if node == nodes[idx]:\n')
        f.write('                ad=idx*2\n')
        f.write(
            "                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')\n\n")

        f.write('if __name__ == "__main__":\n\n')
        f.write('    master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)\n')
        f.write('    url = "{}"\n'.format(url))
        f.write("    client = Client(url, timeout=100)\n    client.connect()\n\n")
        f.write('    nodes = []\n')
        f.write('    root = client.get_objects_node()\n')
        f.write('    obj = client.get_node(root)\n')
        if modeler == 'openmodelica':
            f.write("    run = obj.get_child('1:OpenModelica.run')\n")
            f.write('    run.set_value(True)\n')
        f.write('\n   #sensors:\n')

        for idx, x in enumerate(sensors):
            f.write("    node{} = obj.get_child('{}:{}')\n".format(idx + 1, opc_index, x))
            f.write("    nodes.append(node{})\n".format(idx + 1))
        f.write("    len_sensors = {}\n".format(len(sensors)))
        if len(actuators) != 0:
            f.write("    act=[]\n")
            f.write("    ad = (len_sensors * 2) - 2\n")
            for idx, x in enumerate(actuators):
                f.write("   #actuator {}\n".format(idx + 1))
                f.write("    node{} = obj.get_child('{}:{}')\n".format(idx + 1 + len(sensors), opc_index, x[0]))

                #####add reading also for actuators
                f.write("    nodes.append(node{})\n".format(idx + 1 + len(sensors)))
                ###################################
                f.write("    value = {}\n".format(x[1]))
                f.write("    if type(value) == int: value=float(value)\n")
                f.write("    node{}.set_value(value)\n".format(idx + 1 + len(sensors)))
                f.write('    act.append(value)\n')
                #f.write("    node{}.set_value({})\n".format(idx + 1 + len(sensors), x[1]))
                #f.write('    act.append({})\n'.format(x[1]))
                f.write("    ad = ad + 2\n")
                f.write(
                    "    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[{}], data_format='>f')\n".format(
                        x[1]))

        f.write("\n    try:\n")
        f.write('        handler = SubHandler()\n')
        f.write('        sub = client.create_subscription(0, handler)\n')
        f.write('        handle=sub.subscribe_data_change(nodes)\n')
        f.write('        time.sleep(0.1)\n')

        if len(actuators) != 0:
            f.write("\n        while True:\n")
            f.write("            for idx, x in enumerate(act):\n")
            f.write("                r_a = (len_sensors * 2) + (idx * 2)\n")
            f.write("                a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')\n")
            f.write("                if a[0] != act[idx]:\n")
            f.write("                    nodd = globals()['node{}'.format(len_sensors + 1 + idx)]\n")
            f.write("                    nodd.set_value(a[0])\n")
            f.write("                    act[idx] = a[0]\n")
            f.write("                time.sleep(0.7)\n")

        f.write("\n    finally:\n")
        f.write("        print('..retry')\n")

        f.close()

def modbus(path_temp_script):
    with open(r'{}/modbus.py'.format(path_temp_script), 'w') as f:
        f.write("import modbus_tk\n")
        f.write("import modbus_tk.defines as cst\n")
        f.write("import modbus_tk.modbus_tcp as modbus_tcp\n\n")

        f.write('if __name__ == "__main__": \n\n')
        f.write('    server = modbus_tcp.TcpServer()\n')
        f.write('    server.start()\n')
        f.write('    slave1 = server.add_slave(1)\n')
        f.write('    slave1.add_block("a", cst.HOLDING_REGISTERS, 0, 100)')
