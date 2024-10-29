import asyncio
import websockets

clients = set()

async def register(websocket):
    clients.add(websocket)
    print("Client connected.")
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("Client disconnected.")


async def send_video_info(video_info):
    try:
        for client in clients:
                await client.send(video_info)
                
        print("Image queued to be sent to clients.")
    except FileNotFoundError:
        print("Image file not found.")
    except Exception as e:
        print(f"Error in send_video_info: {e}")



async def handler(websocket, path, lock):
    await register(websocket)

def start_server(lock):
    async def server():
        async with websockets.serve(lambda ws, path: handler(ws, path, lock), "0.0.0.0", 8080):
            print("Server started at ws://0.0.0.0:8080")
            await asyncio.Future()  # Run forever

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server())