import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct

sensors_address = []
actuators_address = [14]
def unpack_float(fl):
    a = struct.unpack('>HH', struct.pack('>f',fl))
    return(a)

actuators = []
def write_act_local():
    actuators = [0] * len(actuators_address)
    r_a = len(sensors_address) * 2
    for idx, x in enumerate(actuators_address):
        a = master.execute(1, cst.READ_HOLDING_REGISTERS, x, 2, data_format='>f')
        actuators[idx] = a[0]
        fl = unpack_float(a[0])
        slave.set_values("a", r_a, fl)
        r_a = r_a + 2
    return actuators

def get_act_local():
    r_a = len(sensors_address) * 2
    cr = [0] * len(actuators_address)
    for idx, x in enumerate(actuators_address):
        ab = master_local.execute(1, cst.READ_HOLDING_REGISTERS, r_a, 2, data_format='>f')
        cr[idx] = ab[0]
        r_a = r_a + 2
    return(cr)

def act_control():
    if len(actuators_address) != 0:
        current = get_act_local()
        for idx, x in enumerate(actuators):
            if current[idx] != x:
                actuators[idx] = current[idx]
                master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=actuators_address[idx],output_value=[current[idx]], data_format='>f')
            time.sleep(0.5)

sensors=[]
sensors = [0] * len(sensors_address)
def write_sens_local():
    r_s = 0
    for idx, x in enumerate(sensors_address):
        b = master.execute(1, cst.READ_HOLDING_REGISTERS, x, 2, data_format='>f')
        sensors[idx] = b[0]
        fl2 = unpack_float(b[0])
        slave.set_values("a", r_s, fl2)
        r_s = r_s + 2
time.sleep(0.5)

if __name__ == "__main__":

    server = modbus_tcp.TcpServer()
    server.start()
    slave1 = server.add_slave(1)
    slave1.add_block("a", cst.HOLDING_REGISTERS, 0, 100)  # address 0
    slave = server.get_slave(1)
    master = modbus_tcp.TcpMaster(host="900.1.1.2", port=502) #IP MODEL
    master_local = modbus_tcp.TcpMaster(host="localhost", port=502) #IP LOCAL

    if len(actuators_address) != 0:
        actuators = write_act_local()

    while True:
        write_sens_local()
        act_control()
