import threading
import time
import timeit
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct

logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

server = modbus_tcp.TcpServer()
server.start()

def unpack_float(fl):
    a = struct.unpack('>HH', struct.pack('>f',fl))
    return(a)


slave1 = server.add_slave(1)

slave1.add_block("a", cst.HOLDING_REGISTERS, 0, 10)#address 0, length 100
slave1.add_block("b", cst.HOLDING_REGISTERS, 200, 20)#address 200, length 20

aa= (16025,39322)
slave = server.get_slave(1)

valore = unpack_float(0.3)
valore2 = unpack_float(0.6)
valore3 = unpack_float(0.7)

slave.set_values ("a", 0, valore)
slave.set_values ("a", 2, valore2)
slave.set_values ("a", 4, valore3)

print(slave.get_values("a",0,0))
#server.start()