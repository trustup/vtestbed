import threading
import time
import timeit
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

master = modbus_tcp.TcpMaster(host="localhost", port=502)

while True:
    #a = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 10)
    a = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 2, data_format='>f')
    b = master.execute(1, cst.READ_HOLDING_REGISTERS, 2, 2, data_format='>f')
    c = master.execute(1, cst.READ_HOLDING_REGISTERS, 4, 2, data_format='>f')
    print(a)
    print(b)
    print(c)
    time.sleep(1)
