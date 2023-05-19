def server_opcua(sensors, actuators, path_temp_script):

    url_opc = 'localhost'
    with open(r'{}/server_opcua.py'.format(path_temp_script), 'w') as f:

        f.write('import sys\n')
        f.write('sys.path.insert(0, "..")\n')
        f.write('from opcua import ua, Server\n\n')

        f.write('if __name__ == "__main__":\n\n')
        f.write('    server = Server()\n')
        f.write('    server.set_endpoint("opc.tcp://{}:4841")\n\n'.format(url_opc))
        f.write('    uri = "http://examples.freeopcua.github.io"\n')
        f.write('    idx = server.register_namespace(uri)\n\n')

        f.write('    myobj = server.get_objects_node()\n\n')

        if len(sensors) != 0:
            for idx, x in enumerate(sensors):
                f.write('    myvar{} = myobj.add_variable(idx, "{}", 0.0)\n'.format(idx, x))
                f.write('    myvar{}.set_writable()\n'.format(idx))

        if len(actuators) != 0:
            for idx, x in enumerate(actuators):
                f.write('    myvar{} = myobj.add_variable(idx, "{}", 0.0)\n'.format(idx+len(sensors), x[0]))
                f.write('    myvar{}.set_writable()\n'.format(idx+len(sensors)))

        f.write('\n    server.start()\n')
        f.close()