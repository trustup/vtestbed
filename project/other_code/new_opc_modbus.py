import time
import timeit
import opcua
from opcua import Client
from opcua import ua
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct

def unpack_float(fl):
    a = struct.unpack('>HH', struct.pack('>f',fl))
    return(a)

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        for idx, x in enumerate(nodes):
            if node == nodes[idx]:
                ad=idx*2
                value = unpack_float(val)
                slave.set_values("a", ad, value)
                #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[value], data_format='>f')

if __name__ == "__main__":

    server = modbus_tcp.TcpServer()
    server.start()
    master = modbus_tcp.TcpMaster(host="localhost", port=502)
    slave1 = server.add_slave(1)
    slave1.add_block("a", cst.HOLDING_REGISTERS, 0, 100)  # address 0, length 100
    slave = server.get_slave(1)

    url = "opc.tcp://localhost:4841"
    client = Client(url, timeout=100)
    client.connect()

    nodes = []
    root = client.get_objects_node()
    obj = client.get_node(root)
    run = obj.get_child('1:OpenModelica.run')

   #sensors:
    node1 = obj.get_child('1:mainTank.V')
    nodes.append(node1)
    node2 = obj.get_child('1:secondaryTank.V')
    nodes.append(node2)
    node3 = obj.get_child('1:velocityTank2')
    nodes.append(node3)
    node4 = obj.get_child('1:massOverflow')
    nodes.append(node4)
    len_sensors = 4
    run.set_value(True)
    act=[]
    ad = (len_sensors * 2) - 2
   #actuator 1
    node5 = obj.get_child('1:input1')
    node5.set_value(0.6)
    act.append(0.6)
    ad = ad + 2
    wr = unpack_float(0.6)
    #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.6], data_format='>f')
    slave.set_values("a", ad, wr)
    #actuator 2
    node6 = obj.get_child('1:input2')
    node6.set_value(0.3)
    act.append(0.3)
    ad = ad + 2
    wr = unpack_float(0.3)
    slave.set_values("a", ad, wr)
    #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.3], data_format='>f')
   #actuator 3
    node7 = obj.get_child('1:input3')
    node7.set_value(0.5)
    act.append(0.5)
    ad = ad + 2
    #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[0.5], data_format='>f')
    wr = unpack_float(0.3)
    slave.set_values("a", ad, wr)

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
                time.sleep(1)

    finally:
        print('..retry')