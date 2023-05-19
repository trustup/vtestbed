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
client = Client(url)
client.connect()
master = modbus_tcp.TcpMaster(host="localhost", port=502)


nodes = []
#passo come variabile quanti elementi ci sono in sensori, esempio 3, so quindi che gli eventuali attuatori saranno dalla posizione 4 in poi
act = [] #qui ci passo solo gli attuatori

root = client.get_objects_node()
obj = client.get_node(root)
run = obj.get_child('1:OpenModelica.run')

var1 = obj.get_child('1:tank1.V')
nodes.append(var1)
var2 = obj.get_child('1:openTank.V')
nodes.append(var2)
var3 = obj.get_child('1:u')
nodes.append(var3)
number_sensors=2
act=[var3] #lato generazione vado ad inserire var{}.format(number_sensors + x)

run.set_value(True)
var3.set_value(1.0)

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        val = round(val, 3)
        #print(val)
        for idx, x in enumerate(nodes):
            if node == nodes[idx]:
                ad=idx*2
                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=ad, output_value=[val], data_format='>f')




def read():
    threading.Timer(2, read).start()
    a=master.execute(1,cst.READ_HOLDING_REGISTERS, 4, 2, data_format='>f')
    print('LEGGOOOO',a)

if len(act) != 0:
    read()

handler = SubHandler()
sub = client.create_subscription(0, handler)
handle=sub.subscribe_data_change(nodes)