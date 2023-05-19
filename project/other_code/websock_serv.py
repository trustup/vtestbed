import asyncio
import websockets
import yaml

async def hello(websocket, path):
    name = await websocket.recv()

    print(f"< {name}")

    greeting = f"Hello {name}!"
    #greeting = {name}

    await websocket.send(greeting)
    print(f"> {greeting}")
    #print(type(greeting))
    #prova = yaml.safe_load(greeting)
    #print(prova)
    #print(type(prova))

start_server = websockets.serve(hello, "10.8.0.94", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
