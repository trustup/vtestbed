import sys
sys.path.insert(0, "..")
import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from opcua import Client


class SubHandler(object):
    def datachange_notification(self, node, val, data):
        #print("Python: New data change event", node, val)
        for idx, x in enumerate(nodes):
            if node == nodes[idx]:
                ad=idx*2
                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')



if __name__ == "__main__":

    master = modbus_tcp.TcpMaster(host="localhost", port=502)
    client = Client("opc.tcp://localhost:4841", timeout=100)
    client.connect()
    root = client.get_objects_node()
    obj = client.get_node(root)
    run = obj.get_child('1:OpenModelica.run')
    nodes = []
    node1 = obj.get_child('1:mainTank.V')
    nodes.append(node1)
    node2 = obj.get_child('1:secondaryTank.V')
    nodes.append(node2)
    run.set_value(True)
    len_sensors = 2


    act = []
    ad = len_sensors
       #actuator 1
    node3 = obj.get_child('1:on')
    node3.set_value(1.0)
    act.append(1.0)
    ad = ad + 2
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[1.0], data_format='>f')
    #actuator 2
    ad = ad + 2
    node4 = obj.get_child('1:input1')
    node4.set_value(1.0)
    act.append(1.0)
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[1.0], data_format='>f')
      #actuator 3
    ad = ad + 2
    node5 = obj.get_child('1:input2')
    node5.set_value(1.0)
    act.append(1.0)
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[1.0], data_format='>f')
      #actuator 4
    ad = ad + 2
    node6 = obj.get_child('1:input3')
    node6.set_value(1.0)
    act.append(1.0)
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[1.0], data_format='>f')

    try:

        # subscribing to a variable node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(nodes)
        time.sleep(0.1)

        while True:
            for idx, x in enumerate(act):
                r_a = (len_sensors * 2) + (idx * 2)
                a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')
                if a[0] != act[idx]:
                    print("nuovo valore per nodo numero",len_sensors + 1 + idx)
                    nodd = globals()['node{}'.format(len_sensors + 1 + idx)]
                    nodd.set_value(a[0])
                    act[idx] = a[0]
                time.sleep(1)

    finally:
        print('..retry')