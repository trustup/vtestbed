import sys
sys.path.insert(0, "..")
from opcua import ua, Server

if __name__ == "__main__":

    server = Server()
    server.set_endpoint("opc.tcp://localhost:4841")

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    myobj = server.get_objects_node()

    myvar0 = myobj.add_variable(idx, "position_X", 0.0)
    myvar0.set_writable()
    myvar1 = myobj.add_variable(idx, "position_Y", 0.0)
    myvar1.set_writable()
    myvar2 = myobj.add_variable(idx, "station", 0.0)
    myvar2.set_writable()
    myvar3 = myobj.add_variable(idx, "state_station", 0.0)
    myvar3.set_writable()
    myvar4 = myobj.add_variable(idx, "speed", 0.0)
    myvar4.set_writable()
    myvar5 = myobj.add_variable(idx, "start", 0.0)
    myvar5.set_writable()
    myvar6 = myobj.add_variable(idx, "nextWaypoints", 0.0)
    myvar6.set_writable()
    myvar7 = myobj.add_variable(idx, "plc_control", 0.0)
    myvar7.set_writable()

    server.start()
