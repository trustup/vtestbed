import asyncio
import websockets
import yaml

async def hello(websocket, path):
    dav = await websocket.recv()
    #print(f"< {name}")

    #greeting = f"Hello {name}!"
    #greeting = {name}

    #a = yaml.load(dav)
    a = yaml.safe_load(dav)
    with open(r'/home/ubuntu/invio.yml', 'w') as outfile:
        yaml.dump(a,outfile, default_flow_style=True)
    print(a)
    await websocket.send(a)
    #print(f"> {greeting}")
    #print(type(greeting))
    #prova = yaml.safe_load(greeting)
    #print(prova)
    #print(type(yam))
    #with open(r'/home/ubuntu/invio.yml','w') as outfile:
    #    yaml.dump(yam,outfile, default_flow_style=True)

start_server = websockets.serve(hello, "10.8.0.94", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
