import threading
import time
import timeit
import opcua
from opcua import Client
from opcua import ua
#import modbus_tk
#import modbus_tk.defines as cst
#import modbus_tk.modbus_tcp as modbus_tcp

url = "opc.tcp://localhost:4841"
client = Client(url)
client.connect()
#master = modbus_tcp.TcpMaster(host="localhost", port=502)


run = client.get_node(10001)
run.set_value(True)

nodes = []
obj = client.get_node(85)
tank1V = client.get_node("ns=1;i=150000030")
a = obj.get_children()
tank2V = client.get_node("ns=1;i=150000004")
pressure = client.get_node("ns=1;i=100000055")
nodes.append(tank2V)
nodes.append(tank1V)
print(nodes)


class SubHandler(object):
    def datachange_notification(self, node, val, data):
        val = round(val, 3)
        for idx, x in enumerate(nodes):
            if node == nodes[idx]:
                print("node", node)
                print(idx*2)
        #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=0, output_value=[val], data_format='>f')



'''
finished = False
while not finished:
    try:
        handler1 = SubHandler1()
        sub1 = client.create_subscription(0, handler1)
        handle1 = sub1.subscribe_data_change(tank2V)
        finished = True
    except:
        print("timeout A")

finished = False
while not finished:
    try:
        handler2 = SubHandler2()
        sub2 = client.create_subscription(0, handler2)
        handle2 = sub2.subscribe_data_change(tank1V)
        finished = True
    except:
        print("timeout B")

finished = False
while not finished:
    try:
        handler3 = SubHandler3()
        sub3 = client.create_subscription(0, handler3)
        handle3 = sub3.subscribe_data_change(pressure)
        finished = True
    except:
        print("?????")
'''

finished = False
while not finished:
    try:
        handler = SubHandler()
        sub = client.create_subscription(0, handler)
        handle = sub.subscribe_data_change(nodes)
    except:
        print("..retry")

