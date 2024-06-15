import asyncio
import simple_websocket
from simple_websocket import AioClient, ConnectionClosed

async def main():
    ws = await AioClient.connect('ws://localhost:80/ws')
   #ws = await AioClient.connect('ws://0.tcp.ap.ngrok.io:12476/ws') - use this address when running remotely on IOT client and update URI
    
    try:
        while True:
            data = input('> ')
            await ws.send(data)
            data = await ws.receive()
            print(f'< {data}')
    except (KeyboardInterrupt, EOFError, ConnectionClosed):
        await ws.close()

if __name__ == '__main__':
    asyncio.run(main())
