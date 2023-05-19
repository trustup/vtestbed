import threading
import time
import timeit
import opcua
from opcua import Client
from opcua import ua
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

url = "opc.tcp://localhost:4841"
client = Client(url, timeout=300)
client.connect()
#master = modbus_tcp.TcpMaster(host="localhost", port=502)


nodes = []
root = client.get_objects_node()
obj = client.get_node(root)
#run = obj.get_child('1:OpenModelica.run')
print(root)
print(obj)


#sensors:
#node1 = obj.get_child('1:mainTank.V')
#nodes.append(node1)
#node2 = obj.get_child('1:secondaryTank.V')
#nodes.append(node2)
#len_sensors = 2

##actuators:
#act = []
#node3 = obj.get_child('1:on')

#nodes.append(node3)
#run.set_value(True)
#node3.set_value(1.0)
#act.append(1.0)
#print(act)

# class SubHandler(object):
#     def datachange_notification(self, node, val, data):
#         val = round(val, 3)
#         for idx, x in enumerate(nodes):
#             if node == nodes[idx]:
#                 print(node, val)
#                 ad = idx*2
#                 #master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')
#
# # def read():
# #     threading.Timer(2, read).start()
# #     for idx, x in enumerate(act):
# #         r_a = (len_sensors * 2) + (idx * 2)
# #         a = master.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')
# #         if a[0] == act[idx]:
# #             print("non faccio niente")
# #         elif a[0] != act[idx]:
# #             print("cambio valore..")
# #             node3.set_value(a[0])
# #             act[idx] = a[0]
#
#     #print('LEGGOOOO',a[0])
#
#
#
# handler = SubHandler()
# sub = client.create_subscription(0, handler)
# handle = sub.subscribe_data_change(nodes)
#
# #read()
