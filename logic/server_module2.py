import asyncio
import websockets
import base64
from asyncio import Queue

clients = set()
message_queue = Queue()

async def register(websocket):
    clients.add(websocket)
    print("Client connected.")
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("Client disconnected.")

async def send_image():
    # Periodically queue the image for sending every 5 seconds (adjust as needed)
    try:
        with open("pictures/still/frame_v1.0.0_0.jpg", "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            await message_queue.put(image_data)
            print("Image queued to be sent to clients.")
    except FileNotFoundError:
        print("Image file not found.")
    except Exception as e:
        print(f"Error in send_image: {e}")
        

async def message_handler():
    # Continuously send messages from the queue to all clients
    while True:
        message = await message_queue.get()
        if message is None:
            break
        disconnected_clients = set()
        for client in clients:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                disconnected_clients.add(client)
                print("Client disconnected during message send.")
        clients.difference_update(disconnected_clients)
        print(f"Image sent to {len(clients)} clients.")

async def handler(websocket, path):
    await register(websocket)

async def start_server():
    # Start the WebSocket server
    server = await websockets.serve(handler, "0.0.0.0", 8080)
    print("Server started at ws://0.0.0.0:8080")
    
    # Start the image sending and message handler tasks
    # send_image_task = asyncio.create_task(send_image())
    # message_handler_task = asyncio.create_task(message_handler())
    
    await server.wait_closed()
    # await send_image_task
    # await message_handler_task
