import asyncio
import websockets
import yaml
import yaml_converter_auto
import start_scenario_auto
import restart_scenario_auto
import close_scenario_auto
import destroy_scenario_auto
import db_connection
import json
import time
import os as command_os

#models = json.dumps(db_connection.get_models())
models = json.dumps(db_connection.get_models2('matlab'))
models_os = json.dumps(db_connection.get_os("model"))
mtu_os = json.dumps(db_connection.get_os("mtu"))
rtu_os = json.dumps(db_connection.get_os("rtu"))
plc_os = json.dumps(db_connection.get_os("plc"))
generic_os = json.dumps(db_connection.get_os("generic"))
router_os = json.dumps(db_connection.get_os("router"))
modeler = json.dumps(db_connection.get_modeler())
interfaces = json.dumps(db_connection.get_interfaces())
hmi = json.dumps(db_connection.get_hmi())
#scenario_saved = json.dumps(db_connection.get_scenario_saved())

prova = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0.6', 'sensors': 'mainTank.V'}}, 'MTU': {'name': 'Node_7', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': 'high_limit', 'variable': 'mainTank.V>60'}}, 'RTU': {'name': 'Node_4, Node_5, Node_4, Node_5', 'os': 'ubuntu, ubuntu, ubuntu, ubuntu', 'input': 'mainTank.V,, Node_8; input1,, Node_8; mainTank.V,, Node_8; input1,, Node_8'}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': 'Node_6', 'os': 'kali'}, 'ROUTER_FIREWALL': {'name': 'Node_8', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=src=net1 dst=dst=net0'}]}]}, 'NETWORKS': {'name': 'net0', 'members': 'Node_7', 'gateway': 'Node_8'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': 'ssh_root_deny', 'target': 'Node_8'}, 'EXPORT_DATA': {'name': 'demo', 'ip_server': '192.168.1.258', 'source_data': None, 'log_type': None}}
data = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0, input2=0, PLC=0', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}
sample = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'Select OS', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0.6, input2=0.3, input3=0.5', 'sensors': 'mainTank.V, secondaryTank.V, velocityTank2, massOverflow'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': None}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'tankmodel; mtu-hmi', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 20, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}

erro = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0.6', 'sensors': 'mainTank.V'}}, 'MTU': {'name': 'Node_6', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': 'Node_2', 'os': 'ubuntu', 'input': 'mainTank.V'}, 'PLC': {'name': 'Node_8', 'os': 'ubuntu', 'input': 'mainTank.V', 'output_slave': 'input1', 'plc_code': 'double_control.st'}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'Node_7', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=net1 dst=net0'}]}]}, 'NETWORKS': {'name': 'net1; net0', 'members': 'tankmodel, Node_2; Node_6, Node_8', 'gateway': 'Node_7; Node_7'}, 'CONFIG': {'entry_point': 'Node_6', 'cyber_range_id': 40, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': '', 'log_type': ''}}

#a=json.dumps(models)

