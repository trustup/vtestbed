import sys

sys.path.insert(0, "..")
import time

from opcua import ua, Server

if __name__ == "__main__":
    # setup our server
    server = Server()
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://localhost:4840")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "position_X", 0.0)
    myvar.set_writable()  # Set MyVariable to be writable by clients

    myvar2 = myobj.add_variable(idx, "position_Y", 0.0)
    myvar2.set_writable()  # Set MyVariable to be writable by clients
    waypoint_x = myobj.add_variable(idx, "start", 0.0)
    waypoint_x.set_writable()  # Set MyVariable to be writable by clients
    waypoint_y = myobj.add_variable(idx, "nextWaypoints", "")
    waypoint_y.set_writable()  # Set MyVariable to be writable by clients
    waypoint_sp = myobj.add_variable(idx, "speed", 0.5)
    waypoint_sp.set_writable()  # Set MyVariable to be writable by clients
    waypoint_station = myobj.add_variable(idx, "station", 0.5)
    waypoint_station.set_writable()  # Set MyVariable to be writable by clients

    # starting!
    server.start()

    myvar.set_value(15)