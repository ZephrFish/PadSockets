import asyncio
import websockets
import os

async def upload(websocket, path):
    filename = await websocket.recv()
    filesize = int(await websocket.recv())
    with open(filename, 'wb') as f:
        while filesize > 0:
            data = await websocket.recv()
            f.write(data)
            filesize -= len(data)
    await websocket.send('Upload complete.')

async def download(websocket, path):
    filename = await websocket.recv()
    if os.path.isfile(filename):
        filesize = os.path.getsize(filename)
        await websocket.send(str(filesize))
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                await websocket.send(data)
    else:
        await websocket.send('File not found.')

async def main(websocket, path):
    async for message in websocket:
        if message == 'upload':
            await upload(websocket, path)
        elif message == 'download':
            await download(websocket, path)
        else:
            await websocket.send('Invalid command.')

start_server = websockets.serve(main, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
