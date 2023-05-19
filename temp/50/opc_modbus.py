import time
import timeit
import opcua
from opcua import Client
from opcua import ua
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        for idx, x in enumerate(nodes):
            if node == nodes[idx]:
                ad=idx*2
                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')

if __name__ == "__main__":

    master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)
    url = "opc.tcp://localhost:4841"
    client = Client(url, timeout=100)
    client.connect()

    nodes = []
    root = client.get_objects_node()
    obj = client.get_node(root)
    run = obj.get_child('1:OpenModelica.run')
    run.set_value(True)

   #sensors:
    node1 = obj.get_child('1:mainTank.V')
    nodes.append(node1)
    node2 = obj.get_child('1:secondaryTank.V')
    nodes.append(node2)
    node3 = obj.get_child('1:velocityTank2')
    nodes.append(node3)
    node4 = obj.get_child('1:massOverflow')
    nodes.append(node4)
    node5 = obj.get_child('1:pressure1')
    nodes.append(node5)
    len_sensors = 5
    act=[]
    ad = (len_sensors * 2) - 2
   #actuator 1
    node6 = obj.get_child('1:input1')
    nodes.append(node6)
    value = 0.6
    if type(value) == int: value=float(value)
    node6.set_value(value)
    act.append(value)
    ad = ad + 2
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.6], data_format='>f')
   #actuator 2
    node7 = obj.get_child('1:input2')
    nodes.append(node7)
    value = 0.1
    if type(value) == int: value=float(value)
    node7.set_value(value)
    act.append(value)
    ad = ad + 2
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.1], data_format='>f')
   #actuator 3
    node8 = obj.get_child('1:input3')
    nodes.append(node8)
    value = 0.5
    if type(value) == int: value=float(value)
    node8.set_value(value)
    act.append(value)
    ad = ad + 2
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.5], data_format='>f')
   #actuator 4
    node9 = obj.get_child('1:PLC')
    nodes.append(node9)
    value = 0.0
    if type(value) == int: value=float(value)
    node9.set_value(value)
    act.append(value)
    ad = ad + 2
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.0], data_format='>f')
   #actuator 5
    node10 = obj.get_child('1:on')
    nodes.append(node10)
    value = 1.0
    if type(value) == int: value=float(value)
    node10.set_value(value)
    act.append(value)
    ad = ad + 2
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[1.0], data_format='>f')

    try:
        handler = SubHandler()
        sub = client.create_subscription(0, handler)
        handle=sub.subscribe_data_change(nodes)
        time.sleep(0.1)

        while True:
            for idx, x in enumerate(act):
                r_a = (len_sensors * 2) + (idx * 2)
                a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')
                if a[0] != act[idx]:
                    nodd = globals()['node{}'.format(len_sensors + 1 + idx)]
                    nodd.set_value(a[0])
                    act[idx] = a[0]
                time.sleep(0.7)

    finally:
        print('..retry')
