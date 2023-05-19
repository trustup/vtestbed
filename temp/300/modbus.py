import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

if __name__ == "__main__": 

    server = modbus_tcp.TcpServer()
    server.start()
    slave1 = server.add_slave(1)
    slave1.add_block("a", cst.HOLDING_REGISTERS, 0, 100)