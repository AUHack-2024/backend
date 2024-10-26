import asyncio
import websockets
import base64
import json

from frame_extractor import Frame
clients = set()

async def register(websocket):
    clients.add(websocket)
    print("Client connected.")
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("Client disconnected.")


async def send_image(frames):
    try:
        serialized_frames = serialize_frames(frames)
        
        for client in clients:
                await client.send(serialized_frames)
                
        print("Image queued to be sent to clients.")
    except FileNotFoundError:
        print("Image file not found.")
    except Exception as e:
        print(f"Error in send_image: {e}")



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






def serialize_frames(frames):
    str = "["
    
    for frame in frames:
        str += f"{{\"image\": \"{frame.image}\", \"score\": {frame.score}}},"
    
    return str[:-1] + "]"