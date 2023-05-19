import asyncio
import websockets
import time

data = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'Select OS', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0, input2=0, PLC=0', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 20, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}

async def hello():
    uri = "ws://192.168.1.68:8765"
    async with websockets.connect(uri) as websocket:

        await websocket.send("900")
        await websocket.send("100")
        
        while True:
            retn = await websocket.recv()
            print(retn)
        #retn2 = await websocket.recv()
        #print(retn2)
            time.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