async def scenario(websocket, path):

    #online = await websocket.recv()
    #if online == 'Client on line': await websocket.send("Server Ready")

    dt = await websocket.recv()

    # send query to fron end
    if dt == "001":
        #await websocket.send("101" + str(models)) #MODIFICARE! la query deve essere eseguita dopo che il client ha scelto il modeler, non deve essere statica
        #await websocket.send("102" + str(models_os))
        await websocket.send("103" + str(mtu_os))
        await websocket.send("104" + str(rtu_os))
        await websocket.send("105" + str(plc_os))
        await websocket.send("106" + str(generic_os))
        await websocket.send("107" + str(router_os))
        await websocket.send("108" + str(modeler))
        await websocket.send("109" + str(interfaces))
        await websocket.send("110" + str(hmi))
        await websocket.send("111" + str(json.dumps(db_connection.get_scenario_saved())))

    # send sensors to client
    elif dt == "002":
        mod = await websocket.recv()
        res = db_connection.get_sensors(mod)
        js = json.dumps(res)
        print("ris query: "+ str(res))
        await websocket.send("201" + str(js))

    # send actuators to client
    elif dt == '003':
        mod = await websocket.recv()
        res = db_connection.get_actuators(mod)
        js = json.dumps(res)
        print("invio js")
        await websocket.send("301" + str(js))

    # send fix to client
    elif dt == '004':
        vm = await websocket.recv()
        os = await websocket.recv()
        res = db_connection.get_fix(vm, os)
        js = json.dumps(res)
        print(js)
        await websocket.send("401" + str(js))

    # send hmi alert to client
    elif dt == '005':
        js = []
        gethmi = await websocket.recv()
        alert = db_connection.get_alert(gethmi)
        js = json.dumps(alert)
        print(js)
        await websocket.send("501" + str(js))
        #if gethmi == 'scadabr':
        #    alert = db_connection.get_alert()
        #    js = json.dumps(alert)
        #    print(js)
        #await websocket.send("501" + str(js))

    #send supported log type to client (log to export on kafka)
    elif dt == '006':
        vm = await websocket.recv()
        os = await websocket.recv()
        res = db_connection.get_log_type(vm, os)
        js = json.dumps(res)
        print(js)
        await websocket.send("601" + str(js))

    #send models based on modeler
    elif dt == '007':
        modeler2 = await websocket.recv()
        #os = await websocket.recv()
        res = db_connection.get_models2(modeler2)
        res2 = db_connection.get_os_modeler(modeler2)
        js = json.dumps(res)
        js2 = json.dumps(res2)
        await websocket.send("101" + str(js))
        await websocket.send("102" + str(js2))

    #send saved scenarios
    elif dt == '008':
        cr_number = await websocket.recv()
        with open ('/home/ubuntu/virtualTestbed/cyris/cyber_range_saved/cyber_{}.json'.format(cr_number)) as json_file:
            data = json_file.read()
        await websocket.send("801" + str(data))

    ####################################################################################################################
    # START SCENARIO
    elif dt == "900":
        await websocket.send("Initializing")
        st = ''
        dt55 = await websocket.recv()  #ricevo lo yaml
        yaml_fe = yaml.safe_load(dt55)  # formatto lo yaml ricevuto dal front end
        st = await websocket.recv() #ricevo il file .st (plc)

        #saving scenario
        scenario = await websocket.recv()
        scenario = json.loads(scenario)
        with open(r'/home/ubuntu/virtualTestbed/cyris/cyber_range_saved/cyber_{}.json'.format(scenario['layers'][2]['cyberRangeID']), 'w') as file:
            data_out = json.dump(scenario, file, sort_keys=False)

        with open('/home/ubuntu/virtualTestbed/models/openmodelica/tankmodel_plc/double_control.st') as f:
            stread = f.read()
        st_construct = [{"plcName":"plc1", "name":"robot_control.st","value": '{}'.format(stread)}]

        value = yaml_converter_auto.converter(yaml_fe, dt, st) #passo lo yaml al convertitore
        #await websocket.send("000" + str(json.dumps("Scenario Ready")))
        print(value)
        with open(r'/home/ubuntu/virtualTestbed/temp/{}/yaml_received.yml'.format(value[3]), 'w') as file:
            data_out = yaml.dump(yaml_fe, file, sort_keys=False)

        #if len(value) == 1:
        #    await websocket.send(value)
        #else:
        #    await websocket.send("Parsing OK")
        #    await websocket.send(start_scenario_auto.start_scenario(value))



    # RESTART SCENARIO
    # elif dt == "910":
    #     await websocket.send("Initializing Restart")
    #     dt55 = await websocket.recv()
    #     print(dt55)
    #     prova = yaml.safe_load(dt55)
    #     print(prova)
    #     value = yaml_converter_auto.converter(sample, dt)
    #     if len(value) == 1:
    #         await websocket.send(value)
    #     else:
    #         await websocket.send("Parsing OK")
    #         await websocket.send(restart_scenario_auto.restart(value))

    #RESTART SCENARIO2
    elif dt == "910":
        await websocket.send("Initializing Restart")
        dt55 = await websocket.recv() #ricevo il cyber range number
        print(dt55)
        try:
            with open(r'/home/ubuntu/virtualTestbed/temp/{}/values.yml'.format(dt55)) as f:
                value = yaml.safe_load(f)
            await websocket.send(restart_scenario_auto.restart(value))
        except:
            await websocket.send("Wrong Cyber Range Number")

    # # CLOSE SCENARIO
    # elif dt == "920":
    #     await websocket.send("Closing Scenario..")
    #     dt55 = await websocket.recv()
    #     prova = yaml.safe_load(dt55)
    #     value = yaml_converter_auto.converter(sample, dt)
    #     if len(value) == 1:
    #         await websocket.send(value)
    #     else:
    #         await websocket.send("Parsing OK")
    #         await websocket.send(close_scenario_auto.close_scenario(value))

    # CLOSE SCENARIO2
    elif dt == "920":
        await websocket.send("Closing Scenario")
        dt55 = await websocket.recv()  # ricevo il cyber range number
        try:
            with open(r'/home/ubuntu/virtualTestbed/temp/{}/values.yml'.format(dt55)) as f:
                value = yaml.safe_load(f)
            await websocket.send(close_scenario_auto.close_scenario(value))
        except:
            await websocket.send("Wrong Cyber Range Number")

    # DESTROY SCENARIO
    elif dt == "930":
        print('destroy scenario..')
        dt55 = await websocket.recv()  # ricevo il cyber range number
        try:
            #with open(r'/home/ubuntu/PycharmProjects/temp/{}/values.yml'.format(dt55)) as f:
            #    value = yaml.safe_load(f)
            #await websocket.send(destroy_scenario_auto.destroy_scenario(value))
            db_connection.delete_scenario_layout(dt55)
            command_os.system('sudo rm /home/ubuntu/virtualTestbed/cyris/cyber_range_saved/cyber_{}.json'.format(dt55))
            await websocket.send("931"+str(json.dumps(dt55)))
            await websocket.send("111" + str(json.dumps(db_connection.get_scenario_saved())))
        except:
            await websocket.send("Wrong Cyber Range Number")

    elif dt == "940":
        #await websocket.send("Saving Scenario Configuration")
        dt55 = await websocket.recv()
        dt55 = json.loads(dt55)
        with open(r'/home/ubuntu/virtualTestbed/cyris/cyber_range_saved/cyber_{}.json'.format(dt55['layers'][2]['cyberRangeID']), 'w') as file:
            data_out = json.dump(dt55, file, sort_keys=False)
        db_connection.save_scenario_layout(dt55['layers'][2]['cyberRangeID'])
        await websocket.send("111" + str(json.dumps(db_connection.get_scenario_saved())))



    #print(dt)
    #print(type(dt))
    #inv = yaml.safe_load(dt)
    #print(inv)
    #start = yaml_converter_auto.converter(inv)


    #data = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0, input2=0, PLC=0', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}
    #start = yaml_converter_auto.converter(data)
    #await websocket.send(yaml_converter_auto.converter(data))

    #await websocket.send("Parsing Scenario..")
    #await websocket.send(str(start))
    #await websocket.send('Scenario deploy..')
    #print(start)

start_server = websockets.serve(scenario, "10.8.0.94", 8765)
#start_server = websockets.serve(scenario, "192.168.1.68", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
